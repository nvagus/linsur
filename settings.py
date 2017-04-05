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
p_class = 'A'

if p_class == 'A':
    death_compensate = 200000
    survival_compensate = 50000
elif p_class == 'B':
    death_compensate = 500000
    survival_compensate = 40000
elif p_class == 'C':
    death_compensate = 1000000
    survival_compensate = 30000
else:
    raise ValueError('Unknown Compensate Strategy')

# client
age = 30
gender = 'F'


# vehicle
scale = 2000
size = 1000
frequency_model_exp = .33
frequency_model_var = .66
human_injure_exp = 5000
human_injure_var = 2400
pet_injure_exp = 500
pet_injure_var = 300
other_items_exp = 500
other_items_var = 1000
human_loss_rate = .1
pet_loss_rate = .28
human_loss = 200000
pet_loss = 2000
ispet = .1
seat_num = 5
seat_occupy = .8
seat_loss = .7
