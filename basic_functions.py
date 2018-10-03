from random import randint, random
from math import floor, log

'''Basic functions used in all other classes.'''


# Throws a n-sided dice.
def d(n):
    return randint(n > 0, max(0, n))


def r(a):
    return random() > a


# Returns a number from 0 to length of list - 1,
# with probabilities equal to the numbers in the list.
def rand_list(cls, ints_list):
    dice = cls.d(sum(ints_list))
    count = 0
    while dice > 0:
        dice -= ints_list[count]
        count += 1
    return count


# Calculates the level of a Person instance.
def experience(xp, xp_floor, base=2):
    if xp < xp_floor:
        return 1
    else:
        return floor(log(xp // xp_floor, base)) + 1
