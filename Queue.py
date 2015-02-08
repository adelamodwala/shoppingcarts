from node import *

class Queue:
    '''
    Define a Queue ADT with a LIFO structure.
    '''
    
    def __init__(self):
        '''
        Constructor for Queue data type with initialized empty list.
        '''
        self.queue = []
        
    def __str__(self):
        '''
        String reperesentation of Queue object.
        '''
        if self.queue == []:
            return '{}'
        s = '{'
        for item in self.queue:
            s += str(item) + ', '
        s = s[:-2] + '}'
        return s
        
    def push(self, cart):
        '''
        Push a new element at the end of the queue.
        '''
        self.queue.append(cart)
        
    def size(self):
        '''
        Get length of the queue.
        '''
        return(len(self.queue))
        
    def pop(self):
        '''
        Pop the end of the queue (FILO)
        '''
        x = self.queue[-1]
        self.queue = self.queue[:-1]
        return(x)
    
    def remove(self, n):
        '''
        Remove the item at index n, n in 0 to len(self.queue)-1.
        '''
        if n < self.size():
            x = self.queue[n]
            self.queue = self.queue[:n] + self.queue[n+1:]
            return x
    
    def get_ind(self, node):
        '''
        Return the index of the node in Queue.
        '''
        count = 0
        for item in self.queue:
            if node == item:
                return count
            count += 1

class Matrix:
    '''
    The class for a list of Queue objects (i.e. our trolley database).
    '''
    
    def __init__(self, N=0, M=0):
        '''
        Constructor to initialize N Queues each with M nodes.
        '''
        d = {}
        for k in range(1, N+1):
            d[k] = Queue()                  #Create dictionary of queues with
            for l in range(1, M+1):         # queue number as key
                d[k].push(Node(i=k, j=l))
        self.d = d
    
    def __str__(self):
        '''
        String representation of Matrix.
        '''
        if self.d.keys() == []:
            return '{}'
        else:
            s = '{'
            for item in self.d.keys():
                s += str(self.d[item]) + '\n'
            s = s + '}'
            return s
    
    def pop(self, lst):
        '''
        Pop the last element of the queue indexed at lst.
        '''
        car = self.d[lst].pop()
        car.out = True
        return car

    def push(self, lst, cart):
        '''
        Push the node object cart into the Matrix object at queue indexed at
        lst.
        '''
        cart.out = False
        cart.timestamp = cart.returnt = 0
        self.d[lst].push(cart)
        
    def getsizes(self):
        m = {}
        for k in self.d.keys():
            m[k] = self.d[k].size()
        return m
    
if __name__ == '__main__':
    X = Matrix(3,5)
    print X
    cart = X.pop(2)
    print cart
    print X
    #X.push(2,cart)
    #print X