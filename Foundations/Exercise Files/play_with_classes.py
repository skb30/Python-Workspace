
class CalcSpeed:
    # def __init__(self,distance,time):
    #     self.distance = distance
    #     self.time = time
    #     self.speed = 0

    def theSpeed(self, distance, time):

#     print str(timedelta(minutes=timeToAirport))[:-3]
        print "Calculating the speed..."
        minsToHours = 60 / time
        self.speed = minsToHours * distance
        return str(self.speed)



def main():
    x = CalcSpeed()
    print x.theSpeed(80,80)


if __name__ == "__main__":
  main()
