

def calculate(word):
    alphabet = {}
    value    = 0
    sum      = 0

    # create the dictionary using the ascii range
    for letter in range(97, 123):
        alphabet[chr(letter)] = value
        value += 1

    for letter in word:
        sum += alphabet[letter]

    print ("The value of {} is {}".format(word, sum))

def main():
    print ("Find the dollor words")
    calculate("zander")


if __name__ == "__main__":
  main()