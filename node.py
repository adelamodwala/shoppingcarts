## Create the shopping cart class

class Node:
    '''
    Define the Node class as shopping carts.
    '''
    
    def __init__(self, i=0, j=0, timestamp=0, returnt=0, out=False):
        '''
        Constructor for the Node class.
        '''
        self.i = i
        self.j = j
        self.timestamp = timestamp
        self.returnt = returnt
        self.out = out
        
    def __cmp__(self, other):
        '''
        Compare equality of nodes by checking if same indices, otherwise return
        False.
        '''
        if self.i == other.i and self.j == other.j:
            return 0
        else:
            return -1
        #We will only ever use the inequality since greater or less than does 
        # not make any sense for our purposes.
    
    def __str__(self):
        '''
        Return a string representation of node object.
        '''
        s = '[i:' + str(self.i) + ', j:' + str(self.j) + ', timestamp:' + \
          str(self.timestamp) + ', returnt:' + str(self.returnt) + ', out:' + \
          str(self.out) + ']'
        return(str(s))
        
if __name__=='__main__':
    cart1 = Node(1,1)
    cart2 = Node(3,4)
    cart3 = Node(3,4)
        
        