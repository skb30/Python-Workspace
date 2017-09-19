#!/usr/bin/python3
# conditionals.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():

    a, b = 1,2
    if a < b:
        print("a is less than b.")
    elif a > b:
        print("a is greater than b")
    else:
        print("a and b are equal")


    print("a is greater than b") if a > b else print("a is less than b")

if __name__ == "__main__": main()
