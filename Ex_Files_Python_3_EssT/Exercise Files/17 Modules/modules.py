#!/usr/bin/python3
# modules.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

import sys

def main():
    print('Python version {}.{}.{}'.format(*sys.version_info))

    myList = [1,7,2,6,0,5]
    listLength = len(myList) - 1
    # while True;

    for item in myList:
        thisItem = item
        nextItem = myList[myList.index(item) - listLength]
        print (myList[nextItem])

if __name__ == "__main__": main()
