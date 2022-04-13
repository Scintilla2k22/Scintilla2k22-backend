from multiprocessing import Event
from django.core.management.base import BaseCommand
from numpy import add
import pandas as pd
from pandas.io.sql import has_table
from contestants.models import *
from django.conf import settings
import os
import traceback
from events.models import Events

MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing "

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    # logger.info("Delete Restaurants instances")
    Contestants.objects.all().delete()


def create_contestants(row):
    row = dict(row)
    # logger.info("Creating Contestants")
    event_lis = []
    try:
        for events in map(str, row["events"].strip().split(',')):
            events = events.strip()
            c = Events.objects.all().filter(e_name = events)
            if c.exists():
                event_lis.append(c.first().id)
    except:
        traceback.print_exc()
        print("nan")

    payload = {
        "name" : row.get("name"),
        "branch" : row.get("branch"),
        "year" : row.get("year"),
        "contact_number" : row.get("contact_number"),
    }
 
    res = Contestants(**payload)
    res.save()
    print("-- ", event_lis)
    res.events.add(*event_lis)
    res.save()

    # logger.info("{} res created.".format(res))
    return res

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    r_path = os.path.join(settings.BASE_DIR,'static/contestant.csv')

    df = pd.read_csv(r_path)
    
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # print(df.head(10))

    for index, row in df.iterrows():
        create_contestants(row)