from datetime import datetime
import connexion
from connexion import NoContent
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from rapid_test import rapid_test
from user import User
import logging.config
import yaml
from uuid import uuid1
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


with open('app_conf.yml', 'r') as f:
    app_conf = yaml.safe_load(f.read())
    user = app_conf['datastore']['user']
    password = app_conf['datastore']['password']
    hostname = app_conf['datastore']['hostname']
    port = app_conf['datastore']['port']
    db = app_conf['datastore']['db']

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

reading_file = "readings.json"
events_file = "events.json"
event_max = 10

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

def get_rapid_test_reading(timestamp):
    """ gets new rapid test reading after the timestamp """
    logger.info(f'Connecting to DB. Hostname:{hostname}, Port:{port}')
    session = DB_SESSION()
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    readings = session.query(rapid_test).filter(rapid_test.date >= timestamp_datetime) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
    session.close() 
     
    logger.info("Query for rapid test readings after %s returns %d results" %  (timestamp, len(results_list))) 
 
    return results_list, 200 

def get_user_data(timestamp):
    """ gets new user data reading after the timestamp """
    logger.info(f'Connecting to DB. Hostname:{hostname}, Port:{port}')
    session = DB_SESSION()
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    readings = session.query(User).filter(User.date_created >= timestamp_datetime) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 

    session.close() 
     
    logger.info("Query for user readings after %s returns %d results" %  (timestamp, len(results_list))) 
 
    return results_list, 200 

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_conf["events"]["hostname"],   
                          app_conf["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_conf["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
        print(f"\nStart")
        if msg["type"] == "rapid_test": # Change this to your event type 
            # Store the event1 (i.e., the payload) to the DB 
            print(f"\n\nPassed into rapidtest\n\n")
            session = DB_SESSION()
            rt = rapid_test(payload['personal_health_number'],
                            payload['manufacturer']['manName'],
                            payload['manufacturer']['homePage'],
                            payload['result_date'],
                            payload['rapid_test_result'],
                            payload['num_tests_taken'],
                            payload['trace_id'])
            session.add(rt)
            print("\n\nadded")
            session.commit()
            print(f"\n\ncommited")
            session.close()
        elif msg["type"] == "user": # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB 
            session = DB_SESSION()
            usr = User(payload['personal_health_number'],
                        payload['first_name'],
                        payload['last_name'],
                        payload['postal_code'],
                        payload['street'],
                        payload['city'],
                        payload['province'],
                        payload['country'],
                        payload['age'],
                        payload['password'],
                        payload['trace_id'])
            session.add(usr)
            session.commit()
            session.close()
        # Commit the new message as being read 
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) 
 
if __name__ == "__main__":
    t1 = Thread(target= process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)