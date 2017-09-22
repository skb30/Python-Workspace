#!/usr/bin/python3
# generator.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():

    for i in inclusive_range(0, 100, 5):
        print(i, end = ' ')

def inclusive_range(*args):
    numOfargs = len(args)
    if numOfargs < 1: raise TypeError('Need at least one argument')

    if numOfargs == 1:
        start = 0
        stop  = args[0]
        step  = 1
    elif numOfargs == 2:
        start = args[0]
        stop  = args[1]
        step  = 1
    elif numOfargs == 3:
        start = args[0]
        stop  = args[1]
        step  = args[2]
    else:
        raise TypeError("Too many arguemnts, inclusive_range only takes 3 arguments")


    while start <= stop:

        # yield is like return but instead of leaving the function
        # it continues after returning a value
        yield start
        start += step

if __name__ == "__main__": main()
