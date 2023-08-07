import time
import logging
import requests

from pytz import utc
from datetime import datetime
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# persistent scheduler, non-blocking
# it needs process to run continuously for some other reason -  it will terminate otherwise
# that's why it has wile-true-sleep10 loop at the end


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores,
                                executors=executors,
                                job_defaults=job_defaults,
                                timezone=utc,
                                daemon=True)


def task():
    print('Tick! The time is: %s' % datetime.now())
    print(requests.get("http://127.0.0.1:5000").text)


scheduler.add_job(task, id="job_id_1", name="job name 1", trigger='interval', seconds=5, misfire_grace_time=600, max_instances=1, coalesce=False)

scheduler.print_jobs(jobstore="default")

scheduler.start()
while True:
    time.sleep(10)
