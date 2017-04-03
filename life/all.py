#!/usr/bin/env python3
# package: life
# all.py

import numpy
import pandas
from settings import *
from .extend import get_life_table

ltf, ltm = get_life_table()

ds = slice(age, age + death)
ls = slice(age + death, age + death + survival)
ps = slice(age, age + pay)


def get_contract_value(life_table: pandas.DataFrame) -> numpy.ndarray:
    a = numpy.empty(death + survival)
    a[:death] = death_compensate * life_table['ax'][ds] / life_table['ex'][age]
    a[death:] = survival_compensate * life_table['ex'][ls] / life_table['ex'][age]
    return a


def get_payment_value(life_table: pandas.DataFrame) -> numpy.ndarray:
    b = numpy.empty(death + survival)
    b[:pay] = life_table['ex'][ps]
    b[pay:] = 0
    return b


def get_actuary_table(life_table: pandas.DataFrame) -> pandas.DataFrame:
    a = get_contract_value(life_table)
    b = get_payment_value(life_table)
    unit_price = (1 + additional_rate) * numpy.sum(a) / numpy.sum(b)
    b *= unit_price
    ef = numpy.empty(death + survival)
    cv = numpy.empty(death + survival)
    for i in range(1, death + survival):
        ef[i-1] = numpy.sum(a[i:]) - numpy.sum(b[i:])
        cv[i-1] = numpy.sum(b[:i]) / (1 + additional_rate) - numpy.sum(a[:i])
    return pandas.DataFrame({
        'Age': life_table['Age'][age: age + death + survival],
        'Ax': a,
        'Bx': b,
        'cv': cv,
        'ef': ef
    })


def process():
    if gender == 'F':
        lt = ltf
    else:
        lt = ltm
    at = get_actuary_table(lt)
    return at['Bx'].data[0]


def gen():
    global gender, age, p_class, pay, ds, ls, ps

    gender = 'M'
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
                ds = slice(age, age + death)
                ls = slice(age + death, age + death + survival)
                ps = slice(age, age + pay)
                k = i * 2 + j
                data[age-18,k] = process()

    df = pandas.DataFrame(data, columns=['1A', '10A', '1B', '10B', '1C', '10C'])
    df.to_excel('sheet/M.xlsx')

gen()
