#!/usr/bin/python3
# exceptions.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Gorup, LLC

def main():
    # fh = open('lines.txt')
    # strip off the line feed
    # for line in fh: print(line.strip())
    try:
        for line in readfile('lines.txt'):
            print(line.strip())
    except IOError as e:
        print('Cannot read file ', e)
    except ValueError as e:
        print('bad file name', e)

    #https: //docs.python.org /3/library/exceptions.html


def readfile(file):

    if file.endswith('.txt'):
        fh = open(file)
        # create a generator
        return fh.readlines()
    else:
        raise ValueError("Filename must end with .txt")


if __name__ == "__main__": main()
