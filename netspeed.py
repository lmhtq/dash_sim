import os
import sys
import random
import math

def netspeed():
    mu = 100*1000
    sigma = 1
    return random.gauss(mu, sigma)
