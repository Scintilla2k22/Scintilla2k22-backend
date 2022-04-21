from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
import os
import traceback
from events.models import *
from contestants.models import *
from django.utils import timezone

MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'


cont_url = "https://docs.google.com/spreadsheets/d/1F2mos7YdqW8FqUl0HqULTi24sUPoPo-zlQJImQiwLgM/edit#gid=74408774".replace('/edit#gid=', '/export?format=csv&gid=')
team_url = "https://docs.google.com/spreadsheets/d/1_IKFc6MH-1ldSWTPH6oRXZMwvDfEhJG6oMsQbRNpz4U/edit#gid=1299875194".replace('/edit#gid=', '/export?format=csv&gid=')
coord_url ="https://docs.google.com/spreadsheets/d/1hUdUKn02jh0OcIG_6FQshchYPs4SkrNgG3sxr-H4fyk/edit#gid=1700464238".replace('/edit#gid=', '/export?format=csv&gid=')




class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def _create_tags(self, mode):
        call_command(f'seed_events', mode = mode)
        call_command('seed_coords', mode = mode)
        call_command('seed_contestants', mode = mode)
        call_command('seed_teams', mode = mode)
      
    def handle(self, *args, **options):
        mode = options.get("mode", "refresh")
        self._create_tags(mode)