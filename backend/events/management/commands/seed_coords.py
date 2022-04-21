from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
import os
import traceback
from events.models import *
from contestants.models import *
from django.utils import timezone


COORD_URL ="https://docs.google.com/spreadsheets/d/1hUdUKn02jh0OcIG_6FQshchYPs4SkrNgG3sxr-H4fyk/edit#gid=1700464238".replace('/edit#gid=', '/export?format=csv&gid=')


def clear_coord():
    Coordinators.objects.all().filter(is_superuser = False).delete()

def create_coords(row):
    row = dict(row)
    events = []
    try:
        ev_list = row.get("events_coordinating", "").split(',')
        for event  in ev_list:
            ev = event.split('-')[0].strip()
            ev = get_object_or_404(Events, code = ev)
            events.append(ev)
    except :
        print("event not found")
    
    

    payload = {
        "username" : str(row.get("contact_number")).replace(" ", "")[-10:],
        'first_name' : row.get("name"),
        'email' : row.get("email"),
        'gender' : row.get("gender"),
        'branch' : row.get("branch"),
        'year' : row.get("year"),
        "contact_number" : str(row.get("contact_number")).replace(" ", "")[-10:],

    }
    user = Coordinators.objects.update_or_create(**payload)
    user = user[0]
    user.set_password(payload["username"])
    user.save()
    for event in events:
        event.co_ord.add(user)
    print("Coordinator created - ", payload["username"])
    return user

""" Coordinates seed"""
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")
    def _create_tags(self, mode):
        r_path = os.path.join(settings.BASE_DIR,'static/coordinators.csv')
        df = pd.read_csv(COORD_URL)
        if mode == "clear":
            print("clear command executed")
            clear_coord()
        for index, row in df.iterrows():
            create_coords(row)
    

    def handle(self, *args, **options):
        mode = options.get("mode", "refresh")
        self._create_tags(mode)