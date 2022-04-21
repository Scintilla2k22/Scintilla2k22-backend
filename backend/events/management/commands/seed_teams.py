from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
import os
import traceback
from events.models import *
from contestants.models import *
from django.utils import timezone


TEAM_URL = "https://docs.google.com/spreadsheets/d/1_IKFc6MH-1ldSWTPH6oRXZMwvDfEhJG6oMsQbRNpz4U/edit#gid=1299875194".replace('/edit#gid=', '/export?format=csv&gid=')



def clear_team():
    Teams.objects.all().delete()


def create_team(row):
    row = dict(row)
    contnt_lis = []
    try:
        for cont in map(str, str(row["contestants"] ).split('#')):
            cont = cont.replace(" ", "")[-10:]
            if cont:
                c = Contestants.objects.all().filter(contact_number = cont)
                if c.exists():
                    contnt_lis.append(c.first().id)
    except:
        traceback.print_exc()
    try :
        payload = {"t_name" : row.get("t_name").strip()}
        event = Events.objects.all().filter(code = row.get("event").split('-')[0].strip() )
        if(event.exists()):
            payload["event"] = event.first()
        res = Teams.objects.get_or_create(t_name = payload["t_name"])
        if res:
            res = res[0]
            if payload.get("event", False):
                res.event = payload["event"]
            res.save()
            res.contestants.add(*contnt_lis)
            print("Team created - ", payload["t_name"])
            res.save()
    except:
        print("error")

    return res


""" Teams seeding"""
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def _create_tags(self, mode):
        # r_path = os.path.join(settings.BASE_DIR,'static/teams.csv')
        df= pd.read_csv(TEAM_URL)
        if mode == "clear":
            print("clear command  executed")
            clear_team()
        for index, row in df.iterrows():
            create_team(row)

    def handle(self, *args, **options):
        mode = options.get("mode", "refresh")
        self._create_tags(mode)