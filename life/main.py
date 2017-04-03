#!/usr/bin/env python3
# package: life
# main.py

import numpy
import pandas
from .extend import get_life_table
from settings import *

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


def gen_actuary_table(life_table: pandas.DataFrame):
    get_actuary_table(life_table).to_excel('sheet/{}-{}-{}-{}.xlsx'.format(age, gender, pay, p_class))


if __name__ == '__main__':
    ltm, ltf = get_life_table()
    if gender == 'F':
        lt = ltf
    elif gender == 'M':
        lt = ltm
    else:
        raise ValueError('Unknown Gender {}'.format(gender))

    gen_actuary_table(lt)
