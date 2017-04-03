#!/usr/bin/env python3
# project linsur
# settings.py

# life
# pricing
pir = .035
vir = .030
additional_rate = .17
# span
pay = 10
death = 15
survival = 10
_class = 'A'

if _class == 'A':
    death_compensate = 200000
    survival_compensate = 50000
elif _class == 'B':
    death_compensate = 500000
    survival_compensate = 40000
elif _class == 'C':
    death_compensate = 1000000
    survival_compensate = 30000
else:
    raise ValueError('Unknown Compensate Strategy')

p_class = _class

# client
age = 30
gender = 'F'

