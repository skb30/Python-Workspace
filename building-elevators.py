import sys
import time
import random


class City:
    def __init__(self, name):
        self.name = name
        self.streets = []
        self.log = []

    # linkage to children
    def addStreet(self, name):
        self.streets.append(Street(name))
        return self.streets[-1]

    def writeLog(self, message):
        self.log.append(message)


    def printLogs(self):
        for line in self.log:
            print(line)

        print()

        for street in self.streets:
            for line in street.log:
                print(line)

            print()

            for building in street.buildings:
                for line in building.log:
                    print(line)

                print()

                for elevator in building.elevators:
                    for line in elevator.log:
                        print(line)

                    print()

                for floor in building.floors:
                    for line in floor.log:
                        print(line)

                    print()

        print()


class Street:
    def __init__(self,name):
        self.name = name
        self.buildings = []
        self.log = []
        self.numberOfExpressElevators = 1
    # create children objects
    def addBuilding(self,name, numberOfFloors, numberOfElevators,isHighRise):
        if isHighRise:
            self.buildings.append(HighRiseBuilding("{} High-Rise ".format(name), numberOfFloors, numberOfElevators,self.numberOfExpressElevators))
        else:
            self.buildings.append(Building(name, numberOfFloors, numberOfElevators))
        return self.buildings[-1]

    def writeLog(self,logLine):
        self.log.append(logLine)



class Building(object):
    def __init__(self,name,numberOfFloors,numberOfElevators):
        self.name = name
        self.floors = []
        self.elevators = []
        self.totalSteps = 0
        self.numberOfFloors = numberOfFloors

        self.numberOfElevators = numberOfElevators
        self.log = []

        for x in range(1, self.numberOfFloors+1):
            self.addFloor(x)

        for x in range(1, self.numberOfElevators+1):
            self.addElevator(x)
    @property
    def getNumberOfFloors(self): return len(self.floors)

    def listElevators(self):
        print("List of elevators in building {}".format(self.name))
        for elevator in self.elevators:
            print("Elevator {} current floor is: {}".format(elevator.name, elevator.currentFloor))

    def addFloor(self,name, floorID = None):
        self.floors.append(Floor(name, floorID))

    def addElevator(self,name):
        self.elevators.append(Elevator(name, self.numberOfFloors))

    def scheduleElevators(self):
        for floor in self.floors:
            # if the call button is pressed, the floor isn't scheduled and the doors are closed
            if floor.iscallButtonPressed() and floor.isScheduled != True and floor.doorsAreOpen != True:
                # find and schedule the first idle elevator
                for elevator in self.elevators:
                    if elevator.isIdle:
                        floor.writeLog("F{} scheduled E{} which is currently on F{}".format(floor.name,elevator.name,elevator.currentFloor))

                        # moved the following code out of floor.scheduleElevator(elevator). Prevents us from breaking
                        # Darrell's rule of object destruction. Don't pass object reference to another object because
                        # they will then have the keys to the castle.


                        # state  changes to floor and elevator
                        floor.isScheduled = True
                        elevator.callingFloor = floor.name
                        elevator.isInTransitTocallingFloor = True
                        elevator.isInTransitTodestinationFloor = False

                        # set the floor's next elevator
                        if floor.upCallButtonIsOn:
                            floor.nextUpElevator = elevator.name
                        if floor.downCallButtonIsOn:
                            floor.nextDownElevator = elevator.name

                        # change the elevator's state to active
                        elevator.transitionFromIdleToActive()
                        elevator.writeLog("E{} is currently on F{}, and is scheduled for F{}".format(elevator.name,
                                                                                                     elevator.currentFloor,
                                                                                                     floor.name))
                        # do it again for the next elevator in the list.
                        break



    def allElevatorsAreIdle(self):
        for elevator in self.elevators:
            if elevator.isActive:
                return False

        return True

    def allCallButtonsAreOff(self):
        for Floor in self.floors:
            if Floor.upCallButtonIsOn or Floor.downCallButtonIsOn:
                return False

        return True
    @property
    def getNextFloor(self): return len(self.floors) + 1

    # all the elevators have been scheduled, let's go move them.
    def stepElevators(self):
        for elevator in self.elevators:
            if elevator.isActive:
                if elevator.isInTransitTocallingFloor:
                    if elevator.currentFloor == elevator.callingFloor:
                        if elevator.doorsAreOpen != True:
                            elevator.writeLog(
                                "E{} arrived at calling F{} and opened its doors. Origin was F{}".format(elevator.name,
                                                                                                         elevator.callingFloor,
                                                                                                         elevator.originFloor))
                            elevator.doorsAreOpen = True
                            openDoorsOnFloor(self,elevator.currentFloor,
                                             "F{} E{} arrived on calling floor F{}. Origin was F{}".format(
                                                 elevator.currentFloor, elevator.name, elevator.callingFloor, elevator.originFloor))
                            return
                        else:
                            chooseDestinationfloor(self, elevator)
                            closeDoorsOnFloor(self, elevator.currentFloor,
                                              "F{} Destination F{} was selected in E{}".format(
                                                  elevator.currentFloor, elevator.destinationFloor, elevator.name))
                            turnCallButtonOff(elevator, self)
                            elevator.doorsAreOpen = False
                            elevator.isInTransitTocallingFloor = False
                            elevator.isInTransitTodestinationFloor = True
                            elevator.writeLog(
                                "E{} closed its doors on calling F{} and is now headed to F{}".format(elevator.name,
                                                                                                      elevator.currentFloor,
                                                                                                      elevator.destinationFloor))
                            return

                if elevator.isInTransitTodestinationFloor:
                    if elevator.currentFloor == elevator.destinationFloor:
                        if elevator.doorsAreOpen != True:
                            elevator.doorsAreOpen = True
                            elevator.writeLog(
                                "E{} arrived at destination F{} and opened its doors. Called from F{}. Origin was F{}".format(
                                    elevator.name, elevator.destinationFloor, elevator.callingFloor, elevator.originFloor))
                            openDoorsOnFloor(self, elevator.currentFloor,
                                             "F{} E{} arrived on destination floor F{}. Called from F{}. Originated at F{}.".format(
                                                 elevator.currentFloor, elevator.name, elevator.currentFloor, elevator.callingFloor,
                                                 elevator.originFloor))
                            return
                        else:
                            closeDoorsOnFloor(self, elevator.currentFloor, None)
                            elevator.doorsAreOpen = False
                            elevator.isInTransitTodestinationFloor = False
                            elevator.writeLog("E{} closed its doors on destination F{} and is now Idle".format(elevator.name,
                                                                                                           elevator.currentFloor))
                            elevator.transitionFromActiveToIdle(self)
                            return

                if elevator.direction() == "up":
                    elevator.currentFloor += 1
                    elevator.writeLog("E{} moved UP to F{}".format(elevator.name, elevator.currentFloor))
                    elevator.steps += 1
                    self.totalSteps += 1

                if elevator.direction() == 'down':
                    elevator.currentFloor -= 1
                    elevator.writeLog("E{} moved DOWN to F{}".format(elevator.name, elevator.currentFloor))
                    elevator.steps += 1
                    self.totalSteps += 1


    def printLogs(self):
        for Elevator in self.elevators:
            print("***** E{} log *****".formatElevator.name)
            for Line in Elevator.log:
                print(Line)
            print("\n")

        print("\n")

        for Floor in self.floors:
            print("***** F{} log *****".formatFloor.name)
            for Line in Floor.log:
                print(Line)
            print("\n")

    def writeLog(self,LogLine):
        self.log.append(LogLine)

class HighRiseBuilding(Building):

    def __init__(self, name, numberOfFloors, numberOfElevators, numberOfExpressElevators):
        self.numberOfFloors = numberOfFloors + 1
        super().__init__(name, self.numberOfFloors, numberOfElevators)

        self.numberOfExpressElevators = numberOfExpressElevators


        for x in range(1, self.numberOfExpressElevators):
            self.AddExpressElevator("xpress {}".format(x),self.numberOfFloors,numberOfElevators)

        # add a hilo pad floor to the high rise
        super().addFloor(super().getNextFloor,'hilo-pad')
        print("Building Name: {}has added Hilo-Pad floor {} ".format(name, super().getNumberOfFloors))


    def AddExpressElevator(self,name,numberOfElevators):
        self.elevators.append(ExpressElevator(name, self.numberOfFloors, numberOfElevators))



class Floor:
    def __init__(self,name, floorID=None):
        self.floorID = floorID
        self.name = name
        self.upCallButtonIsOn = False
        self.downCallButtonIsOn = False
        self.nextUpElevator = None
        self.nextDownElevator = None
        self.isScheduled = None
        self.doorsAreOpen = False
        self.log = []

    def iscallButtonPressed(self):
        if self.upCallButtonIsOn or self.downCallButtonIsOn:
            return True
        else:
            return False


    def callButtonPressed(self, UpOrDown,FloorsInBuilding):
        self.isScheduled = False

        if self.name == 1:
            self.upCallButtonIsOn = True
            self.writeLog("F{} up button was pressed".format(self.name))
            return

        if self.name == FloorsInBuilding:
            self.downCallButtonIsOn = True
            self.writeLog("F{} down button was pressed".format(self.name))
            return

        if UpOrDown == 'up':
            self.upCallButtonIsOn = True
            self.writeLog("F{} up button was pressed".format(self.name))
            return

        if UpOrDown == 'down':
            self.downCallButtonIsOn = True
            self.writeLog("F{} down button was pressed".format(self.name))
            return

    def writeLog(self,LogLine):
        self.log.append(LogLine)


class Elevator(object):
    def __init__(self, name, maxFloors):
        self.name = name
        self.isOutOfService = True
        self.isIdle = False
        self.isActive = False
        self.doorsAreOpen = False

        @property
        def currentFloor(self):
            return self.currentFloor

        @currentFloor.setter
        def setCurrentFloor(self, floorNumber):
            self.currentFloor = floorNumber

        self.currentFloor = getRandomFloor(1,maxFloors,0)

        self.isInTransitTodestinationFloor = False
        self.destinationFloor = 0

        self.isInTransitTocallingFloor = False
        self.callingFloor = 0

        self.originFloor = self.currentFloor

        self.log = []
        self.steps = 0

        # if isinstance(self, ExpressElevator):
        #     print("{} is an Express Elevator.".format(name))


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


    def transitionFromOutOfServiceToIdle(self,buildingName):
        if self.isOutOfService:
            self.isOutOfService = False
            self.isIdle = True
            self.writeLog("E{} transitioned from OutOfService to Idle. Currently on F{}".format(self.name,self.currentFloor))
        else:
            self.writeLog('E{} : transitionFromOutOfServiceToIdle: invalid state'.format(self.name))


    def transitionFromIdleToActive(self):
        if self.isIdle:
            self.isIdle = False
            self.isActive = True
            self.writeLog("E{} transitioned from Idle to Active".format(self.name))
        else:
            self.writeLog('E{} : transitionFromIdleToActive: invalid state'.format(self.name))

    def transitionFromActiveToIdle(self,building):
        if not (not self.isActive or self.isInTransitTocallingFloor) and not self.isInTransitTodestinationFloor:
            self.isIdle = True
            self.isActive = False
            self.originFloor = self.currentFloor
            self.writeLog("E{} transitioned from Active to Idle. Currently on F{}".format(self.name,self.currentFloor))
        else:
            self.writeLog('E{} : transitionFromActiveToIdle: invalid state'.format(self.name))

    def transitionFromIdleToOutOfService(self,building):
        if self.isIdle:
            self.isOutOfService = True
            self.isIdle = False
            self.writeLog("E{} transitioned from Idle to OutOfService. Currently on F{}. Total Steps = {}".format(self.name, self.currentFloor, self.steps))
        else:
            self.writeLog('E{} = transitionFromIdleToOutOfService: invalid state'.format(self.name))

    def writeLog(self,LogLine):
        self.log.append(LogLine)

class ExpressElevator(Elevator):

    def __init__(self, name, numberOfFloors, numberOfElevators):
        super().__init__(name, numberOfFloors)

    # override

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
    for floor in building.floors:
        if floor.name == targetFloor:
            if infoMessage != None:
                floor.writeLog(infoMessage)
            floor.doorsAreOpen = True
            floor.writeLog("F{} doors opened".format(floor.name))

def closeDoorsOnFloor(building,targetFloor,InfoMessage):
    for floor in building.floors:
        if floor.name == targetFloor:
            if InfoMessage != None:
                floor.writeLog(InfoMessage)
            floor.doorsAreOpen = False
            floor.writeLog("F{} doors closed".format(floor.name))

def turnCallButtonOff(Elevator, building):
    for floor in building.floors:
        if floor.name == Elevator.currentFloor:
            if Elevator.currentFloor < Elevator.destinationFloor:
                floor.upCallButtonIsOn = False
                floor.writeLog("F{} Up call button is off".format(floor.name))

            if Elevator.currentFloor > Elevator.destinationFloor:
                floor.downCallButtonIsOn = False
                floor.writeLog("F{} Down call button is off".format(floor.name))

def chooseDestinationfloor(building, elevator):

    Randomfloor = None
    for floor in building.floors:
        if floor.name == elevator.currentFloor:
            if floor.upCallButtonIsOn:
                RandomFloor = getRandomFloor(elevator.currentFloor,building.getNumberOfFloors,elevator.currentFloor)
                break

            if floor.downCallButtonIsOn:
                RandomFloor = getRandomFloor(1,elevator.currentFloor,elevator.currentFloor)
                break

    elevator.destinationFloor = RandomFloor
    elevator.writeLog("E{} is currently on F{} selected F{} as destination floor".format(elevator.name,elevator.currentFloor,elevator.destinationFloor))


def main():
    random.seed()

    myCity = City('Santa Clara')
    myCity.addStreet('Arguello Place')
    myCity.addStreet('Via Conquistador')

    # build the city
    for street in myCity.streets:
        myCity.writeLog("Street Created: {} in City: {}".format(street.name, myCity.name))
        # randomNumberOfBuildings = random.randint(2,5)
        randomNumberOfBuildings = 2
        for x in range(1,randomNumberOfBuildings):
            randomStreetNumber = random.randint(1000,9999)
            randomNumberOfFloors = random.randint(2,20)
            randomnumberOfElevators = random.randint(1,4)
            # changed to 1 and 0 for true and false
            isHighRise = chooseRandomValue(0,1)
            thisBuilding = street.addBuilding(randomStreetNumber, randomNumberOfFloors, randomnumberOfElevators, isHighRise)
            # thisBuilding = street.addBuilding(randomStreetNumber, 11, 1, 1)

            myCity.writeLog("Building Created: {} {} on {} street in {}, floors = {}, elevators = {}".format(thisBuilding.name,
                                                                                                             street.name,
                                                                                                             street.name,
                                                                                                             myCity.name,
                                                                                                             thisBuilding.numberOfFloors,
                                                                                                             thisBuilding.numberOfElevators))
    # start the simulation
    for street in myCity.streets:
        for building in street.buildings:
            building.writeLog("Building Name: {} {}, floors = {}, elevators = {}".format(building.name,street.name,building.getNumberOfFloors,building.numberOfElevators))
            building.writeLog("Building Name: {} {} - Starting Simulation - Bringing all Elevators to Idle.".format(building.name,street.name))

            # transistion all elevators to idle in this building
            for elevator in building.elevators:
                elevator.transitionFromOutOfServiceToIdle(building.name)
            # randomaly set  all the floors (in the building) call buttons to either up or down
            for floor in building.floors:
                floor.callButtonPressed(chooseRandomValue("up","down"),building.getNumberOfFloors)

            # start the simulation
            while True:
                # iterate thru each floor in the building scheduling an elevator
                building.scheduleElevators()
                # elevators have been scheduled

                building.stepElevators()
                if building.allElevatorsAreIdle() and building.allCallButtonsAreOff():
                    building.writeLog("Building Name: {} {} - All Elevators are now Idle".format(building.name, street.name))
                    break

            for elevator in building.elevators:
                elevator.transitionFromIdleToOutOfService(building)

            building.writeLog("Building Name: {} {} - Total elevator steps = {}".format(building.name, street.name, building.totalSteps))


    myCity.printLogs()


if __name__ == "__main__":
    main()


