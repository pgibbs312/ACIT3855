import connexion 
import yaml
import logging
import logging.config
import datetime 
import json
from pykafka import KafkaClient, Producer
from time import sleep
from flask_cors import CORS, cross_origin

logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
with open("app_conf.yml", 'r') as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
def get_score(index):
    """ Get Score Reading in History """
    retry_count = 0
    hostname = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    while retry_count < app_config["kafka_connect"]["retry_count"]:
        try:
            logger.info('trying to connect, attemp: %d' % (retry_count))
            print(hostname)
            client = KafkaClient(hosts=hostname) 
            topic = client.topics[str.encode(app_config['events']['topic'])] 
            consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
        except:
            logger.info('attempt %d failed, retry in 5 seoncds' % (retry_count))
            retry_count += 1
            sleep(app_config["kafka_connect"]["sleep_time"])
        else:
            break
    logger.info('connected to kafka')
    
    
    index = int(index)
    logger.info("Retrieving score at index %d" % index)
    try:
        score_list = []
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'addScore':
                score_list.append(msg)
        logger.info('returned payload with trace_id: %s' % (score_list[index]['payload']['trace_id']))
        return score_list[index], 200
    except:
        logger.error("No more messages found")
    
    logger.error("Could not find score at index %d" % index)
    return { "message": "Not found "}, 404

def get_user(index):

    """ Get User Reading in History """
    retry_count = 0
    hostname = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    while retry_count < app_config["kafka_connect"]["retry_count"]:
        try:
            logger.info('trying to connect, attempt: %d' % (retry_count))
            print(hostname)
            client = KafkaClient(hosts=hostname) 
            topic = client.topics[str.encode(app_config['events']['topic'])] 
            consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
        except:
            logger.info('attempt %d failed, retry in 5 seoncds' % (retry_count))
            retry_count += 1
            sleep(app_config["kafka_connect"]["sleep_time"])
        else:
            break
    logger.info('connected to kafka')
    
    
    index = int(index)
    logger.info("Retrieving user at index %d" % index)
    try:
        user_list = []
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'add_user':
                user_list.append(msg)
        logger.info('returned payload with trace_id: %s' % (user_list[index]['payload']['trace_id']))
        return user_list[index], 200
    except:
        logger.error("No more messages found")
    
    logger.error("Could not find user at index %d" % index)
    return { "message": "Not found "}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("gibbons.peter312-openapi-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8110)