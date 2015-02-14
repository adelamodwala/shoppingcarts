from parameters import *
from helperfns import *
from pylab import *
import random
import operator
import numpy

if __name__ == '__main__':

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
		
		TARGETTIME = 10000 # overall run of the Monte Carlo simulation
		MAXGRAPH = M # Max number of trolleys per queue
		dobatches = True
		timetodepart = newdeparturetime() 
		timetoarrive = 0 
		timeremaining = TARGETTIME # Initialize countdown of time remaining
		nextbatchtime = [newbatchreturntime(), timeremaining]
		thetimesQ = {} # dictionary with keys being the queue
									 # index whose values are lists that record 
									 # the time spent in a paricular state
									 # e.g. thetimesQ[2] = [124,32,14, ..., 19] where
									 # each item represents the time spent, thetimesQ[2][j],
									 # of Queue 2 with j carts
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
								Q = getsortdict(Q) # get a list of values sorted 
																	 # by queue index in X
								dchosen = weighted_choice(depweight(Q)) # get queue index in X 
																												# to pop from by weights
								cart = X.pop(dchosen+1)
								cart.returnt = timetoarrive
								cart.timestamp = timeremaining
								Out.push(cart)
								trace.append(sum(X.getsizes().values())) # total carts remaining
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
		batch_label = 'Batches' if dobatches else 'No Batches'
		x = arange(0,M+1,1)
		for j in thefracs.keys():
		   plot(x, thefracs[j], label='queue ' + str(j))
		xlabel('%')
		ylabel('K')
		title('Percent time spent with K carts, ' + batch_label)
		legend(loc='upper left')
		savefig('plots/queue_records.png')
		close()

		y = arange(0,len(trace),1)
		plot(y,trace)
		xlabel('Iteration')
		ylabel('X.size')
		title('Total number of carts at each iteration, ' + batch_label)
		savefig('plots/total_carts.png')
		close()
				
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
	print 'mean: ' + str(Jmean)
	#print Jstd

