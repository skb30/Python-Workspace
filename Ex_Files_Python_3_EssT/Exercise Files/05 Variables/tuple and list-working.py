#!/usr/bin/python3
# variables.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC

def main():
   # tuple example (immutable)
   x = (1,2,3,4,5)
   print (id(x),type(x), x)
   for i in x:
       print(i)

   # list example
   x = [1,2,3,4,5]
   x.insert(2,100)
   x.append(50)
   print (id(x),type(x), x)
   for i in x:
       print(i)
if __name__ == "__main__": main()
