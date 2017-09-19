#!/usr/bin/python3
# ops.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
    print("This is the ops.py file.")

    l = []
    # initialize the list container with 0 - 100
    l[:] = range(100)
    # slice it
    for n in l[20:40]:
        print("{} ".format(n), end="")
    print()
    # slice it with a step over
    for n in l[20:40:3]:
        print("{} ".format(n), end="")
    try:
    # assing to the slices
        l[20:40:3] = 99,99,99,99,99,99,99
        for n in l:
            print("{} ".format(n), end="")
    except:
        print('')
        print('Too many slices to be replaced.')



if __name__ == "__main__": main()
