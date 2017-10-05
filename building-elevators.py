import sys
import time
import random

class Building:
    def __init__(self,name,NumberOfFloors,NumberOfElevators):
        self.name = name
        self.Floors = []
        self.Elevators = []
        self.TotalSteps = 0

        for x in range(1, NumberOfFloors+1):
            self.AddFloor(x)

        for x in range(1, NumberOfElevators+1):
            self.AddElevator(x)

    def AddFloor(self,name):
        self.Floors.append(Floor(name))

    def AddElevator(self,name):
        self.Elevators.append(Elevator(name))

    def CallButtonPressed(self,SourceFloor,DestinationFloor):
        if SourceFloor == DestinationFloor:
            return False

        for Floor in self.Floors:
            if Floor.name == SourceFloor:
                if Floor.IsScheduled:
                    return False
                else:
                    if SourceFloor < DestinationFloor:
                        Floor.DestinationFloor = DestinationFloor
                        Floor.UpCallButtonIsOn = True
                        print("F%s up button pressed for Floor %s" % (SourceFloor,DestinationFloor))
                        return True
                    else:
                        Floor.DestinationFloor = DestinationFloor
                        Floor.DownCallButtonIsOn = True
                        print("F%s down button pressed for Floor %s" % (SourceFloor,DestinationFloor))
                        return True


    def ScheduleElevators(self):
        for Floor in self.Floors:
            if Floor.isCallButtonPressed() and Floor.IsScheduled != True:
                for Elevator in self.Elevators:
                    if Elevator.IsIdle:
                        print("F%s scheduled e%s for Floor %s" % (Floor.name, Elevator.name, Floor.DestinationFloor))
                        Floor.ScheduleElevator(Elevator,Floor.DestinationFloor)
                        break

    def AllElevatorsAreIdle(self):
        for Elevator in self.Elevators:
            if Elevator.IsActive:
                return False

        return True


    def StepElevators(self):
        self.TotalSteps += 1
        for Elevator in self.Elevators:
            Elevator.Step()


class Floor:
    def __init__(self,name):
        self.name = name
        self.UpCallButtonIsOn = False
        self.DownCallButtonIsOn = False
        self.NextUpElevator = None
        self.NextDownElevator = None
        self.DestinationFloor = 0
        self.IsScheduled = None

    def isCallButtonPressed(self):
        if self.UpCallButtonIsOn or self.DownCallButtonIsOn:
            return True
        else:
            return False

    def ScheduleElevator(self,Elevator,DestinationFloor):
        self.IsScheduled = True
        Elevator.DestinationFloor = DestinationFloor
        Elevator.CallingFloor = self.name
        Elevator.IsInTransitToCallingFloor = True
        Elevator.IsInTransitToDestinationFloor = False

        if self.name > self.DestinationFloor:
            self.NextDownElevator = Elevator.name
        else:
            self.NextUpElevator = Elevator.name

        Elevator.TransitionFromIdleToActive(self.name, self.DestinationFloor)
        print("E%s scheduled for Floor %s going to Floor %s" % (Elevator.name, self.name, self.DestinationFloor))


class Elevator:
    def __init__(self,name):
        self.name = name
        self.IsOutOfService = True
        self.IsIdle = False
        self.IsActive = False
        self.DoorsAreOpen = False

        self.CurrentFloor = random.randrange(1, FloorsInBuilding + 1)

        while self.CurrentFloor == 1:
            self.CurrentFloor = random.randrange(1, FloorsInBuilding + 1)

        self.IsInTransitToDestinationFloor = None
        self.DestinationFloor = 0

        self.IsInTransitToCallingFloor = None
        self.CallingFloor = 0

    def Direction(self):
        if self.IsInTransitToCallingFloor:
            if self.CurrentFloor < self.CallingFloor:
                return 'up'
            if self.CurrentFloor > self.CallingFloor:
                return 'down'
        if self.IsInTransitToDestinationFloor:
            if self.CurrentFloor < self.DestinationFloor:
                return 'up'
            if self.CurrentFloor > self.DestinationFloor:
                return 'down'

    def Step(self):
        if self.IsActive:
            if self.IsInTransitToCallingFloor:
                if self.CurrentFloor == self.CallingFloor:
                    if self.DoorsAreOpen != True:
                        self.DoorsAreOpen = True
                        print("E%s arrived at calling floor %s and opened its doors" % (self.name,self.CallingFloor))
                        return 1
                    else:
                        self.DoorsAreOpen = False
                        self.CallingFloor = None
                        self.IsInTransitToCallingFloor = False
                        self.IsInTransitToDestinationFloor = True
                        print("E%s closed its doors on calling floor %s and is now headed to floor %s" % (self.name,self.CurrentFloor,self.DestinationFloor))
                        return 2

            if self.IsInTransitToDestinationFloor:
                if self.CurrentFloor == self.DestinationFloor:
                    if self.DoorsAreOpen != True:
                        self.DoorsAreOpen = True
                        print("E%s arrived at destination floor %s and opened its doors" % (self.name,self.DestinationFloor))
                        return 3
                    else:
                        self.DoorsAreOpen = False
                        self.DestinationFloor = None
                        self.IsInTransitToDestinationFloor = False
                        print("E%s closed its doors on destination floor %s and is now Idle" % (self.name,self.CurrentFloor))
                        self.TransitionFromActiveToIdle()
                        return 4

            if self.Direction() == "up":
                self.CurrentFloor += 1
                print("E%s moved UP to Floor %s" % (self.name,self.CurrentFloor))
            if self.Direction() == 'down':
                self.CurrentFloor -= 1
                print("E%s moved DOWN to Floor %s" % (self.name,self.CurrentFloor))


    def TransitionFromOutOfServiceToIdle(self):
        if self.IsOutOfService:
            self.IsOutOfService = False
            self.IsIdle = True
            print("E%s transitioned from OutOfService to Idle(%d)" % (self.name,self.CurrentFloor))
        else:
            print('E%s : TransitionFromOutOfServiceToIdle: invalid state' %(self.name))


    def TransitionFromIdleToActive(self,CallingFloor,DestinationFloor):
        if self.IsIdle:
            self.IsIdle = False
            self.IsActive = True
            self.Calling = CallingFloor
            self.DestinationFloor = DestinationFloor
            print("E%s transitioned from Idle to Active. Current Floor = %s, CallingFloor = %s, Destination Floor = %s" % (self.name,self.CurrentFloor,self.CallingFloor,self.DestinationFloor))
        else:
            print('E%s : TransitionFromIdleToActive: invalid state' % (self.name))

    def TransitionFromActiveToIdle(self):
        if self.IsActive and not self.IsInTransitToCallingFloor and not self.IsInTransitToDestinationFloor:
            self.IsIdle = True
            self.IsActive = False
            print("E%s transitioned from Active to Idle(%d)" % (self.name,self.CurrentFloor))
        else:
            print('E%s : TransitionFromActiveToIdle: invalid state' % (self.name))

    def TransitionFromIdleToOutOfService(self):
        if self.IsIdle:
            self.IsOutOfService = True
            self.IsIdle = False
            print("E%s transitioned from Idle(%d) to OutOfService" % (self.name,self.CurrentFloor))
        else:
            print('E%s = TransitionFromIdleToOutOfService: invalid state' % (self.name))

def main():
    print("Starting Elevator")

    FloorsInBuilding = 5
    ElevatorCarsInBuilding = 2
    print("Starting Elevator")
    MyBuilding = Building('3001 Via Conquistador',FloorsInBuilding,ElevatorCarsInBuilding)


    for Elevator in MyBuilding.Elevators:
        Elevator.TransitionFromOutOfServiceToIdle()

    for Floor in MyBuilding.Floors:
        DestinationFloor = random.randrange(1, FloorsInBuilding + 1)

        while DestinationFloor == Floor.name:
            DestinationFloor = random.randrange(1, FloorsInBuilding + 1)

        MyBuilding.CallButtonPressed(Floor.name,DestinationFloor)

    while True:
        print("Starting the elevator")
        MyBuilding.ScheduleElevators()
        MyBuilding.StepElevators()
        if MyBuilding.AllElevatorsAreIdle():
            print("All Elevators are now Idle. Ending Simulation")
            break

    for Elevator in MyBuilding.Elevators:
        Elevator.TransitionFromIdleToOutOfService()

    print("Total Steps = %d" % (MyBuilding.TotalSteps))

    MyBuilding = None

if __name__ == "__main__": main()