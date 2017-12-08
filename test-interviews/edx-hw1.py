
def main():
    answer = ''
    low = 0
    high = 101

    print("Plesae think of a number between 0 and 100!")
    ans = (high + low) // 2
    print("Is your secret number {}?".format(ans))
    answer = input("Enter 'h' to indicate the guess is too high. Enter 'l'" +
                   " to indicate the guess is too low. Enter 'c' to indicate I guessed correctly.")

    while True:
        if answer == 'c':
             break
        elif answer == 'h':
            high = ans
        else:
            low  = ans
        ans = (high + low) // 2


        print("Is your secret number {}?".format(ans))
        answer = input("Enter 'h' to indicate the guess is too high. Enter 'l'" +
                       " to indicate the guess is too low. Enter 'c' to indicate I guessed correctly.")

if __name__ == "__main__": main()