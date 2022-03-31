from datetime import date, datetime
import connexion
from connexion import NoContent
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging.config
import yaml
from base import Base
from stats import Stats
from uuid import uuid1
from apscheduler.schedulers.background import BackgroundScheduler

DB_ENGINE = create_engine("sqlite:///stats.sqlite")
Base.metadata.bind = DB_ENGINE 
DB_SESSION = sessionmaker(bind=DB_ENGINE)



with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

def populate_stats():
    """perodically update stats"""
    logger.info("Start Periodic Processing")
    session = DB_SESSION()
    result = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    results = result.to_dict()
    session.close()
    trace_id = str(uuid1())
    current_time = datetime.now()
    rapid_test = requests.get(app_config["eventstore"]['url1'], params={'timestamp': results['last_updated']})
    user_data = requests.get(app_config['eventstore']['url2'], params={'timestamp': results['last_updated']})
    rapid_test_obj = rapid_test.json()
    print(f"\n\nrapid test {rapid_test_obj}")
    user_data_obj = user_data.json()
    print(f"\n\nuser data {user_data_obj}")
    num_tests_results = len(rapid_test_obj) + results["num_tests_results"]
    num_users = len(user_data_obj) + results["num_users"]
    age_list =[]
    positive_tests = [test['personal_health_number'] for test in rapid_test_obj if test['rapid_test_result'] == 'yes']
    num_positive_test = len(positive_tests) + results["num_positive_tests"]
    negative_tests = [test['personal_health_number'] for test in rapid_test_obj if test['rapid_test_result'] == 'no']
    num_negative_test = len(negative_tests) + results["num_negative_tests"]
    print(positive_tests)
    for test in positive_tests:
        for user in user_data_obj:
            print(test)
            print(user['personal_health_number'])
            print(test == user['personal_health_number'])
            if test == user['personal_health_number']:
                age_list.append(user['age'])
    
    print(f"\n\n{age_list}\n\n")
    try:
        highest_positive_occuring_age = sorted(age_list)[-1]
        print(f"\n\n{highest_positive_occuring_age}\n\n")
    except:
        print("oh no i broke")
    total_requests = num_tests_results + num_users
    logger.info(f'number of events received {total_requests}')
    if rapid_test.status_code == 500:
        logger.error(f'something went wrong 500 error code')
    logger.debug(f'Total number of tests: {num_tests_results}. TraceID: {trace_id}')
    logger.debug(f'Total number of users: {num_users}. TraceID: {trace_id}')
    logger.debug(f'Total number of positive tests: {num_positive_test}. . TraceID: {trace_id}')
    logger.debug(f'Total number of negative tests: {num_negative_test}. TraceID: {trace_id}')
    logger.debug(f'Age group with the most positive cases{highest_positive_occuring_age}. TraceID: {trace_id}')

    session = DB_SESSION()
    stat = Stats(num_tests_results, num_users, num_positive_test, num_negative_test, highest_positive_occuring_age, current_time)
    """    stats = Stats(stats["num_tests_results"],
                stats["num_users"],
                stats["num_positive_tests"],
                stats["num_negative_tests"],
                stats["highest_positive_occuring_age"],
                datetime.strptime(stats["last_updated"], "%Y-%m-%d %H:%M:%S.%f"))"""
    session.add(stat)
    session.commit()
    session.close()

    logger.debug(f'number of test results: {num_tests_results}, number of users: {num_users}, number of positive tests: {num_positive_test}, number of negative tests: {num_negative_test}, Age with the most positive cases: {highest_positive_occuring_age}')
    logger.info(f'stat processing has been completed.')
    return NoContent, 201

def get_stats():
    logger.info('request has started')
    try:
        session = DB_SESSION()
        result = session.query(Stats).order_by(Stats.last_updated.desc()).first()
        session.close()
        result = result.to_dict()
        logger.debug(f'current stats: {result}')
        logger.info(f'request complete')
        return result, 200
    except:
        logger.error(f'Statistics do not exist')


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) 
 
if __name__ == "__main__": 
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)