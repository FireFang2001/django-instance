import random
import time


def get_ticket():

    ticket = ''
    s = '0123456789abcdefghijklmnopqrstuvwxyz'
    for i in range(15):
        ticket += random.choice(s)
    ticket = 'TK' + ticket + str(int(time.time()))
    return ticket
