#!/usr/bin/env python3
# package: life
# all.py

from settings import *
from .extend import get_life_table
from .main import get_actuary_table

ltm, ltf = get_actuary_table()

def process():
    return get_actuary_table()
