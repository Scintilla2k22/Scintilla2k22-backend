from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
import os
import traceback
from events.models import *
from contestants.models import *
from django.utils import timezone




def clear_events():
    Events.objects.all().delete()

def create_events(row):
    row = dict(row)
    cords_lis = []
    try:
        for cords in map(str, str(row["co_ord"] ).split(',')):
            c = Coordinators.objects.all().filter(username = cords)
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


""" Coordinates seed"""
class Command(BaseCommand):

    def _create_tags(self):
        r_path = os.path.join(settings.BASE_DIR,'static/events.csv')
        df = pd.read_csv(r_path)
        # clear_events()
        for index, row in df.iterrows():
            create_events(row)

    def handle(self, *args, **options):
        self._create_tags()