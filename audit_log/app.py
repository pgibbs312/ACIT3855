import connexion 
import yaml
import logging
import logging.config
import datetime 
import json
from pykafka import KafkaClient, Producer

logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
with open("app_conf.yml", 'r') as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
def get_score(index):
    """ Get Score Reading in History """
    hostname = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    index = int(index)
    logger.info("Retrieving score at index %d" % index)
    try: 
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
    except:
        logger.error("No more messages found")
    
    logger.error("Could not find score at index %d" % index)
    return { "message": "Not found "}, 404

def get_user(index):

    """ Get User Reading in History """
    hostname = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving user at index %d" % index)
    try: 
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
    except:
        logger.error("No more messages found")
    
    logger.error("Could not find score at index %d" % index)
    return { "message": "Not found "}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("gibbons.peter312-openapi-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8110)