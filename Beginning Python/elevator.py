#!/usr/bin/python3

class Elevator():

    def __init__(self, floors_in_bulding, floor):

        # construct the elevator list
        self.floors = []
        for i in range(1, floors_in_bulding + 1):
            self.floors.append("floor: " + str(i))

        self.floor  = floor

    def move(self,floor):
        print("The door is opening on {} ".format(self.floor))
        print("Elevator {} button pushed ".format(floor))
        print("The door is closing on {} ".format(self.floor))

        if floor < self.floor:
            self.floor -= 1
            self.down(floor)
        else:
            self.up(floor)
        print("Closing door on floor {}".format(self.floor))

    def up(self, floor):
        # what floor am I on?
        for f in range (1, floor):
            print("Floor {} ding".format(f))
        self.floor = f
        print("The door is opening on floor: {}".format(self.floor))

    def down(self, floor):

        for f in range (self.floor+1, floor, -1):
            print("Passing Floor {} ding".format(f))
            self.floor = f-1
        print("The door is opening on floor: {}".format(self.floor))


        # print("The door is closing, going down: {}".format(self.floor))


def main():

    e = Elevator(10,5)
    print("The elevator is stationed on floor {} ".format(e.floor))
    e.move(1)
    e.move(6)
    print("The elevator is resting floor:", e.floor)

if __name__ == "__main__":
  main()