#!/usr/bin/python3

class Animal:
    def walk(self):
        print("I'm walking here")

    def clothes(self):
        print("I'm sporting fine threads")

    def talk(self):
        print("I have something to say")

class Duck (Animal):
    def quack(self):
        print('Quaaack!')

    def walk(self):
        print('Walks like a duck.')

class Dog(Animal):
    def clothes(self):
        print("I have a brown and white coat")

    def talk(self):
        super().talk()
        print("Bow Wow!")

def main():
    donald = Duck()
    donald.clothes()
    donald.walk()
    trooper = Dog()
    trooper.walk()
    trooper.talk()



if __name__ == "__main__": main()
