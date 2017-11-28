def main():
    myList = [100,2,13,24]
    # myList = []
    # myList = [1]

    max = max_value(myList)
    min = min_value(myList)
    avg = mean(myList)


    reversed = reverse_list(myList)
    for c in myList:
        print(c)

    print(max, min, avg)


def mean(list):

    if len(list) == 0: return None

    m = 0
    for number in list:
        m += number
    mean = m / len(list)
    return mean


def max_value(list):

    if len(list) == 0: return None

    m = 0

    for number in list:
        if number > m:
            m = number

    return m

def min_value(list):

    if len(list) == 0: return None

    m = list[0]

    for number in list:
        if number < m:
            m = number

    return m


def reverse_list(list):

    if len(list) == 0: return None

    begin = 0
    end   = len(list) - 1

    while begin < end:
        # swap
        list[begin], list[end] = list[end], list[begin]
        begin += 1
        end   -= 1

    return list

if __name__ == "__main__":
    main()