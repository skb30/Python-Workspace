import sys
import time
import random


class Building:
    def __init__(self,name,numOfFloors,NumberOfElevators):
        self.name = name
        self.Floors = []
        self.Elevators = []
        self.Totalsteps = 0
        self.numOfFloors = numOfFloors
        self.NumberOfElevators = NumberOfElevators

        for x in range(1, self.numOfFloors+1):
            self.AddFloor(x)

        for x in range(1, self.NumberOfElevators+1):
            self.AddElevator(x)

    def AddFloor(self,name):
        self.Floors.append(Floor(name))

    def AddElevator(self,name):
        self.Elevators.append(Elevator(name, self.numOfFloors))


        # for elevator in self.Elevators:
        #     print(str(elevator.name))
        #
        # exit()
        #
        # self.Elevators.index(name).currentFloor = getRandomFloor(1, self.numOfFloors + 1, 1)
#        self.Elevators[-1].currentFloor = getRandomFloor(1, self.numOfFloors + 1, 1)

    def scheduleElevators(self):
        for floor in self.Floors:
            if floor.iscallButtonPressed() and floor.isScheduled != True and floor.doorsAreOpen != True:
                for elevator in self.Elevators:
                    if elevator.isIdle:
                        floor.writeLog("Floor %s: scheduled E%s which is currently on Floor %s" % (floor.name,elevator.name,elevator.currentFloor))
                        floor.scheduleElevator(elevator)
                        break

    def allElevatorsAreIdle(self):
        for elevator in self.Elevators:
            if elevator.isActive:
                return False

        return True

    def allCallButtonsAreOff(self):
        for Floor in self.Floors:
            if Floor.upCallButtonIsOn or Floor.downCallButtonIsOn:
                return False

        return True

    def stepElevators(self):
        for Elevator in self.Elevators:
            Elevator.step(self)
            self.Totalsteps += 1


    def printLogs(self):
        for Elevator in self.Elevators:
            print("***** E%s log *****" % Elevator.name)
            for Line in Elevator.Log:
                print(Line)
            print("\n")

        print("\n")

        for Floor in self.Floors:
            print("***** Floor %s: log *****" % Floor.name)
            for Line in Floor.Log:
                print(Line)
            print("\n")


class Floor:
    def __init__(self,name):
        self.name = name
        self.upCallButtonIsOn = False
        self.downCallButtonIsOn = False
        self.nextUpElevator = None
        self.nextDownElevator = None
        self.isScheduled = None
        self.doorsAreOpen = False
        self.Log = []

    def iscallButtonPressed(self):
        if self.upCallButtonIsOn or self.downCallButtonIsOn:
            return True
        else:
            return False

    def scheduleElevator(self,elevator):
        self.isScheduled = True
        elevator.callingFloor = self.name
        elevator.isInTransitTocallingFloor = True
        elevator.isInTransitTodestinationFloor = False

        if self.upCallButtonIsOn:
            self.nextUpElevator = elevator.name
        if self.downCallButtonIsOn:
            self.nextDownElevator = elevator.name

        elevator.transitionFromIdleToActive()
        elevator.writeLog("Elevator {} is currently on Floor {}, and is scheduled for Floor {}".format(elevator.name, elevator.currentFloor, self.name))
        self.writeLog("Elevator {} is currently on Floor {}, scheduled for Floor {}".format(elevator.name, elevator.currentFloor, self.name))

    def callButtonPressed(self, UpOrDown,FloorsInBuilding):
        self.isScheduled = False

        if self.name == 1:
            self.upCallButtonIsOn = True
            self.writeLog("Floor %s: up button was pressed" % (self.name))
            return

        if self.name == FloorsInBuilding:
            self.downCallButtonIsOn = True
            self.writeLog("Floor %s: down button was pressed" % (self.name))
            return

        if UpOrDown == 'up':
            self.upCallButtonIsOn = True
            self.writeLog("Floor %s: up button was pressed" % (self.name))
            return

        if UpOrDown == 'down':
            self.downCallButtonIsOn = True
            self.writeLog("Floor %s: down button was pressed" % (self.name))
            return

    def writeLog(self,LogLine):
        self.Log.append(LogLine)


class Elevator:
    def __init__(self, name, maxFloors):
        self.name = name
        self.isOutOfService = True
        self.isIdle = False
        self.isActive = False
        self.doorsAreOpen = False

        self.currentFloor = getRandomFloor(1,maxFloors,0)

        self.isInTransitTodestinationFloor = False
        self.destinationFloor = 0

        self.isInTransitTocallingFloor = False
        self.callingFloor = 0

        self.Log = []
        self.steps = 0


    def direction(self):
            if self.isInTransitTocallingFloor:
                if self.currentFloor < self.callingFloor:
                    return 'up'
                if self.currentFloor > self.callingFloor:
                    return 'down'
            if self.isInTransitTodestinationFloor:
                if self.currentFloor < self.destinationFloor:
                    return 'up'
                if self.currentFloor > self.destinationFloor:
                    return 'down'


    def step(self,building):
        if self.isActive:
            if self.isInTransitTocallingFloor:
                if self.currentFloor == self.callingFloor:
                    if self.doorsAreOpen != True:
                        self.writeLog("Building: {} elevator {} arrived at calling floor {} and opened its doors".format(building.name,self.name,self.callingFloor))
                        self.doorsAreOpen = True
                        openDoorsOnFloor(building,self.currentFloor,"Floor {}: Elevator {} arrived on calling floor.".format(self.callingFloor,self.name))
                        return
                    else:
                        chooseDestinationfloor(self,building)
                        closeDoorsOnFloor(building,self.currentFloor,"Floor {}: Destination floor {} was selected in Elevator {} for building: {}".format(
                            self.currentFloor,self.destinationFloor,self.name, building.name))
                        turnCallButtonOff(self, building)
                        self.doorsAreOpen = False
                        self.isInTransitTocallingFloor = False
                        self.isInTransitTodestinationFloor = True
                        self.writeLog("E%s closed its doors on calling Floor %s: and is now headed to Floor %s:" % (self.name,self.currentFloor,self.destinationFloor))
                        return

            if self.isInTransitTodestinationFloor:
                if self.currentFloor == self.destinationFloor:
                    if self.doorsAreOpen != True:
                        self.doorsAreOpen = True
                        self.writeLog("E%s arrived at destination Floor %s: and opened its doors" % (self.name,self.destinationFloor))
                        openDoorsOnFloor(building,self.currentFloor,"Floor %s: E%s arrived on destination floor. Called from Floor %s:" % (self.currentFloor, self.name, self.callingFloor))
                        return
                    else:
                        closeDoorsOnFloor(building, self.currentFloor,None)
                        self.doorsAreOpen = False
                        self.isInTransitTodestinationFloor = False
                        self.writeLog("E%s closed its doors on destination Floor %s: and is now Idle" % (self.name,self.currentFloor))
                        self.transitionFromActiveToIdle(building)
                        return

            if self.direction() == "up":
                self.currentFloor += 1
                self.writeLog("E%s moved UP to Floor %s:" % (self.name,self.currentFloor))
                self.steps += 1
                return 5
            if self.direction() == 'down':
                self.currentFloor -= 1
                self.writeLog("E%s moved DOWN to Floor %s:" % (self.name,self.currentFloor))
                self.steps += 1
                return 6


    def transitionFromOutOfServiceToIdle(self,buildingName):
        if self.isOutOfService:
            self.isOutOfService = False
            self.isIdle = True
            self.writeLog("Building {} - E{} transitioned from OutOfService to Idle. Currently on F{}".format(buildingName,self.name,self.currentFloor))
        else:
            self.writeLog('Building {} - E{} : transitionFromOutOfServiceToIdle: invalid state'.format(buildingName,self.name))


    def transitionFromIdleToActive(self):
        if self.isIdle:
            self.isIdle = False
            self.isActive = True
            self.writeLog("E%s transitioned from Idle to Active" % (self.name))
        else:
            self.writeLog('E%s : transitionFromIdleToActive: invalid state' % (self.name))

    def transitionFromActiveToIdle(self,building):
        if self.isActive and not self.isInTransitTocallingFloor and not self.isInTransitTodestinationFloor:
            self.isIdle = True
            self.isActive = False
            self.writeLog("E%s transitioned from Active to Idle. Currently on F%d" % (self.name,self.currentFloor))
        else:
            self.writeLog('E%s : transitionFromActiveToIdle: invalid state' % (self.name))

    def transitionFromIdleToOutOfService(self,building):
        if self.isIdle:
            self.isOutOfService = True
            self.isIdle = False
            self.writeLog("E%s transitioned from Idle to OutOfService. Currently on F%d" % (self.name,self.currentFloor))
        else:
            self.writeLog('E%s = transitionFromIdleToOutOfService: invalid state' % (self.name))

    def writeLog(self,LogLine):
        self.Log.append(LogLine)

# Proxy Methods (Global)
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

def openDoorsOnFloor(building,targetFloor,infoMessage):
    for floor in building.Floors:
        if floor.name == targetFloor:
            if infoMessage != None:
                floor.writeLog(infoMessage)
            floor.doorsAreOpen = True
            floor.writeLog("Floor %s: doors opened" % (floor.name))

def closeDoorsOnFloor(building,targetFloor,InfoMessage):
    for floor in building.Floors:
        if floor.name == targetFloor:
            if InfoMessage != None:
                floor.writeLog(InfoMessage)
            floor.doorsAreOpen = False
            floor.writeLog("Floor %s: doors closed" % (floor.name))

def turnCallButtonOff(Elevator, building):
    for floor in building.Floors:
        if floor.name == Elevator.currentFloor:
            if Elevator.currentFloor < Elevator.destinationFloor:
                floor.upCallButtonIsOn = False
                floor.writeLog("Floor %s: Up call button is off" % (floor.name))

            if Elevator.currentFloor > Elevator.destinationFloor:
                floor.downCallButtonIsOn = False
                floor.writeLog("Floor %s: Down call button is off" % (floor.name))

def chooseDestinationfloor(Elevator, building):
    Randomfloor = None
    for floor in building.Floors:
        if floor.name == Elevator.currentFloor:
            if floor.upCallButtonIsOn:
                RandomFloor = getRandomFloor(Elevator.currentFloor,building.numOfFloors,Elevator.currentFloor)
                break

            if floor.downCallButtonIsOn:
                RandomFloor = getRandomFloor(1,Elevator.currentFloor,Elevator.currentFloor)
                break

    Elevator.destinationFloor = RandomFloor
    Elevator.writeLog("E%s is currently on Floor %s selected Floor %s as destination floor" % (Elevator.name,Elevator.currentFloor,Elevator.destinationFloor))

def createBuilding(buildingAddress,floorsInBuilding,numOfElevators):
        return Building(buildingAddress,floorsInBuilding,numOfElevators)


def main():
    random.seed()
    cities = []

    buildings = []

    cities.append(buildings.append(createBuilding('3001 Via Conquistador',10,1)))
    buildings.append(createBuilding('2364 Arguello Place', 10, 2))
    
    for building in buildings:


        print("Bringing all Elevators to Idle. Starting Simulation on Building {}".format(building.name))
        for elevator in building.Elevators:
            elevator.transitionFromOutOfServiceToIdle(building.name)
        #

        for floor in building.Floors:
            floor.callButtonPressed(chooseRandomValue("up","down"),building.numOfFloors)
        #
        while True:
            building.scheduleElevators()
            building.stepElevators()
            if building.allElevatorsAreIdle() and building.allCallButtonsAreOff():
                print("All Elevators are now Idle on building {}.".format(building.name))
                break

        for elevator in building.Elevators:
            elevator.transitionFromIdleToOutOfService(building)

            building.printLogs()

        for elevator in building.Elevators:
            print("Total Elevator E%s steps = {}".format(elevator.name, elevator.steps))

        print("Total elevator steps for building {}  = {}".format(building.name,building.Totalsteps))

    print("Simulation Ended.")
if __name__ == "__main__":
    main()



