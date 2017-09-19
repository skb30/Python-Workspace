import datetime

# using a dictionary instead of a switch statement
class Specials:
    def __init__(self):

        self.weekly_specials = {'Sunday': 'spinach',
                           'Monday': 'mushroom',
                           'Tuesday': 'pepperoni'}


    def get_special(self, today):
        print "Today's special is: "  + self.weekly_specials[today]

def main():
    s = Specials()
    s.get_special("Sunday")
    m = Specials()
    m.get_special("Monday")
    t = Specials()
    t.get_special("Tuesday")

if __name__ == "__main__":
  main()