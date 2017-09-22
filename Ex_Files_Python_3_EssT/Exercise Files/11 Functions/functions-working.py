#!/usr/bin/python3
# functions.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
    testfunc(42)
    testfunc(22,66)
    testfunc(1,2,3)

def testfunc(number1, number2 = None, number3 = 9999):
    print('This is a test function', number1, number2, number3 )

# example of a dummy function
def mock(number, str):
    pass

if __name__ == "__main__": main()
