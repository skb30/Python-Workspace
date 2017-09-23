#!/usr/bin/python3

class Duck:
     # example of a class that might be used as getting and setting config params
    def __init__(self, **kwargs):
        # self._ is used to signify the attribute will be accessed by using only accessor methods

        # create a dict attribute
        self._variables = kwargs

    # set the dict with key/value pair passed as an arg
    def set_variables(self, k, v):

        self._variables[k] = v

    def get_variables(self, k):

        return  self._variables[k]

    def quack(self):
        print('Quaaack!', self._v)

    def walk(self):
        print('Walks like a duck.', self._v)

def main():
    frank = Duck(id = 777)
    donald = Duck(color = 'black')
    print(donald.get_variables('color'))
    donald.set_variables('color', 'red')
    print(donald.get_variables('color'))
    donald.set_variables('id', 500)
    print(donald.get_variables('id'))
    print(frank.get_variables('id'))



if __name__ == "__main__": main()
