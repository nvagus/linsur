#!/usr/bin/env python3
# package: life
# extend.py

import os
import numpy
from scipy import log, exp
from scipy.integrate import quad
import pandas
import settings


def get_compensation(l: float, q: float) -> float:
    # with Balducci Assumption
    v = 1 / (1 + settings.vir)
    lnv = log(v)
    p = 1 - q
    return l * p * q * quad(lambda x: exp(lnv * x) / (p + q * x) ** 2, 0, 1)[0]


def extend(xlsx: str, sheet: str, column: str) -> pandas.DataFrame:
    xlsx = os.path.join('sheet', xlsx)
    df = pandas.read_excel(xlsx, sheet)
    age, qx = df['AGE'], df[column]
    apv = numpy.empty(len(age))
    lx = numpy.empty(len(age))
    dx = numpy.empty(len(age))
    ax = numpy.empty(len(age))
    pv = 1 / (1 + settings.pir)
    tpv = 1
    l = 1.
    for i in range(len(age)):
        apv[i] = tpv
        tpv *= pv
        lx[i] = l
        dx[i] = qx[i] * l
        l -= dx[i]
    for i, (l, q) in enumerate(zip(lx, qx)):
        ax[i] = get_compensation(l, q)
    ax *= apv
    ex = apv * lx
    data = numpy.vstack([age, lx, dx, 1 - qx, qx, apv, ax, ex]).T
    df = pandas.DataFrame(data, columns=['Age', 'lx', 'dx', 'px', 'qx', 'vx', 'ax', 'ex'])
    return df


_LIFE_TABLE_MALE = os.path.join('sheet', 'life_table_male.xlsx')
_LIFE_TABLE_FEMALE = os.path.join('sheet', 'life_table_female.xlsx')


def get_life_table() -> (pandas.DataFrame, pandas.DataFrame):
    return pandas.read_excel(_LIFE_TABLE_FEMALE), pandas.read_excel(_LIFE_TABLE_MALE)


if __name__ == '__main__':
    extend('CL.xlsx', 'CL(2010-2013)', 'CL3').to_excel(_LIFE_TABLE_MALE)
    extend('CL.xlsx', 'CL(2010-2013)', 'CL4').to_excel(_LIFE_TABLE_FEMALE)
