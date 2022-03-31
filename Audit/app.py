import connexion
import swagger_ui_bundle
from pykafka import KafkaClient
import yaml
import json
import logging.config

with open('app_conf.yml', 'r') as f:
    app_conf = yaml.safe_load(f.read())
    user = app_conf['datastore']['user']
    password = app_conf['datastore']['password']
    hostname = app_conf['datastore']['hostname']
    port = app_conf['datastore']['port']
    db = app_conf['datastore']['db']
    trace_id = app_conf['datastore']['trace_id']

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

def get_rapid_test_reading(index): 
    """ Get Rapid Test Reading in History """ 
    hostname = "%s:%d" % (app_conf["events"]["hostname"],  
                          app_conf["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_conf["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving rapid test at index %d" % index) 
    try: 
        count = 0
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
            if count == index:
                return msg, 200
            count += 1
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200 
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find rapid test result at index %d" % index) 
    return { "message": "Not Found"}, 404

def get_user_data(index): 
    """ Get Rapid Test Reading in History """ 
    hostname = "%s:%d" % (app_conf["events"]["hostname"],  
                          app_conf["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_conf["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving user at index %d" % index) 
    try: 
        count = 0
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
            if count == index:
                return msg, 200
            count += 1
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200 
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find user data at index %d" % index) 
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yml") 
 
if __name__ == "__main__":
    app.run(port=8110)