#!/usr/bin/python3
# variables.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():

    n = 10
    s = '''\
    This is the {} variables.py file.
    With lines 
    added to 
    the bottom 
    '''.format(n)


    print (s)

if __name__ == "__main__": main()
