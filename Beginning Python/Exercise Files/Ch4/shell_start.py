#
# Example file for working with filesystem shell methods
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)
import os
import shutil
from zipfile import ZipFile
from os import path
from shutil import make_archive

def main():
    if path.exists("textfile.txt"):
    # get the path to the file in the current directory
        src = path.realpath("textfile.txt");   
        head, tail = path.split(src)   
        
        print "path: " + head
        print "file: " + tail
        #create the bkup name
        bk = src + ".bkup"
        print bk
        # now copy the file 
        shutil.copy(src,bk)
        # copy over the permissions, modification times, and other info
        shutil.copystat(src,bk)
        # rename a file
        os.rename(bk, "newfile.txt")
        
        #now lets create a zip file
        root_dir, fn = path.split(src)
        
        # determine what archives are available
        print shutil.get_archive_formats()
        shutil.make_archive("myarchive", 'zip',root_dir)
        
         # more fine-grained control over ZIP files
        with ZipFile("testzip.zip","w") as newzip:
          newzip.write("newfile.txt")
          newzip.write("textfile.txt")
        
if __name__ == "__main__":
  main()
