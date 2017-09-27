#!/usr/bin/python3


class Duck ():
    def quack(self):
        print('Quaaack!')

    def walk(self):
        print('Walks like a duck.')

    def bark(self):
        print("ducks do not bark")

    def fur(self):
        print("brown feathers ")

class Dog():
    def bark(self):
        print("woof!!")

    def fur(self):
        print("brown and white")

    def walk(self):
        print('Walks like a dog.')

    def quack(self):
        print("dogs don't quack")

def main():

    donald  = Duck()
    trooper = Dog()

    # example of polymorphism - calling same methods on different class objects.
    for o in (donald, trooper):
        o.fur()
        o.bark()
        o.walk()
        o.quack()

    print("")
    print("In the forest ")
    print("")

    # this method can take either a dog or a duck
    in_the_forest(trooper)
    print("")
    print("In the pond")
    print("")
    # this method can take either a dog or a duck
    in_the_pond(donald)

def in_the_forest(dog):
    dog.bark()
    dog.fur()

def in_the_pond(a_duck):
    a_duck.quack()
    a_duck.walk()

if __name__ == "__main__": main()
