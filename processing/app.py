from email import header
from time import strftime
from unittest import result
import connexion
from connexion import NoContent
from flask import session
import os
from os import path
import yaml
import sqlite3
from sqlalchemy import create_engine, null
from sqlalchemy.orm import sessionmaker
from base import Base
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import logging.config
from datetime import datetime
import datetime
import requests
import uuid
from stats import Stats
from flask_cors import CORS, cross_origin

logger = logging.getLogger('basicLogger')
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open("app_conf.yml", 'r') as f:
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def create_tables():

    conn = sqlite3.connect('stats.sqlite')

    c = conn.cursor()
    c.execute('''
        CREATE TABLE stats
        (
            id INTEGER PRIMARY KEY ASC,
            num_scores INTEGER NOT NULL,
            top_score INTEGER NOT NULL,
            low_score INTEGER NOT NULL,
            longest_run Varchar(100) NOT NULL,
            shortest_run VARCHAR(100) NOT NULL,
            num_users INTEGER NOT NULL, 
            last_updated Varchar(100) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
if not path.exists(app_config["datastore"]["filename"]):
    create_tables()
    print('created db')

def populate_stats():
    logger.info('Start Periodic Processing')
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    time = str(time)
    id = str(uuid.uuid4())
    session = DB_SESSION()

    query = get_time()
    last_update = query[-1]
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    current_timestamp = str(current_timestamp)
    print(f'last updated @ {last_update}')
    print(f'current timestamp: {current_timestamp}')

    # Get score and user data
    headers = {"content-type": "application/json"}
    score_request = requests.get(app_config['eventstore']['url']+last_update+"&end_timestamp="+current_timestamp, headers=headers)
    user_request = requests.get(app_config['eventstore2']['url']+last_update+"&end_timestamp="+current_timestamp, headers=headers)
    score_data = score_request.json()
    user_data = user_request.json()
    print(f'score_data: {score_data}')
    if len(score_data) == 0 and len(user_data) == 0:
        return null
    num_scores = 0
    top_score = 0
    low_score = 0
    longest_run = 0
    shortest_run = 0
    num_users = 0
    count = 0

    # Forloop for score data
    for i in score_data:
        num_scores += 1
        #logger.info(f'processing event with trans_id: {i["trans_id"]}')
        if top_score < i["score"]:
            top_score = i["score"]
        else:
            low_score = i["score"]
        runTime = i["runTime"]
        runTime = runTime.replace(":", ".")
        runTime = float(runTime)
        if longest_run < runTime:
            longest_run = runTime
        else: 
            shortest_run = runTime
        count += 1
    # Forloop for user data
    for i in user_data:
        num_users += 1
    scores_received = score_request.json()
    users_received = user_request.json()
    if score_request.status_code != 200:
        logger.error(f'bad request with status code: {score_request.status_code}')
    if user_request.status_code != 200:
        logger.error(f'Did not get response from user request')
    else:
        logger.info(f'received {num_users} of requests with status code: {score_request.status_code}')
    logger.info(f'received {len(scores_received)} score responses')
    logger.info(f'received {len(users_received)} user responses')
    # if no request received
    

    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    last_update = str(current_timestamp)
    print(f'Top score: {top_score}, longest run: {longest_run}')
    stats = Stats(
        num_scores,
        top_score,
        low_score,
        longest_run,
        shortest_run,
        num_users,
        last_updated
    )
    session.add(stats)
    session.commit()
    session.close()

    # Log debug message with updated stat values 
    logger.debug(f'Stored event: populate stats with trace id: {id} with status code 201')
    

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_stats,
        'interval',
        seconds=app_config['scheduler']['period_sec']
    )
    sched.start()


def get_stats():
    """ Returns a list of values """
    session = DB_SESSION()
    stats = session.query(Stats)
    result_list = []

    for i in stats:
        result_list.append(i.to_dict())
    latest = result_list[len(result_list)-1]
    print(f'the # of indexes: {len(result_list)}')
    stat_dict = {
        'num_scores': latest['num_scores'], 
        'top_score': latest['top_score'], 
        'low_score': latest['low_score'], 
        'longest_run': latest['longest_run'], 
        'shortest_run': latest['shortest_run'], 
        'num_users': latest['num_users'], 
        'last_updated': latest['last_updated']
    }
    logger.debug(stat_dict)
    logger.info('get stats completed')
    session.close()
    return stat_dict, 200
    
def get_time():

    con = sqlite3.connect('stats.sqlite')
    cur = con.cursor()
    last_row = cur.execute('select * from stats').fetchall()[-1]
    row = []
    for i in last_row:
        row.append(i)

    return row
app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("BCIT37-BCIT_Stats-1.0.0-swagger.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)