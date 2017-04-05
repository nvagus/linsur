#!/usr/bin/env python3
# package vehicle
# price.py

import functools
import numpy
from settings import *


def gamma(e, var):
    theta = e / var
    alpha = e * theta
    return functools.partial(numpy.random.gamma, shape=alpha, scale=1/theta)


def random01():
    return numpy.random.random()


def get_price_array():
    price1 = numpy.empty(size)
    price2 = numpy.empty(size)
    price3 = numpy.empty(size)
    human_injure_model = gamma(human_injure_exp, human_injure_var)
    pet_injure_model = gamma(pet_injure_exp, pet_injure_var)
    other_items_model = gamma(other_items_exp, other_items_var)

    for i in range(size):
        response = random01()
        if response < .1:
            response = 1
            nopay = .15
        elif response < .4:
            response = .7
            nopay = .08
        elif response < .6:
            response = .5
            nopay = .05
        elif response < .9:
            response = .3
            nopay = .03
        else:
            response = 0
            nopay = .00

        _price = numpy.array([0., 0., 0.])

        for _ in range(seat_num):
            if random01() < seat_loss:
                if random01() < ispet:
                    # ispet
                    if random01() < pet_loss_rate:
                        # dead pet
                        _price[2] += pet_loss
                    else:
                        _price[2] += pet_injure_model()
                else:
                    # ishuman
                    if random01() < human_loss_rate:
                        # disable human
                        _price[0] += human_loss
                    else:
                        _price[1] += human_injure_model()
            if random01() < seat_occupy:
                break
        _price *= response
        if response > 0.9:
            _price[0] = max(_price[0] - 11000, 0)
            _price[1] = max(_price[1] - 1000, 0)
            _price[2] = max(_price[2] - max(100 - other_items_model(), 0), 0)
        else:
            _price[0] = max(_price[0] - 110000, 0)
            _price[1] = max(_price[1] - 10000, 0)
            _price[2] = max(_price[2] - max(2000 - other_items_model(), 0), 0)
        _price *= (1 - nopay)
        price1[i] = min(_price[0], 200000)
        price2[i] = min(_price[1], 20000)
        price3[i] = min(_price[2], 2000)

    return price1, price2, price3



if __name__ == '__main__':
    print(get_price_array())
