#!/usr/bin/python3
# break.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
    s = 'this is a string'
    for c in s:
        if c == 's': continue
        print(c, end='')
    print()
    for c in s:
        if c == 's': break
        print(c, end='')
    print()
    for c in s:
        print(c, end='')
    else:
        print(" Else")

if __name__ == "__main__": main()
