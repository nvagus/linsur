#!/usr/bin/env python3
# package vehicle
# main.py

import numpy
from .frequency import get_frequency_model
from .price import get_price_array
from settings import *


def get_insurance_price():
    f = get_frequency_model()
    p1, p2, p3 = get_price_array()
    with open('sheet/model', 'w') as file:
        numpy.set_printoptions(threshold=numpy.nan)
        file.write(str(f))
        file.write(str(p1))
        file.write(str(p2))
        file.write(str(p3))
    h = sum(f)
    assert h < size
    x = sum((p1 + p2 + p3)[:h]) / scale
    return x / 3.3616

if __name__ == '__main__':
    print(get_insurance_price())
