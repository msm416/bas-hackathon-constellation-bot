#!pip install opencv-python
#!apt update && apt install -y libsm6 libxext6
#!apt-get install -y libxrender-dev

from apscheduler.schedulers.blocking import BlockingScheduler
from main import generateAndPost

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    generateAndPost()
    print('This job is run every 3 minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
