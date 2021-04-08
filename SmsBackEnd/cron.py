import datetime
from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.core import management


import os
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = datetime.datetime.now()   # a unique code

    def __init__(self):
        directory = settings.DBBACKUP_STORAGE_OPTIONS['location']
        if not os.path.exists(directory):
            os.makedirs(directory)

    def do(self):
        management.call_command('dbbackup')
        management.call_command('mediabackup')
        # pass    # do your thing here

class MyCronJobAtTime(CronJobBase):
    RUN_AT_TIMES = ['08:00']     
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'SmsBackEnd.MyCronJobAtTime'

    def __init__(self):
        directory = settings.DBBACKUP_STORAGE_OPTIONS['location']
        if not os.path.exists(directory):
            os.makedirs(directory)

    def do(self):
        management.call_command('dbbackup')
        management.call_command('mediabackup')


def my_scchuled_job_dbbackup(): 
    f = open("/Users/athiphat/backup/demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()
    print("Before run dbbackup ===> ")
    management.call_command('dbbackup')
    print("After run dbbackup ===> ")
    return True
