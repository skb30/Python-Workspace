import sys
import time
import random


class Building:
    def __init__(self,name,NumberOfFloors,NumberOfElevators):
        self.name = name
        self.Floors = []
        self.Elevators = []
        self.TotalSteps = 0
        self.NumberOfFloors = NumberOfFloors
        self.NumberOfElevators = NumberOfElevators

        for x in range(1, self.NumberOfFloors+1):
            self.AddFloor(x)

        for x in range(1, self.NumberOfElevators+1):
            self.AddElevator(x)

    def AddFloor(self,name):
        self.Floors.append(Floor(name))

    def AddElevator(self,name):
        self.Elevators.append(Elevator(name, self.NumberOfFloors))


        # for elevator in self.Elevators:
        #     print(str(elevator.name))
        #
        # exit()
        #
        # self.Elevators.index(name).CurrentFloor = getRandomFloor(1, self.NumberOfFloors + 1, 1)
#        self.Elevators[-1].CurrentFloor = getRandomFloor(1, self.NumberOfFloors + 1, 1)

    def ScheduleElevators(self):
        for Floor in self.Floors:
            if Floor.iscallButtonPressed() and Floor.IsScheduled != True and Floor.DoorsAreOpen != True:
                for Elevator in self.Elevators:
                    if Elevator.IsIdle:
                        Floor.writeLog("F%s scheduled E%s which is currently on F%s" % (Floor.name,Elevator.name,Elevator.CurrentFloor))
                        Floor.ScheduleElevator(Elevator)
                        break

    def AllElevatorsAreIdle(self):
        for Elevator in self.Elevators:
            if Elevator.IsActive:
                return False

        return True

    def AllCallButtonsAreOff(self):
        for Floor in self.Floors:
            if Floor.UpCallButtonIsOn or Floor.DownCallButtonIsOn:
                return False

        return True

    def StepElevators(self):
        for Elevator in self.Elevators:
            Elevator.Step()
            self.TotalSteps += 1


    def PrintLogs(self):
        for Elevator in self.Elevators:
            print("***** E%s log *****" % Elevator.name)
            for Line in Elevator.Log:
                print(Line)
            print("\n")


        print("\n")

        for Floor in self.Floors:
            print("***** F%s log *****" % Floor.name)
            for Line in Floor.Log:
                print(Line)
            print("\n")


class Floor:
    def __init__(self,name):
        self.name = name
        self.UpCallButtonIsOn = False
        self.DownCallButtonIsOn = False
        self.NextUpElevator = None
        self.NextDownElevator = None
        self.IsScheduled = None
        self.DoorsAreOpen = False
        self.Log = []

    def iscallButtonPressed(self):
        if self.UpCallButtonIsOn or self.DownCallButtonIsOn:
            return True
        else:
            return False

    def ScheduleElevator(self,Elevator):
        self.IsScheduled = True
        Elevator.CallingFloor = self.name
        Elevator.IsInTransitToCallingFloor = True
        Elevator.IsInTransitToDestinationFloor = False

        if self.UpCallButtonIsOn:
            self.NextUpElevator = Elevator.name
        if self.DownCallButtonIsOn:
            self.NextDownElevator = Elevator.name

        Elevator.transitionFromIdleToActive()
        Elevator.writeLog("E%s currently on F%s, scheduled for F%s" % (Elevator.name, Elevator.CurrentFloor, self.name))
        self.writeLog("E%s currently on F%s, scheduled for F%s" % (Elevator.name, Elevator.CurrentFloor, self.name))

    def callButtonPressed(self, UpOrDown,FloorsInBuilding):
        self.IsScheduled = False

        if self.name == 1:
            self.UpCallButtonIsOn = True
            self.writeLog("F%s up button was pressed" % (self.name))
            return 1

        if self.name == FloorsInBuilding:
            self.DownCallButtonIsOn = True
            self.writeLog("F%s down button was pressed" % (self.name))
            return 1

        if UpOrDown == 'up':
            self.UpCallButtonIsOn = True
            self.writeLog("F%s up button was pressed" % (self.name))
            return 1

        if UpOrDown == 'down':
            self.DownCallButtonIsOn = True
            self.writeLog("F%s down button was pressed" % (self.name))
            return 1

    def writeLog(self,LogLine):
        self.Log.append(LogLine)


class Elevator:
    def __init__(self, name, maxFloors):
        self.name = name
        self.IsOutOfService = True
        self.IsIdle = False
        self.IsActive = False
        self.DoorsAreOpen = False

        self.CurrentFloor = 0

        self.IsInTransitToDestinationFloor = False
        self.DestinationFloor = 0

        self.IsInTransitToCallingFloor = False
        self.CallingFloor = 0

        self.Log = []
        self.Steps = 0


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
                        self.writeLog("E%s arrived at calling F%s and opened its doors" % (self.name,self.CallingFloor))
                        self.DoorsAreOpen = True
                        openDoorsOnFloor(self.CurrentFloor,"F%s E%s arrived on calling floor" % (self.CallingFloor,self.name))
                        return 1
                    else:
                        chooseDestinationFloor(self)
                        closeDoorsOnFloor(self.CurrentFloor,"F%s Destination floor F%s was selected in E%s" % (self.CurrentFloor,self.DestinationFloor,self.name))
                        turnCallButtonOff(self)
                        self.DoorsAreOpen = False
                        self.IsInTransitToCallingFloor = False
                        self.IsInTransitToDestinationFloor = True
                        self.writeLog("E%s closed its doors on calling F%s and is now headed to F%s" % (self.name,self.CurrentFloor,self.DestinationFloor))
                        return 2

            if self.IsInTransitToDestinationFloor:
                if self.CurrentFloor == self.DestinationFloor:
                    if self.DoorsAreOpen != True:
                        self.DoorsAreOpen = True
                        self.writeLog("E%s arrived at destination F%s and opened its doors" % (self.name,self.DestinationFloor))
                        openDoorsOnFloor(self.CurrentFloor,"F%s E%s arrived on destination floor. Called from F%s" % (self.CurrentFloor, self.name, self.CallingFloor))
                        return 3
                    else:
                        closeDoorsOnFloor(self.CurrentFloor,None)
                        self.DoorsAreOpen = False
                        self.IsInTransitToDestinationFloor = False
                        self.writeLog("E%s closed its doors on destination F%s and is now Idle" % (self.name,self.CurrentFloor))
                        self.transitionFromActiveToIdle()
                        return 4

            if self.Direction() == "up":
                self.CurrentFloor += 1
                self.writeLog("E%s moved UP to F%s" % (self.name,self.CurrentFloor))
                self.Steps += 1
                return 5
            if self.Direction() == 'down':
                self.CurrentFloor -= 1
                self.writeLog("E%s moved DOWN to F%s" % (self.name,self.CurrentFloor))
                self.Steps += 1
                return 6


    def transitionFromOutOfServiceToIdle(self):
        if self.IsOutOfService:
            self.IsOutOfService = False
            self.IsIdle = True
            self.writeLog("E%s transitioned from OutOfService to Idle. Currently on F%s" % (self.name,self.CurrentFloor))
        else:
            self.writeLog('E%s : transitionFromOutOfServiceToIdle: invalid state' %(self.name))


    def transitionFromIdleToActive(self):
        if self.IsIdle:
            self.IsIdle = False
            self.IsActive = True
            self.writeLog("E%s transitioned from Idle to Active" % (self.name))
        else:
            self.writeLog('E%s : transitionFromIdleToActive: invalid state' % (self.name))

    def transitionFromActiveToIdle(self):
        if self.IsActive and not self.IsInTransitToCallingFloor and not self.IsInTransitToDestinationFloor:
            self.IsIdle = True
            self.IsActive = False
            self.writeLog("E%s transitioned from Active to Idle. Currently on F%d" % (self.name,self.CurrentFloor))
        else:
            self.writeLog('E%s : transitionFromActiveToIdle: invalid state' % (self.name))

    def transitionFromIdleToOutOfService(self):
        if self.IsIdle:
            self.IsOutOfService = True
            self.IsIdle = False
            self.writeLog("E%s transitioned from Idle to OutOfService. Currently on F%d" % (self.name,self.CurrentFloor))
        else:
            self.writeLog('E%s = transitionFromIdleToOutOfService: invalid state' % (self.name))

    def writeLog(self,LogLine):
        self.Log.append(LogLine)


def getRandomFloor(minvalue,maxvalue,excludevalue):
    randomNumber = random.randint(minvalue,maxvalue)
    while randomNumber == excludevalue:
        randomNumber = random.randint(minvalue, maxvalue)

    return randomNumber

def chooseRandomValue(value1,value2):
    randomvalue = random.randint(0,1)

    if randomvalue == 0:
        return value1
    else:
        return value2

def openDoorsOnFloor(targetFloor,infoMessage):
    for floor in myBuilding.Floors:
        if floor.name == targetFloor:
            if infoMessage != None:
                floor.writeLog(infoMessage)
            floor.DoorsAreOpen = True
            floor.writeLog("F%s doors opened" % (floor.name))

def closeDoorsOnFloor(targetFloor,InfoMessage):
    for floor in myBuilding.floors:
        if floor.name == targetFloor:
            if InfoMessage != None:
                floor.writeLog(InfoMessage)
            floor.DoorsAreOpen = False
            floor.writeLog("F%s doors closed" % (floor.name))

def turnCallButtonOff(Elevator, myBuilding):
    for floor in myBuilding.Floors:
        if floor.name == Elevator.CurrentFloor:
            if Elevator.CurrentFloor < Elevator.DestinationFloor:
                floor.UpCallButtonIsOn = False
                floor.writeLog("F%s Up call button is off" % (floor.name))

            if Elevator.CurrentFloor > Elevator.DestinationFloor:
                floor.DownCallButtonIsOn = False
                floor.writeLog("F%s Down call button is off" % (floor.name))

def chooseDestinationfloor(Elevator):
    Randomfloor = None
    for floor in myBuilding.Floors:
        if floor.name == Elevator.CurrentFloor:
            if floor.UpCallButtonIsOn:
                RandomFloor = getRandomFloor(Elevator.CurrentFloor,myBuilding.NumberOfFloors,Elevator.CurrentFloor)
                break

            if floor.DownCallButtonIsOn:
                RandomFloor = getRandomFloor(1,Elevator.CurrentFloor,Elevator.CurrentFloor)
                break

    Elevator.DestinationFloor = RandomFloor
    Elevator.writeLog("E%s is currently on F%s selected F%s as destination floor" % (Elevator.name,Elevator.CurrentFloor,Elevator.DestinationFloor))


def main():

    random.seed()

    floorsInBuilding = 20
    elevatorCarsInBuilding = 2

    myBuilding = Building('3001 Via Conquistador',floorsInBuilding,elevatorCarsInBuilding)

    print("Bringing all Elevators to Idle. Starting Simulation")
    for elevator in myBuilding.Elevators:
        # print(type(Elevator))
        # print("The elevator type is: {}".format(type(Elevator))
        elevator.transitionFromOutOfServiceToIdle()


    for floor in myBuilding.Floors:
        buttonPressed = getRandomFloor(1, elevator.CurrentFloor, elevator.CurrentFloor)
        # floor.callButtonPressed(buttonPressed,floorsInBuilding)

    while True:
        myBuilding.ScheduleElevators()
        myBuilding.StepElevators()
        if myBuilding.AllElevatorsAreIdle() and myBuilding.AllCallButtonsAreOff():
            print("All Elevators are now Idle. Ending Simulation\n")
            break

    for elevator in myBuilding.Elevators:
        elevator.transitionFromIdleToOutOfService()

    myBuilding.PrintLogs()

    for elevator in myBuilding.Elevators:
        print("Total Elevator E%s Steps = %s" % (elevator.name, elevator.Steps))

    print("Total Steps = %d" % (myBuilding.TotalSteps))


if __name__ == "__main__":
    main()



