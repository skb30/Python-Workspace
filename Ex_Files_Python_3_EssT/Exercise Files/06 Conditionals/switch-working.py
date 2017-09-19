#!/usr/bin/python3
# switch.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
    print('this is the switch.py file')

    d = dict(
        one = 'first',
        two = 'second',
        three = 'third'
    )
    v = 'one'
    print(d.get(v, "other"))

if __name__ == "__main__": main()
