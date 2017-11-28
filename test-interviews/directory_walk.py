#!/usr/bin/python3


def print_directory_contents(sPath):
    """
    This function takes the name of a directory
    and prints out the paths files within that
    directory as well as any files contained in
    contained directories.

    This function is similar to os.walk. Please don't
    use os.walk in your answer. 1We are interested in your
    ability to work with nested structures.
    """
    import os
    count = 0
    for f in os.listdir(sPath):
        path = os.path.join(sPath, f)
        if os.path.isdir(path):
            print_directory_contents(path)
        else: print(f)

        count +=1

    print("num of rec: {}".format(count))

def main():
    print_directory_contents("../Beginning Python")
if __name__ == "__main__":main()