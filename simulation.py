from helperfns import *
from pylab import *
import random
import operator
import numpy

rep = 1
probvec = []
for z in range(rep):
    #This loop is just for repeated simulations to check for consistency

    X = Matrix(N, M)  
        #The cart 'database' containing the queues for arrival and departure
    Out = Queue()     
        #Initialize an empty list to record all trolleys that are currently 
        # out but not abandoned
    Aban = Queue()    
        #Initialize an empty list of trolleys that have been abandoned 
        #(when return time has expired)
    
    TARGETTIME = 10000
    MAXGRAPH = M 
    dobatches = False
    timetodepart = newdeparturetime() 
    timetoarrive = 0 
    timeremaining = TARGETTIME 
    nextbatchtime = [newbatchreturntime(), timeremaining]
    thetimesQ = {}
    trace = []
    for i in range(1,N+1):
        thetimesQ[i] = [0]*(M+1)
    

    while timeremaining > 0:
        
        if Aban.size() > 0 and nextbatchtime[1] - timeremaining > nextbatchtime[0]\
           and dobatches:
            #We will now return all the abandoned trolleys to the queues
            return_aban(Aban, X)
            nextbatchtime = [newbatchreturntime(), timeremaining]
        
        if timeremaining <= timetodepart and timeremaining <= timetoarrive:
            # Finish without any further events.
            get = X.getsizes()        
            for i in range(1, N+1):
                if get[i] <= MAXGRAPH:
                    thetimesQ[i][get[i]] += timeremaining
            timeremaining = 0
        elif sum(X.getsizes().values()) == 0 or timetodepart < timetoarrive:
            # Await next trolley departure.
            timeremaining = timeremaining - timetodepart
            timetoarrive = timetoarrive - timetodepart
            get = X.getsizes()        
            for i in range(1, N+1):
                if get[i] <= MAXGRAPH:
                    thetimesQ[i][get[i]] += timetodepart
            if sum(X.getsizes().values()) > 0:       
                # there are trolleys still in the queues
                timetoarrive = newarrivaltime()
                Q = X.getsizes()
                Q = getsortdict(Q)
                dchosen = weighted_choice(depweight(Q))
                #Q[dchosen] -= 1
                cart = X.pop(dchosen+1)
                cart.returnt = timetoarrive
                cart.timestamp = timeremaining
                Out.push(cart)
                trace.append(sum(X.getsizes().values()))
            timetodepart = newdeparturetime()
        else:    
            # Await next trolley arrival.
            timeremaining = timeremaining - timetoarrive
            timetodepart = timetodepart - timetoarrive
            get = X.getsizes()        
            for i in range(1, N+1):
                if get[i] <= MAXGRAPH:
                    thetimesQ[i][get[i]] += timetoarrive
            if sum( X.getsizes().values()) < N*M and Out.size() > 0:
                Q = X.getsizes()
                Q = getsortdict(Q)            
                achosen = weighted_choice(arrweight(Q))
                w = outweights(Out)
                cart = Out.remove(weighted_choice(w))
                X.push(achosen+1, cart)
                trace.append(sum(X.getsizes().values()))
            timetoarrive = newarrivaltime()
        if Out.size() > 0 and dobatches:
            for item in Out.queue:
                if item.timestamp - timeremaining > item.returnt:
                    m = Out.get_ind(item)
                    Aban.push(Out.remove(m))
            trace.append(sum(X.getsizes().values()))
                
    #print X.getsizes()
    #print thetimesQ
    thefracs = {}
    for i in thetimesQ.keys():
        thefracs[i] = [x/TARGETTIME for x in thetimesQ[i]]
    #print thefracs
    #x = arange(0,M+1,1)
    #for j in thefracs.keys():
    #    plot(x, thefracs[j])
    y = arange(0,len(trace),1)
    plot(y,trace)
        
    #Computing P(|Q_j|>0):
    theprobs = [0]*N
    for i in range(1, N+1):
        theprobs[i-1] = sum(thefracs[i][1:])
    probvec.append(theprobs)
    
J = numpy.array(probvec)
Jmean = numpy.mean(J, axis = 0)
    #Get mean across columns (i.e. between runs, not within runs)
Jstd = numpy.std(J, axis = 0)
    #Get standard error across columns (i.e. between runs, not within runs)
print J
print numpy.sum(J, 1) 
#print Jmean
#print Jstd

