#!/usr/bin/python3
# iterators.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
    fh = open('lines.txt')
    for line in fh.readlines():
        print(line, end="")


    s = "This is a string"

    for i, c in enumerate(s):

        if c == 's':
            print("index {} of {}".format(i,c))


if __name__ == "__main__": main()
