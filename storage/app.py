from http import client
import connexion
from connexion import NoContent

import mysql.connector
import pymysql
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from game_score import GameScore
from user import User
import logging
import logging.config
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

logger = logging.getLogger('basicLogger')
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
with open("app_conf.yml", 'r') as f:
    parsed_conf = yaml.load(f, Loader=yaml.FullLoader)
    DB_ENGINE = create_engine(f'mysql+pymysql://{parsed_conf["datastore"]["user"]}:{parsed_conf["datastore"]["password"]}@{parsed_conf["datastore"]["hostname"]}:{parsed_conf["datastore"]["port"]}/{parsed_conf["datastore"]["db"]}')
    Base.metadata.bind = DB_ENGINE
    DB_SESSION = sessionmaker(bind=DB_ENGINE)

def addScore(body):
    """ Receives a score """
    logger.info(f'Stored event addScore request received with a trace id of {body["trans_id"]}')
    session = DB_SESSION()
     
    #Might have to add back ids here, and redo yaml file possible
    score = GameScore(
        body['trans_id'],
        body['score_id'],
        body['date'],
        body['runTime'],
        body['score'],
        body['userName'],
    )
    
    session.add(score)
    session.commit()
    session.close()
    logger.debug(f'Stored Event: addscore id {body["trans_id"]} with status code 201')
    
    return NoContent, 201                        

def add_user(body):
    """ Receives a user """
    
    logger.info(f'Stored event add_user request received with a trace id: {body["trans_id"]}')
    session = DB_SESSION()
    user = User(
        body['trans_id'],
        body['user_id'],
        body['email'],
        body['name'],
        body['password'],
        body['phoneNumber'],
        body['timeStamp']
    )
    session.add(user)
    session.commit()
    session.close()
    logger.debug(f'Stored event: add_user with trace id: {body["trans_id"]} with status code 201')
    logger.info('Connecting to DB. Hostname: pg-acit3855-kafka.eastus.cloudapp.azure.com, Port: 3306')
    return NoContent, 201

def get_score(timestamp):
    """ Gets new game score after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    scores = session.query(GameScore).filter(GameScore.date >= timestamp_datetime)
    result_list = []

    for i in scores:
        result_list.append(i.to_dict())

    session.close()

    logger.info("Query for Game Score scores after %s returns %d results" %(timestamp, len(result_list)))

    return result_list, 200

def get_user(timestamp):
    """ Gets new users added after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    scores = session.query(User).filter(User.timeStamp >= timestamp_datetime)
    test = session.query(User)
    print(test)
    result_list = []

    for i in scores:
        result_list.append(i.to_dict())

    session.close()

    logger.info("Query for users added after %s returns %d results" %(timestamp, len(result_list)))

    return result_list, 200

def process_messages():
    
    logger.info("logging started")
    hostname = "%s:%d" % (parsed_conf["events"]["hostname"], parsed_conf["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(parsed_conf["events"]["topic"])]

    # read all the old messages formt he history in the message que
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]
        if msg["type"] == "addScore":
            addScore(payload)
            logger.info('payload stored. msg type: %s, trace id: %s' % (msg["type"], payload["trans_id"]))
        
        elif msg["type"] == "add_user":
            add_user(payload)
            logger.info('payload stored. msg type: %s, trace id: %s' % (msg["type"], payload["trans_id"]))
        else:
            logger.info(msg["type"])
        
        consumer.commit_offsets()
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("BCIT37-game-score-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)