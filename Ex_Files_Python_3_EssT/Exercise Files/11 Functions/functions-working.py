#!/usr/bin/python3
# functions.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():

    # Example func return a range
    for i in testfunc():
        print(i, end=' ')

def testfunc():
    return range(25)
if __name__ == "__main__": main()
