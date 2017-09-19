# 
# Example file for variables
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)

# Declare a variable and initialize it
f = 0;
print f


# Global vs. local variables in functions
def someFunction():
  global f
  f = "def"
  print f

someFunction()
print f 

del f
print f

