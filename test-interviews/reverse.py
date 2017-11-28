
# def my_reverse_print(foo_list):
#
#     if not foo_list: return
#
#     size = len(foo_list) - 1
#     for item in foo_list:
#
#         print(foo_list[size])
#         size -= 1
#     # reverse_print(foo_list[-1])

class Mine:
    def recur(self, num):
        print(num, end="")
        if num > 1:
            print(" * ",end="")
            return num * self.recur(self, num-1)
        print(" =")
        return 1

def main():
    # a = Mine()
    print(Mine.recur(Mine, 10))


def reverse_print(foo_list, size=None):

    if not foo_list: return

    if size is None:
        size = len(foo_list) - 1

    print(foo_list[size])

    if size != 0:
        size -= 1
        reverse_print(foo_list, size)

def bubbleSort(numbers):

    if not numbers: return
    sz = len(numbers) - 1
    j = 0

    for i in range(0, sz):
        j=0
        while j < sz:
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
            j+=1

    return numbers
def sortWithSkip(numbers, skip):

    if not numbers: return

    print(numbers)

    sort = []
    replace = []

    for i, n in enumerate(numbers):
        if n != skip:
            sort.append(numbers[i])
            replace.append(i)

    bubbleSort(sort)

    j = 0
    for i in replace:
        numbers[i] = sort[j]
        j += 1


    print(numbers)


def bubbleSortSkip(numbers, skip):

    if not numbers: return
    sz = len(numbers) - 1
    j = 0

    for i in range(0, sz):
        j=0
        while j < sz:
            # if the list has only 2 elements then swap if the last element isn't -1
            if sz == 1:
                if numbers[j+1] == skip: break
                else:
                    if numbers[j] > numbers[j+1]:
                        numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                        break
            # check to see if we have a skip in the next element
            if numbers[j+1] == skip:

                #determine how many skips are in a row before we handle a swap condition
                x = j+1
                while numbers[j+x] == skip:
                    x += 1

                # x is the number of skips in a row
                if numbers[j] > numbers[x]:
                    numbers[j], numbers[x] = numbers[x], numbers[j]

                # adjust the conditions
                j += x
                sz -= x
            else:
                if numbers[j] > numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                j+=1

    print(numbers)

class Reverse:
    def __init__(self):
        self.size = None

    def recur(self, list):
        self.size = len(list)
        print(self.list[self.size])
        if self.size != 0:
            self.size -= 1
            return self.recur(self, )

def main():
    s = 'azbeggha'
    count = 0
    i = 0
    tmp = ''
    next = ''
    alpha = ''
    print(len(s))
    for c in s:
        next = s[i+1]

        if c <= next:
            tmp += c
            i+=1
        else:
            if c <= next: tmp += c
            if len(tmp) > len(alpha):
                alpha = tmp
                if c <= next:
                    alpha[len(alpha)] = c
                tmp = ''
            i+=1

        if i == len(s) -1:
            break
    print(alpha)
    # for i in range(len(s) - 2) :
    #
    #     tmp = s[i:i+3]
    #     if tmp == 'bob':
    #         count += 1
    # print(count)



    # # foo_list = ['1']
    # # foo_list = []
    # size = len(foo_list) - 1
    # list_of_numbers = [-1,2,1,7,-1,100,16,-1,-1]
    # list_of_numbers = [5,4,3,2,1]
    # list_of_numbers = [9,8,7,6,5,-1,4,3,2,1,0]
    # sortWithSkip(list_of_numbers, 5)
    # print(bubbleSort(list_of_numbers))
    # foo_list = ['a','b','c','d', 'e', '1', '2']

    # reverse_print(foo_list)


if __name__ == "__main__": main()
# global
size = None