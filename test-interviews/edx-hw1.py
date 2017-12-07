
def main():
    epsilon = 50
    answer = ''
    guess = 50
    print("Plesae think of a number between 0 and 100 ")
    limit = 0;


    while True:
        answer = input("Is your secert number {} ? ".format(guess))
        if answer == 'c':
             break
        elif answer == 'h':
            guess = guess - limit
            x = guess // 2
            guess = guess - x
            limit = guess
        else:
            guess = guess + limit
            x = guess // 2
            guess = guess + x
            limit = guess
        print("guess is: {}".format(guess))






if __name__ == "__main__": main()