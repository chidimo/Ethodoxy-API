from django.core.management.base import BaseCommand#, CommandError

import os
import json
import glob

import django
from django.conf import settings

BASE_DIR = os.path.join(settings.BASE_DIR, 'drbo')
SAVE_PATH = os.path.join(BASE_DIR, 'text')
DATA_STORE = os.path.join(BASE_DIR, 'json')
CHAPTER_STORE = os.path.join(DATA_STORE, 'chapters')
VERSE_STORE = os.path.join(DATA_STORE, 'verses')
CHALLONER_STORE = os.path.join(DATA_STORE, 'challoner')

NT = (os.path.join(DATA_STORE, 'new_test.json'))
OT = (os.path.join(DATA_STORE, 'old_test.json'))
CHAPS = glob.glob(f'{CHAPTER_STORE}/*.json')
VERSES = glob.glob(f'{VERSE_STORE}/*.json')
COMMENTARIES = glob.glob(f'{CHALLONER_STORE}/*.json')
