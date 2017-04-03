#!/usr/bin/env python3
# package: life
# all.py

import numpy
import pandas
from settings import *
from .extend import get_life_table
from .main import get_actuary_table

ltf, ltm = get_life_table()


def process():
    if gender == 'F':
        lt = ltf
    else:
        lt = ltm
    return get_actuary_table(lt)['Bx'][0]


def gen():
    global gender, age, p_class, pay

    gender = 'F'
    def reset():
        global death_compensate, survival_compensate
        if p_class == 'A':
            death_compensate = 200000
            survival_compensate = 50000
        elif p_class == 'B':
            death_compensate = 500000
            survival_compensate = 40000
        elif p_class == 'C':
            death_compensate = 1000000
            survival_compensate = 30000

    data = numpy.empty((23, 6))
    for age in range(18, 41):
        for i, p_class in enumerate(['A', 'B', 'C']):
            reset()
            for j, pay in enumerate([1, 10]):
                k = i * 3 + j
                data[age-18,k] = process()

    pandas.DataFrame(data, columns=['1A', '10A', '1B', '10B', '1C', '10C']).to_excel('F.xslx')
