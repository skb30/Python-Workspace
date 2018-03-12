import string


def getCipherCode(char, key):
    aChar = ord(char)
    aKey  = ord(key)
    index = aKey - aChar

    # create a pointer to the Key so that we offset from it
    code = aKey + index

    # check to see if we wrap
    if code > ord('z'):
        code = code - ord('z')
        code = ord('a') + code
    elif code < ord('a'):
        # figure out the difference
        code = code - ord('a')
        code = ord('z') + code
    return chr(code)

def cipherString(targetString, keyString):
    targetStringLen   = len(targetString)
    keyStringLen      = len(keyString)
    targetStringIndex = 0
    keyStringIndex = 0
    encodedString = ""

    while True:

        # boundry to exit the loop
        if targetStringIndex == targetStringLen:
            break
        # boundry to reset keyStringIndex
        if keyStringIndex == keyStringLen:
            keyStringIndex = 0

        key = keyString[keyStringIndex]

        c = targetString[targetStringIndex]

        if c >= 'a' and  c <= 'z':
            encodedString += getCipherCode(c,key)
            targetStringIndex += 1
            keyStringIndex += 1
            continue

        encodedString += ' '
        targetStringIndex += 1

    return encodedString

print ("hi1")
print(cipherString("a very good day, I say", "scooter"))
print ("hi2")

#
# print(getCipherCode('a', 'a')) # should print a
# print(getCipherCode('b', 'c')) # should print a
# print(getCipherCode('z', 'b')) # should print a



