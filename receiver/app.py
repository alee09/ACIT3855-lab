from datetime import datetime
import connexion
from connexion import NoContent
import json
# import requests
# from sqlalchemy import false
import yaml
import logging.config
from uuid import uuid1
from pykafka import KafkaClient
events_file = "./events.json"
event_max = 10

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')


def report_rapid_test_reading(body):
    headers = {"content-type": "application/json"}
    event_id = str(uuid1())
    body['trace_id'] = event_id

    client = KafkaClient(hosts='acit3855-asynchronousmessaging.eastus.cloudapp.azure.com:9092') 
    topic = client.topics[str.encode("events")] 
    producer = topic.get_sync_producer() 
    
    msg = { "type": "rapid_test",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%d %H:%M:%S.%f"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201

def user_data(body):
    # reading_file = "./user_data.json"
    # user_json = json.dump(body, indent=2)
    # with open("user_date.json","w") as user_data:
    #     user_data.write(user_json)
    event_id = str(uuid1())
    body['trace_id'] = event_id
    headers = {"content-type": "application/json"}
    # response = requests.post(
    #     app_config["eventstore2"]["url"], json=body, headers=headers)

    # logger.info(f"Received event User added request with a trace id of {event_id}")
    # logger.info(f"Returned event User added response (Id: {event_id} with status {response.status_code}")

    client = KafkaClient(hosts='acit3855-asynchronousmessaging.eastus.cloudapp.azure.com:9092') 
    topic = client.topics[str.encode("events")] 
    producer = topic.get_sync_producer()

    msg = { "type": "user",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%d %H:%M:%S.%f"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml", strict_validation=False, validate_responses=False) 
 
if __name__ == "__main__": 
    app.run(port=8080)