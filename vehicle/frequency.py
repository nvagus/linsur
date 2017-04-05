#!/usr/bin/env python3
# package vehicle
# frequency.py


import functools
import numpy
from settings import *


def negative_binomial(e, var):
    p = e / var
    assert 0 <= p <= 1
    n = e * p / (1 - p)
    return functools.partial(numpy.random.negative_binomial, n=n, p=p)


def get_frequency_model():
    model = negative_binomial(frequency_model_exp, frequency_model_var)
    sequence = numpy.round(model(size=scale)).astype(numpy.int64)
    return sequence

