def fib(n):
    a = 0
    b = 1
    f = 0
    for i in range(n):
        f = a + b
        a = b
        b = f
    return f

def rfib(n, a=0, b=1, f=0):
    if n == 0:
        return f
    else:
        f = a + b
        a = b
        b = f
        n -= 1
        return rfib(n, a ,b, f)

def fibx(n):
    if n == 0 or n == 1:
        return 1

    else:
        return fibx(n-1) + fibx(n-2)

def main():

    for n in range(40):

        # print(fib(n))
        print(rfib(n))
        # print(fibx(n))

if __name__ == '__main__':
   main()