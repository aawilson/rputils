# -*- coding: utf-8 -*-
# This library is for parsing dice notation. It is mostly based on the notation given at
# http://en.wikipedia.org/wiki/Dice_notation.
# This will accept '×'' for "multiply end result X times", but it is usually easier to use *
# 'x' will mean "perform combination X times"

# Accepts "standard" notation

# Accepts these alternative notations
# XzY for "zero-bias" notation (0-X rather than 1-X)
# XdF for "fudge" notation (alternatively, XdF.1 or XdF.2, for 1+,1-,4blank and 2+,2-,2blank respectively. Default is .2)
# XhY as standard, but only take highest
# XlY as standard, but only take lowest
# XiY as standard, but drop lowest
# Xd% for percentage, equivalent to Xd100

# Accepts these addenda for standard and zero-bias:
#  eX -- successes of X or greater
#  rX -- successes of X or greater, with die max re-rolled and added to same die (leave out X to just get highest result)
#  fX -- successes of X or greater, minus 1s
#  mX -- successes of X or greater, with die max re-rolled to see if it adds another success

import random
import re

DICE_REGEX = re.compile(r'(?:(\d+)?([dxhli%]|dF)(\d+)(?:([erfmF])(\d+))?(\+\-\d+)?)+')


class roll_factory(object):
    def __init__(self, roll_func, roll_qualifier):

        def func():
            return roll_func(roll_qualifier)

        self.func = func

    def __call__(self):
        return self.func()

    def roll(self):
        return self.func()



class rolls(list):
    def __init__(self, otherlist=None, resultfunc=sum):
        self.resultfunc = resultfunc
        super(rolls, self).__init__(otherlist)
        self.cached = None

    def result(self):
        if not self.cached:
            self.cached = [x.roll() for x in self]

        return self.resultfunc(self.cached)

    # alias roll
    roll = result

    def reroll(self):
        self.cached = None
        return self.result()


def success_result_factory(threshold):
    if not threshold:
        def newfunc(lst):
            return max(a.roll() for a in lst)
        return newfunc


def standard(y):
    return random.randint(1, y)


def zerobias(y):
    return random.randint(0, y)


def fudge(y):
    if y == ".1":
        rand = random.randint(1, 6)
        if rand == 1:
            return -1
        elif rand == 2:
            return 1
        else:
            return 0
    if y == ".2":
        return random.randint(-1, 1)

def d(x, y):
    return rolls([roll_factory(standard, y) for i in range(x)])


def z(x, y):
    return rolls([roll_factory(zerobias, y) for i in range(x)])


def dF(x=4, y=".2"):
    return rolls([roll_factory(fudge, y) for i in range(x)])


if __name__ == '__main__':

    print [standard(6) for x in range(20)]

    print [zerobias(5) for x in range(20)]

    print [d(3, 6).roll() for x in range(20)]

    print [z(3, 5).roll() for x in range(20)]

    # standard notation
    "d6"
    "1d6"
    "1d1"
    "1d200"
    "2d6"
    "2d6 + 2"
    "3 * 2d6"
    "3 x 2d6"
    "2d6 + 3 + 2d5 + 6"
    "2 x (2d6 + 1)"

    # zero-bias notation
    "z6"
    "1z6"
    "1z1"
    "1z200"
    "2z6"
    "2z6 + 2"
    "3 * 2z6"
    "3 x 2z6"
    "2z6 + 3 + 2z5 + 6"
    "2 x (2z6 + 1)"

    # Fudge notation
    "3dF"
    "dF"  # Equivalent to 4dF
    "3dF.2"  # Equivalent to 3dF
    "dF.2"
    "3dF.1"  # Like F, but 1 positive, 1 negative, 4 blanks
    "dF.1"

