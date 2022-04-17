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
from django.contrib.auth.models import User
from django.utils import timezone

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


def clear_team():
    Teams.objects.all().delete()

def create_team(row):
    row = dict(row)
    contnt_lis = []
    try:
        for cords in map(str, str(row["contestants"] ).split(',')):
            cords = cords.strip()
            c = Contestants.objects.all().filter(contact_number = int(cords))
            if c.exists():
                contnt_lis.append(c.first().id)
    except:
        traceback.print_exc()
        print("nan")

    payload = {
        "t_name" : row.get("t_name"),
        
    }


    try :
        event = Events.objects.all().filter(id = row.get("event") )
        if(event.exists()):
            payload["event"] = event.first()
        res = Teams(**payload)
        res.save()
        res.contestants.add(*contnt_lis)
        print("Team created - ", payload["t_name"])
        res.save()
    except:
        print("error")
    # logger.info("{} res created.".format(res))
    return res


def create_events(row):
    row = dict(row)
    # logger.info("Creating Contestants")
    cords_lis = []
    try:
        for cords in map(str, str(row["co_ord"] ).split(',')):
            c = User.objects.all().filter(username = cords)
            if c.exists():
                cords_lis.append(c.first().id)
    except:
        traceback.print_exc()
        print("nan")

    payload = {
        "e_name" : row.get("e_name"),
        "e_desc" : row.get("e_desc"),
        "type" : row.get("type"),
        "e_time" : str(timezone.now()),
        "status" : row.get("status"),
        "id" : row.get("id"),
        "code" : row.get("code")
    }
 
    res = Events(**payload)
    res.save()
    print("Events Added -  ", payload["e_name"])
    res.save()

    # logger.info("{} res created.".format(res))
    return res


 

def clear_data_contestants():
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
    print("  Contestant added -- ",payload["name"])
    res.events.add(*event_lis)
    res.save()

    # logger.info("{} res created.".format(res))
    return res

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Event Seeding

    r_path = os.path.join(settings.BASE_DIR,'static/events.csv')
    df = pd.read_csv(r_path)
    clear_data()
    if mode == MODE_CLEAR:
        return
    for index, row in df.iterrows():
        create_events(row)

    ##############################

    # Contestants Seeding 

    r_path = os.path.join(settings.BASE_DIR,'static/contestant.csv')

    df = pd.read_csv(r_path)
    
    clear_data_contestants()
    if mode == MODE_CLEAR:
        return
    for index, row in df.iterrows():
        create_contestants(row)

    #####################################
    
    # Team Seeding
    
    r_path = os.path.join(settings.BASE_DIR,'static/teams.csv')

    df= pd.read_csv(r_path)
    clear_team()
    if mode == MODE_CLEAR:
        return
    for index, row in df.iterrows():
        create_team(row)

    ################################