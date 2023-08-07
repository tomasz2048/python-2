import logging
import requests

from pytz import utc
from datetime import datetime
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler


# volatile scheduler blocking - does not need any other thread to continue running
# job gets defined in the code, no persistence

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 3
}

scheduler = BlockingScheduler(executors=executors,
                              job_defaults=job_defaults,
                              timezone=utc,
                              daemon=True)


def task():
    print('Tick! The time is: %s' % datetime.now())
    print(requests.get("http://127.0.0.1:5000").text)


scheduler.add_job(task, id="job_id_2", name="job name 2", trigger='interval', seconds=5, misfire_grace_time=600,
                  max_instances=1, coalesce=True)

scheduler.start()
