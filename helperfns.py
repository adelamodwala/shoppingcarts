from Queue import *
from node import *
import random
import operator

M = 100		#Number of trolleys in each queue
N = 4		#Number of queues
gamma = 25 	#Departure rate of carts per time period such that rho < 1
alpha = 20	#Arrival rate of carts per hour
lam = 1

def weighted_choice(weights): 
    '''
    Return an index from a list given the weights of said list. Courtesy of     
    http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/#id4
    '''
    totals = []           
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

def outweights(out):
    '''
    Get weights for the Out Queue based on smallest return time being given
    the largest weight i.e. probability of returning.
    '''
    weights = [0]*out.size()
    if out.size() > 0:
        weights = [0]*out.size()
        m = 0
        for cart in out.queue:
            weights[m] = 1/cart.returnt
            m += 1
        weights = [x / sum(weights) for x in weights]
    return weights
    
def return_aban(Aban, X):
    '''
    Return all abandoned carts based on the weights given to the queues 
    in the cart database.
    '''
    if Aban.size() > 0:
        sizes = X.getsizes()
        sizes = sorted(sizes.iteritems(), key=operator.itemgetter(1))
          #Get sorted tuples based on number of elements in each queue,
          # from smallest to largest
        tofill = []
        for tup in sizes:
            x = (tup[0],tup[1],M-tup[1])
            tofill.append(x)
        for T in range(N):
            for S in range(tofill[T][2]):
                if Aban.size() > 0:
                    X.push(sizes[T][0], Aban.pop())
                    
                    
def newarrivaltime():
    return random.expovariate(alpha)

def newdeparturetime():
    return random.expovariate(gamma)

def newbatchreturntime():
    return random.expovariate(lam)

def depweight(Q):
    '''
    Compute weights for queues for departure of next trolley, Q is a list of
    trolley counts for X.
    '''
    if sum(Q) == 0:
        return Q
    return [(float(x)/sum(Q)) for x in Q]

def count_zero(Q):
    '''
    Return the count of item that happen to be zero in list Q.
    '''
    c = 0
    for i in range(len(Q)):
        if Q[i] == 0:
            c += 1
    return c

def count_M(Q):
    '''
    Return the count of item that happen to be M in list Q.
    '''
    c = 0
    for i in range(len(Q)):
        if Q[i] == M:
            c += 1
    return c


def arrweight(Q):
    '''
    Compute weights for queues for arrival of next trolley. Based on the
    assumption that queues with larger number of trolleys will usually
    get more trolleys due to convenience.
    '''
    l = len(Q)
    weights = [0.0]*l
    sumtot = 0
    for i in range(l):
        if Q[i] < M:
            weights[i] = Q[i]
            sumtot = sumtot + weights[i]
    if count_zero(Q) == l - count_M(Q):  
        #If queues only have lenghts 0 and M, give equal weight to those with 0
        for i in range(l):
            if Q[i] == 0:
                weights[i] = 1.0/count_zero(Q)
        return weights
    if sumtot == 0:
        return weights
    return [float(x)/sumtot for x in weights]

def getsortdict(d):
    '''
    Return a sorted list of values from dictionary d where sorting is based
    on the keys.
    '''
    Q = sorted(d.iteritems(), key=operator.itemgetter(0))
    Y = []
    for tup in Q:
        Y.append(tup[1])
    return Y
    
if __name__ == '__main__':
    X = Matrix(3,5)
    print X
    Aban = Queue()
    Aban.push(X.pop(2))
    Aban.push(X.pop(2))
    Aban.push(X.pop(3))
    print Aban
    #return_aban(Aban, X)
    print Aban
    print X
    for cart in Aban.queue:
        cart.returnt = newarrivaltime()