#!/usr/bin/python3
class inclusive_range:

    # pass a list of arguments
    # clean the data
    def __init__(self, *args):
        numArgs = len(args)
        if numArgs < 1:
            raise TypeError("Must supply at least one argument")
        if numArgs == 1:
            self._stop = args[0]
            self._start = 1
            self._step  = 1
        elif numArgs == 2:
            (self._start, self._stop) = args
            self._step = 1
        elif numArgs == 3:
            (self._start, self._stop, self._step) = args
        else:
            raise TypeError("Too many arguments. Takes start, stop and skip")

    # this method causes the object to become an iterator
    def __iter__(self):

        while (self._start <= self._stop):
            yield self._start
            self._start += self._step
def main():
    try:
        # o = inclusive_range(0,1000,25)

        for i in inclusive_range(1,25):
            print(i,end=" ")
    except TypeError as e:
        print(e)
        return
if __name__ == "__main__": main()
