#!/usr/bin/python3
# regex.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Gorup, LLC

import re

def main():
    fh = open('raven.txt')
    for line in fh:
        match = re.search('(Len|Neverm)ore', line)
        # use the match object to print the match
        if match:
            print(match.group())


    # example of reg sub

    print("Example of regular expression w/ subsitution")
    fh.close()
    fh = open('raven.txt')
    # for line in fh:
    #     print(re.sub('(Len|Neverm)ore',"###", line), end='')

    # for line in fh:
    #     match = re.search('(Len|Neverm)ore', line)
    #     # use the match object to print the match
    #     if match:
    #         print(re.sub(match.group(), '###', line), end='')

    # example using pre-compile expression
    fh.close()
    fh = open('raven.txt')
    pattern = re.compile('(Len|Neverm)ore', re.IGNORECASE)

    for line in fh:
        if re.search(pattern, line):
            print(pattern.sub('###', line), end='')





if __name__ == "__main__": main()
