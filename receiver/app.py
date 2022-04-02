from urllib import response
import uuid
import connexion
import yaml
import logging
import logging.config
from connexion import NoContent
import datetime
import json
import requests
from pykafka import KafkaClient, Producer

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

def addScore(body):
    id = str(uuid.uuid4())
    body['trans_id'] = id
    payload = body
    headers = {'Content-Type': 'application/json'}
    logger.info(f'Stored event addScore request with a trace id of {id}')
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}: {app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "addScore",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H: %M:%S"),
        "payload": payload
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # r = requests.post(app_config['eventstore_1']['url'], json=payload, headers=headers)
    # if r.status_code == 201:
    #     logger.info(f'Returned Event: addscore id {id} with status code {r.status_code}')
    # else:
    #     logger.info(f'addScore event: {id} Bad request')
    # return NoContent, 201


def add_user(body):

    id = str(uuid.uuid4())
    body['trans_id'] = id
    logger.info(f'Stored event add_user request with a trace id of ${id}')
    payload = body
    headers = {'Content-Type': 'application/json'}
    logger.info(f'Returned event add_user response id: ${id} with status 201')
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}: {app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "add_user",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H: %M:%S"),
        "payload": payload
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    # r = requests.post(app_config['eventstore_2']['url'], json=payload, headers=headers)
    # if r.status_code == 201:
    #     logger.info(f'Returned event: add_user if {id} with status code {r.status_code}')
    # else:
    #     logger.info(f'add_user event: {id} Bad request')
    # return NoContent, r.status_code


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("BCIT37-game-score-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8080)
