import sys
import time
import random

FloorsInBuilding = 5
ElevatorCarsInBuilding = 2

class Building:
    def __init__(self,name,NumberOfFloors,NumberOfElevators):
        self.name = name
        self.Floors = []
        self.Elevators = []
        self.log = []
        self.TotalSteps = 0
        # self.log = open("building-log.txt", "w+")

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
                        self.log.append("F" + str(SourceFloor) + "up button pressed for Floor " + str(DestinationFloor))
                        return True
                    else:
                        Floor.DestinationFloor = DestinationFloor
                        Floor.DownCallButtonIsOn = True
                        self.log.append("F" + str(SourceFloor) + "down button pressed for Floor " + str(DestinationFloor))
                        return True


    def ScheduleElevators(self):
        for Floor in self.Floors:
            if Floor.isCallButtonPressed() and Floor.IsScheduled != True:
                for Elevator in self.Elevators:
                    if Elevator.IsIdle:
                        self.log.append("F" + str(Floor.name) + " scheduled " + str(Elevator.name) + " for Floor " + str(Floor.DestinationFloor))
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
        self.log = []


    def get_log(self):
        for line in self.log:
            print(line)

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
        self.log.append("E" + str(Elevator.name) + " scheduled for Floor " + str(self.name) + " going to Floor " + str(self.DestinationFloor))


class Elevator:
    def __init__(self,name):
        self.name = name
        self.IsOutOfService = True
        self.IsIdle = False
        self.IsActive = False
        self.DoorsAreOpen = False
        self.log = []

        self.CurrentFloor = random.randrange(1, FloorsInBuilding + 1)

        while self.CurrentFloor == 1:
            self.CurrentFloor = random.randrange(1, FloorsInBuilding + 1)

        self.IsInTransitToDestinationFloor = None
        self.DestinationFloor = 0

        self.IsInTransitToCallingFloor = None
        self.CallingFloor = 0

    def get_log(self):
        for line in self.log:
            print(line)


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
                        self.log.append("E" + str(self.name) +  " arrived at calling floor " + str(self.CallingFloor) + " and opened its doors ")

                        return 1
                    else:
                        self.DoorsAreOpen = False
                        self.CallingFloor = None
                        self.IsInTransitToCallingFloor = False
                        self.IsInTransitToDestinationFloor = True
                        self.log.append("E" + str(self.name) + " closed its doors on calling floor " + str(self.CurrentFloor) +  " and is now headed to floor " + str(self.DestinationFloor))
                        return 2

            if self.IsInTransitToDestinationFloor:
                if self.CurrentFloor == self.DestinationFloor:
                    if self.DoorsAreOpen != True:
                        self.DoorsAreOpen = True

                        self.log.append("E" + str(self.name) + " arrived at destination floor " + str(self.DestinationFloor) + " and opened its doors")
                        return 3
                    else:
                        self.DoorsAreOpen = False
                        self.DestinationFloor = None
                        self.IsInTransitToDestinationFloor = False
                        self.log.append("E" + str(self.name) + " closed its doors on destination floor " +  str(self.CurrentFloor) + "and is now Idle")
                        self.TransitionFromActiveToIdle()
                        return 4

            if self.Direction() == "up":
                self.CurrentFloor += 1
                self.log.append("E" + str(self.name) + " moved UP to Floor " +  str(self.CurrentFloor))
            if self.Direction() == 'down':
                self.CurrentFloor -= 1
                self.log.append("E%s moved DOWN to Floor %s\n" % (self.name,self.CurrentFloor))


    def TransitionFromOutOfServiceToIdle(self):
        if self.IsOutOfService:
            self.IsOutOfService = False
            self.IsIdle = True

            self.log.append("E%s transitioned from OutOfService to Idle(%d)" % (self.name,self.CurrentFloor))
        else:
            self.log.append('E%s : TransitionFromOutOfServiceToIdle: invalid state\n' %(self.name))


    def TransitionFromIdleToActive(self,CallingFloor,DestinationFloor):
        if self.IsIdle:
            self.IsIdle = False
            self.IsActive = True
            self.Calling = CallingFloor
            self.DestinationFloor = DestinationFloor
            self.log.append("E%s transitioned from Idle to Active. Current Floor = %s, CallingFloor = %s, Destination Floor = %s\n" % (self.name,self.CurrentFloor,self.CallingFloor,self.DestinationFloor))
        else:
            self.log.append('E%s : TransitionFromIdleToActive: invalid state\n' % (self.name))

    def TransitionFromActiveToIdle(self):
        if self.IsActive and not self.IsInTransitToCallingFloor and not self.IsInTransitToDestinationFloor:
            self.IsIdle = True
            self.IsActive = False
            self.log.append("E%s transitioned from Active to Idle(%d)\n" % (self.name,self.CurrentFloor))
        else:
            self.log.append('E%s : TransitionFromActiveToIdle: invalid state\n' % (self.name))

    def TransitionFromIdleToOutOfService(self):
        if self.IsIdle:
            self.IsOutOfService = True
            self.IsIdle = False
            self.log.append("E%s transitioned from Idle(%d) to OutOfService\n" % (self.name,self.CurrentFloor))
        else:
            self.log.append('E%s = TransitionFromIdleToOutOfService: invalid state\n' % (self.name))

def main():
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

    for elevator in MyBuilding.Elevators:
        elevator.get_log()

    for floor in MyBuilding.Floors:
        floor.get_log()

    print("Total Steps = %d" % (MyBuilding.TotalSteps))

    MyBuilding = None

if __name__ == "__main__": main()