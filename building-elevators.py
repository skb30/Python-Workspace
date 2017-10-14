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
        self.Elevators.append(Elevator(name))


        for Elevator in self.Elevators:
            print(str(name))
        #
        # exit()
        #
        # self.Elevators.index(name).CurrentFloor = GetRandomFloor(1, self.NumberOfFloors + 1, 1)
#        self.Elevators[-1].CurrentFloor = GetRandomFloor(1, self.NumberOfFloors + 1, 1)

    def ScheduleElevators(self):
        for Floor in self.Floors:
            if Floor.isCallButtonPressed() and Floor.IsScheduled != True and Floor.DoorsAreOpen != True:
                for Elevator in self.Elevators:
                    if Elevator.IsIdle:
                        Floor.WriteLog("F%s scheduled E%s which is currently on F%s" % (Floor.name,Elevator.name,Elevator.CurrentFloor))
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

    def isCallButtonPressed(self):
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

        Elevator.TransitionFromIdleToActive()
        Elevator.WriteLog("E%s currently on F%s, scheduled for F%s" % (Elevator.name, Elevator.CurrentFloor, self.name))
        self.WriteLog("E%s currently on F%s, scheduled for F%s" % (Elevator.name, Elevator.CurrentFloor, self.name))

    def CallButtonPressed(self, UpOrDown,FloorsInBuilding):
        self.IsScheduled = False

        if self.name == 1:
            self.UpCallButtonIsOn = True
            self.WriteLog("F%s up button was pressed" % (self.name))
            return 1

        if self.name == FloorsInBuilding:
            self.DownCallButtonIsOn = True
            self.WriteLog("F%s down button was pressed" % (self.name))
            return 1

        if UpOrDown == 'up':
            self.UpCallButtonIsOn = True
            self.WriteLog("F%s up button was pressed" % (self.name))
            return 1

        if UpOrDown == 'down':
            self.DownCallButtonIsOn = True
            self.WriteLog("F%s down button was pressed" % (self.name))
            return 1

    def WriteLog(self,LogLine):
        self.Log.append(LogLine)


class Elevator:
    def __init__(self,name):
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
                        self.WriteLog("E%s arrived at calling F%s and opened its doors" % (self.name,self.CallingFloor))
                        self.DoorsAreOpen = True
                        OpenDoorsOnFloor(self.CurrentFloor,"F%s E%s arrived on calling floor" % (self.CallingFloor,self.name))
                        return 1
                    else:
                        ChooseDestinationFloor(self)
                        CloseDoorsOnFloor(self.CurrentFloor,"F%s Destination floor F%s was selected in E%s" % (self.CurrentFloor,self.DestinationFloor,self.name))
                        TurnCallButtonOff(self)
                        self.DoorsAreOpen = False
                        self.IsInTransitToCallingFloor = False
                        self.IsInTransitToDestinationFloor = True
                        self.WriteLog("E%s closed its doors on calling F%s and is now headed to F%s" % (self.name,self.CurrentFloor,self.DestinationFloor))
                        return 2

            if self.IsInTransitToDestinationFloor:
                if self.CurrentFloor == self.DestinationFloor:
                    if self.DoorsAreOpen != True:
                        self.DoorsAreOpen = True
                        self.WriteLog("E%s arrived at destination F%s and opened its doors" % (self.name,self.DestinationFloor))
                        OpenDoorsOnFloor(self.CurrentFloor,"F%s E%s arrived on destination floor. Called from F%s" % (self.CurrentFloor, self.name, self.CallingFloor))
                        return 3
                    else:
                        CloseDoorsOnFloor(self.CurrentFloor,None)
                        self.DoorsAreOpen = False
                        self.IsInTransitToDestinationFloor = False
                        self.WriteLog("E%s closed its doors on destination F%s and is now Idle" % (self.name,self.CurrentFloor))
                        self.TransitionFromActiveToIdle()
                        return 4

            if self.Direction() == "up":
                self.CurrentFloor += 1
                self.WriteLog("E%s moved UP to F%s" % (self.name,self.CurrentFloor))
                self.Steps += 1
                return 5
            if self.Direction() == 'down':
                self.CurrentFloor -= 1
                self.WriteLog("E%s moved DOWN to F%s" % (self.name,self.CurrentFloor))
                self.Steps += 1
                return 6


    def TransitionFromOutOfServiceToIdle(self):
        if self.IsOutOfService:
            self.IsOutOfService = False
            self.IsIdle = True
            self.WriteLog("E%s transitioned from OutOfService to Idle. Currently on F%s" % (self.name,self.CurrentFloor))
        else:
            self.WriteLog('E%s : TransitionFromOutOfServiceToIdle: invalid state' %(self.name))


    def TransitionFromIdleToActive(self):
        if self.IsIdle:
            self.IsIdle = False
            self.IsActive = True
            self.WriteLog("E%s transitioned from Idle to Active" % (self.name))
        else:
            self.WriteLog('E%s : TransitionFromIdleToActive: invalid state' % (self.name))

    def TransitionFromActiveToIdle(self):
        if self.IsActive and not self.IsInTransitToCallingFloor and not self.IsInTransitToDestinationFloor:
            self.IsIdle = True
            self.IsActive = False
            self.WriteLog("E%s transitioned from Active to Idle. Currently on F%d" % (self.name,self.CurrentFloor))
        else:
            self.WriteLog('E%s : TransitionFromActiveToIdle: invalid state' % (self.name))

    def TransitionFromIdleToOutOfService(self):
        if self.IsIdle:
            self.IsOutOfService = True
            self.IsIdle = False
            self.WriteLog("E%s transitioned from Idle to OutOfService. Currently on F%d" % (self.name,self.CurrentFloor))
        else:
            self.WriteLog('E%s = TransitionFromIdleToOutOfService: invalid state' % (self.name))

    def WriteLog(self,LogLine):
        self.Log.append(LogLine)


def GetRandomFloor(MinValue,MaxValue,ExcludeValue):
    RandomNumber = random.randint(MinValue,MaxValue)
    while RandomNumber == ExcludeValue:
        RandomNumber = random.randint(MinValue, MaxValue)

    return RandomNumber

def ChooseRandomValue(Value1,Value2):
    RandomValue = random.randint(0,1)

    if RandomValue == 0:
        return Value1
    else:
        return Value2

def OpenDoorsOnFloor(TargetFloor,InfoMessage, MyBuilding):
    for Floor in MyBuilding.Floors:
        if Floor.name == TargetFloor:
            if InfoMessage != None:
                Floor.WriteLog(InfoMessage)
            Floor.DoorsAreOpen = True
            Floor.WriteLog("F%s doors opened" % (Floor.name))

def CloseDoorsOnFloor(TargetFloor,InfoMessage, MyBuilding):
    for Floor in MyBuilding.Floors:
        if Floor.name == TargetFloor:
            if InfoMessage != None:
                Floor.WriteLog(InfoMessage)
            Floor.DoorsAreOpen = False
            Floor.WriteLog("F%s doors closed" % (Floor.name))

def TurnCallButtonOff(Elevator, MyBuilding):
    for Floor in MyBuilding.Floors:
        if Floor.name == Elevator.CurrentFloor:
            if Elevator.CurrentFloor < Elevator.DestinationFloor:
                Floor.UpCallButtonIsOn = False
                Floor.WriteLog("F%s Up call button is off" % (Floor.name))

            if Elevator.CurrentFloor > Elevator.DestinationFloor:
                Floor.DownCallButtonIsOn = False
                Floor.WriteLog("F%s Down call button is off" % (Floor.name))

def ChooseDestinationFloor(Elevator, MyBuilding):
    RandomFloor = None
    for Floor in MyBuilding.Floors:
        if Floor.name == Elevator.CurrentFloor:
            if Floor.UpCallButtonIsOn:
                RandomFloor = GetRandomFloor(Elevator.CurrentFloor,MyBuilding.NumberOfFloors,Elevator.CurrentFloor)
                break

            if Floor.DownCallButtonIsOn:
                RandomFloor = GetRandomFloor(1,Elevator.CurrentFloor,Elevator.CurrentFloor)
                break

    Elevator.DestinationFloor = RandomFloor
    Elevator.WriteLog("E%s is currently on F%s selected F%s as destination floor" % (Elevator.name,Elevator.CurrentFloor,Elevator.DestinationFloor))


def main():

    random.seed()

    FloorsInBuilding = 20
    ElevatorCarsInBuilding = 2

    MyBuilding = Building('3001 Via Conquistador',FloorsInBuilding,ElevatorCarsInBuilding)

    print("Bringing all Elevators to Idle. Starting Simulation")
    for Elevator in MyBuilding.Elevators:
        # print(type(Elevator))
        # print("The elevator type is: {}".format(type(Elevator))
        Elevator.TransitionFromOutOfServiceToIdle()


    for Floor in MyBuilding.Floors:
        Floor.CallButtonPressed(ChooseRandomValue("up","down"),FloorsInBuilding)

    while True:
        MyBuilding.ScheduleElevators()
        MyBuilding.StepElevators()
        if MyBuilding.AllElevatorsAreIdle() and MyBuilding.AllCallButtonsAreOff():
            print("All Elevators are now Idle. Ending Simulation\n")
            break

    for Elevator in MyBuilding.Elevators:
        Elevator.TransitionFromIdleToOutOfService()

    MyBuilding.PrintLogs()

    for Elevator in MyBuilding.Elevators:
        print("Total Elevator E%s Steps = %s" % (Elevator.name, Elevator.Steps))

    print("Total Steps = %d" % (MyBuilding.TotalSteps))


if __name__ == "__main__":
    main()



