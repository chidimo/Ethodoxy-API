from django.core.management.base import BaseCommand#, CommandError

import os
import json
import glob

import django
from django.conf import settings

BASE_DIR = settings.BASE_DIR
SAVE_PATH = os.path.join(BASE_DIR, "drbo_org_scrap")
DATA_STORE = os.path.join(BASE_DIR, "drbo_data")
CHAPTER_STORE = os.path.join(BASE_DIR, "drbo_data", "chapters")
VERSE_STORE = os.path.join(BASE_DIR, "drbo_data", "verses")
CHALLONER_STORE = os.path.join(BASE_DIR, "drbo_data", "challoner")

NT = (os.path.join(DATA_STORE, "new_test.json"))
OT = (os.path.join(DATA_STORE, "old_test.json"))
CHAPS = glob.glob("{}/*.json".format(CHAPTER_STORE))
VERSES = glob.glob("{}/*.json".format(VERSE_STORE))
COMMENTARIES = glob.glob("{}/*.json".format(CHALLONER_STORE))
