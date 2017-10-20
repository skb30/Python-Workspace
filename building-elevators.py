import sys
import time
import random


class City:
    def __init__(self, name):
        self.name = name
        self.streets = []
        self.log = []

    def writeLog(self, message):
        self.log.append(message)

class Street:
    def __init__(self,name):
        self.name = name
        self.buildings = []
        self.log = []

    def addBuilding(self,name, numOfFloors, numberOfElevators):
        self.buildings.append(Building(name, numOfFloors, numberOfElevators))

    def writeLog(self,logLine):
        self.log.append(logLine)

class Building:
    def __init__(self,name,numOfFloors,NumberOfElevators):
        self.name = name
        self.Floors = []
        self.Elevators = []
        self.Totalsteps = 0
        self.numOfFloors = numOfFloors
        self.NumberOfElevators = NumberOfElevators
        self.Log = []

        for x in range(1, self.numOfFloors+1):
            self.AddFloor(x)

        for x in range(1, self.NumberOfElevators+1):
            self.AddElevator(x)

    def AddFloor(self,name):
        self.Floors.append(Floor(name))

    def AddElevator(self,name):
        self.Elevators.append(Elevator(name, self.numOfFloors))

    def scheduleElevators(self):
        for floor in self.Floors:
            if floor.iscallButtonPressed() and floor.isScheduled != True and floor.doorsAreOpen != True:
                for elevator in self.Elevators:
                    if elevator.isIdle:
                        floor.writeLog("F%s: scheduled E%s which is currently on F%s" % (floor.name,elevator.name,elevator.currentFloor))
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
            print("***** F%s: log *****" % Floor.name)
            for Line in Floor.Log:
                print(Line)
            print("\n")

    def writeLog(self,LogLine):
        self.Log.append(LogLine)

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
        elevator.writeLog("E{} is currently on F{}, and is scheduled for F{}".format(elevator.name, elevator.currentFloor, self.name))
        self.writeLog("E{} is currently on F{}, scheduled for F{}".format(elevator.name, elevator.currentFloor, self.name))

    def callButtonPressed(self, UpOrDown,FloorsInBuilding):
        self.isScheduled = False

        if self.name == 1:
            self.upCallButtonIsOn = True
            self.writeLog("F%s: up button was pressed" % (self.name))
            return

        if self.name == FloorsInBuilding:
            self.downCallButtonIsOn = True
            self.writeLog("F%s: down button was pressed" % (self.name))
            return

        if UpOrDown == 'up':
            self.upCallButtonIsOn = True
            self.writeLog("F%s: up button was pressed" % (self.name))
            return

        if UpOrDown == 'down':
            self.downCallButtonIsOn = True
            self.writeLog("F%s: down button was pressed" % (self.name))
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
                        self.writeLog("Building: {} E{} arrived at calling F{} and opened its doors".format(building.name,self.name,self.callingFloor))
                        self.doorsAreOpen = True
                        openDoorsOnFloor(building,self.currentFloor,"F{}: E{} arrived on calling floor.".format(self.callingFloor,self.name))
                        return
                    else:
                        chooseDestinationfloor(self,building)
                        closeDoorsOnFloor(building,self.currentFloor,"F{}: Destination F{} was selected in E{} for building: {}".format(
                            self.currentFloor,self.destinationFloor,self.name, building.name))
                        turnCallButtonOff(self, building)
                        self.doorsAreOpen = False
                        self.isInTransitTocallingFloor = False
                        self.isInTransitTodestinationFloor = True
                        self.writeLog("E%s closed its doors on calling F%s: and is now headed to F%s:" % (self.name,self.currentFloor,self.destinationFloor))
                        return

            if self.isInTransitTodestinationFloor:
                if self.currentFloor == self.destinationFloor:
                    if self.doorsAreOpen != True:
                        self.doorsAreOpen = True
                        self.writeLog("E%s arrived at destination F%s: and opened its doors" % (self.name,self.destinationFloor))
                        openDoorsOnFloor(building,self.currentFloor,"F%s: E%s arrived on destination floor. Called from F%s:" % (self.currentFloor, self.name, self.callingFloor))
                        return
                    else:
                        closeDoorsOnFloor(building, self.currentFloor,None)
                        self.doorsAreOpen = False
                        self.isInTransitTodestinationFloor = False
                        self.writeLog("E%s closed its doors on destination F%s: and is now Idle" % (self.name,self.currentFloor))
                        self.transitionFromActiveToIdle(building)
                        return

            if self.direction() == "up":
                self.currentFloor += 1
                self.writeLog("E%s moved UP to F%s:" % (self.name,self.currentFloor))
                self.steps += 1

            if self.direction() == 'down':
                self.currentFloor -= 1
                self.writeLog("E%s moved DOWN to F%s:" % (self.name,self.currentFloor))
                self.steps += 1



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




class SkyScraper(Building):
    def __init__(self):
        pass

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
            floor.writeLog("F%s: doors opened" % (floor.name))

def closeDoorsOnFloor(building,targetFloor,InfoMessage):
    for floor in building.Floors:
        if floor.name == targetFloor:
            if InfoMessage != None:
                floor.writeLog(InfoMessage)
            floor.doorsAreOpen = False
            floor.writeLog("F%s: doors closed" % (floor.name))

def turnCallButtonOff(Elevator, building):
    for floor in building.Floors:
        if floor.name == Elevator.currentFloor:
            if Elevator.currentFloor < Elevator.destinationFloor:
                floor.upCallButtonIsOn = False
                floor.writeLog("F%s: Up call button is off" % (floor.name))

            if Elevator.currentFloor > Elevator.destinationFloor:
                floor.downCallButtonIsOn = False
                floor.writeLog("F%s: Down call button is off" % (floor.name))

def chooseDestinationfloor(elevator, building):
    Randomfloor = None
    for floor in building.Floors:
        if floor.name == elevator.currentFloor:
            if floor.upCallButtonIsOn:
                RandomFloor = getRandomFloor(elevator.currentFloor,building.numOfFloors,elevator.currentFloor)
                break

            if floor.downCallButtonIsOn:
                RandomFloor = getRandomFloor(1,elevator.currentFloor,elevator.currentFloor)
                break

    elevator.destinationFloor = RandomFloor
    elevator.writeLog("E%s is currently on F%s selected F%s as destination floor" % (elevator.name,elevator.currentFloor,elevator.destinationFloor))

def createBuilding(buildingAddress,floorsInBuilding,numOfElevators):
        return Building(buildingAddress,floorsInBuilding,numOfElevators)


myCounter = 0


def main():
    random.seed()
    ##   Create some streets

    # Create a street
    arguello = Street('Arguello Place')

    # build some buildings on the street
    arguello.addBuilding('3001',10,1)
    arguello.addBuilding('2364',10,2)
    arguello.addBuilding('7000',20, 2)

    # create another street
    conq = Street('Conquestador')

    # build some buildings for this street
    conq.addBuilding('100', 10, 1)
    conq.addBuilding('6244', 10, 2)
    conq.addBuilding('8000', 20, 2)

    # create a city
    sc = City('Santa Clara')

    # add some streets to the city
    sc.streets.append(arguello)
    sc.streets.append(conq)


    # start the simulations for each building on each street in the city
    for street in sc.streets:

        print()
        print()
        print("Starting elevator simulation for city: {}\n".format(sc.name))
        # create the buildings on the street
        for building in street.buildings:

            building.writeLog("Building Name = {}".format(building.name))
            building.writeLog("Bringing all Elevators to Idle. Starting Simulation on Building {}".format(building.name))
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
                    building.writeLog("All Elevators are now Idle on building {}.".format(building.name))
                    break

            for elevator in building.Elevators:
                elevator.transitionFromIdleToOutOfService(building)
                elevator.writeLog("Total Elevator E{} steps = {}".format(elevator.name, elevator.steps))

            building.writeLog("Total elevator steps for building {} = {}".format(building.name,building.Totalsteps))


        print("**** Street name = {} ****\n".format(street.name))
        for building in street.buildings:
            building.printLogs()

        sc.writeLog("Simulation ended for city {}". format(sc.name))

    print("Simulation Ended.")
if __name__ == "__main__":
    main()



