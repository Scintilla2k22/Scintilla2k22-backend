from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
import os
import traceback
from events.models import *
from contestants.models import *
from django.utils import timezone


CONT_URL = "https://docs.google.com/spreadsheets/d/1F2mos7YdqW8FqUl0HqULTi24sUPoPo-zlQJImQiwLgM/edit#gid=74408774".replace('/edit#gid=', '/export?format=csv&gid=')



def clear_data_contestants():
    """Deletes all the table data"""
    # logger.info("Delete contestants instances")
    Contestants.objects.all().delete()



def create_contestants(row):
    row = dict(row)
    # logger.info("Creating Contestants")
    event_lis = []
    event_obj_lis = []
    try:
        ev_list = row.get("events_participating", "").split(',')
        for event  in ev_list:
            ev = event.split('-')[0].strip()
            ev = Events.objects.all().filter(code = ev)
            if ev.exists():
                event_lis.append(ev.first().id)
                event_obj_lis.append(ev.first())
    except :
        traceback.print_exc()
    # try:
    #     for events in map(str, row["events"].strip().split(',')):
    #         events = events.strip()
    #         c = Events.objects.all().filter(e_name = events)
    #         if c.exists():
    #             event_obj_lis.append(c.first())
    #             event_lis.append(c.first().id)
    # except:
    #     traceback.print_exc()
    #     print("nan")

    payload = {
        "name" : row.get("name"),
        "branch" : row.get("branch"),
        "year" : row.get("year"),
        "contact_number" : row.get("contact_number").replace(" ", "")[-10:],
    }
     
    res = Contestants.objects.get_or_create(contact_number = payload["contact_number"])
    # print(res)

    if res:
        res = res[0]
        res.name = payload["name"]
        res.branch = payload["branch"]
        res.year = payload["year"]
        res.save()
        print("  Contestant added -- ",payload["name"])
        res.events.add(*event_lis)
        res.save()

    # for ev in event_obj_lis:
    #     sc = Score(participants = res, score = 1, event = ev)
    #     sc.save()
    # logger.info("{} res created.".format(res))
    return res




""" Coordinates seed"""
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def _create_tags(self, mode):
        # r_path = os.path.join(settings.BASE_DIR,'static/contestants.csv')
        df = pd.read_csv(CONT_URL)
        if mode == "clear":
            print("clear command executed")
            clear_data_contestants()
            
        for index, row in df.iterrows():
            create_contestants(row)

    def handle(self, *args, **options):
        mode = options.get("mode", "refresh")
        self._create_tags(mode)