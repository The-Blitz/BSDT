import os.path
import operator
import numpy
class Vertex:
    def __init__(self,key,w,p,fq):
        self.id = key
        self.connectedTo = {}
        self.word = w
        self.pos = p
        self.freq =fq

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + " " +str(self.word)+ " " + str(self.pos)  + " " + str(self.freq)

    def getConnections(self):
        return sorted(self.connectedTo.keys(),key=operator.attrgetter('pos','id'))

    def getId(self):
    	return self.id
    
    def getWord(self):
    	return self.word
    
    def getPos(self):
    	return self.pos

    def getFreq(self):
    	return self.freq

    def getWeight(self,nbr):
    	return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key,word,pos,freq):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,word,pos,freq)
        self.vertList[key+"-"+str(pos)] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,fword,fpos,ffreq,t,tword,tpos,tfreq,cost=0):
        if (f+"-"+str(fpos)) not in self.vertList:
            nv = self.addVertex(f,fword,fpos,ffreq)
        if (t+"-"+str(tpos)) not in self.vertList:
            nv = self.addVertex(t,tword,tpos,tfreq)
        self.vertList[f+"-"+str(fpos)].addNeighbor(self.vertList[t+"-"+str(tpos)], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(sorted(self.vertList.values(),key=operator.attrgetter('pos','id')))

    def generateMatrix(self):
        npages = len(self.vertList)
        auxMat = numpy.zeros((npages, npages))
        cont1=0
        for v in self:
        	cont2 =0
        	auxSum =0.0 # sum of all edges
        	for w in v.getConnections():
        		auxSum = auxSum + v.getWeight(w)
        	for w in self:
        	    if (w in v.getConnections()):
        	    	if(auxSum!=0):
        	    		auxMat[cont2][cont1] = v.getWeight(w) / auxSum
        	    cont2= cont2 + 1
        	cont1= cont1 + 1	
        return auxMat		
	
    def generateProbVector(self):
    	npages = len(self.vertList)
    	auxVect = numpy.zeros(npages)
    	auxSum =0.0 # sum of all frequencies
    	cont1 =0
    	for v in self:
    		auxSum = auxSum + (v.getFreq()*1.0)
		
    	for v in self:
    		if(auxSum !=0) :
    			auxVect[cont1] = (v.getFreq()*1.0) / auxSum
    		else:
    			auxVect[cont1] = 1.0/npages
    		cont1= cont1 + 1
    	return auxVect

    def pageRank(self,c = 0.85 , iterations =30): # c= damping factor
        ranks = {}
        rankList = []
        npages = len(self.vertList)
        
        mat = self.generateMatrix()
        probVector = self.generateProbVector()
        
        for v in range(npages):
        	rankList.append(1.0 / npages)
        
        for i in range(iterations):
            rankList = c * mat.dot(rankList) + (1-c) * probVector
    
        cont=0
        for v in self:
        	ranks[v] = rankList[cont]
        	cont = cont + 1
        return ranks
	
def dijkstra(graph, start):
	S = set()

	delta = dict.fromkeys(graph.getVertices(), 9999999)
	previous = dict.fromkeys(graph.getVertices(), None)
  
	delta[start] = 0
 
	while len(S) != graph.numVertices:
		
		vertex= min((set(delta.keys()) - S), key=delta.get)
		v = graph.getVertex(vertex)
		for w in v.getConnections():
			new_path = delta[v.getId()] + v.getWeight(w)
			if new_path < delta[w.getId()]:
				delta[w.getId()] = new_path
				previous[w.getId()] = v.getId()
		S.add(v.getId())	
	return (delta, previous)

def getDistanceSense(start, end):

	if(start == end ): 
		return 2 ; # error same vertex
	fileName  = 'Distances/' + start + '.txt'	
	if (os.path.exists(fileName)):
		#print("fileName exists")
		with open(fileName,'r',encoding='utf-8') as f:
			for line in f:
				line = line.split(' ')
				adja = line[0]
				dist = int (line[1])
				if (adja == end):
					ans = 1.0 / dist
					return ans
	return -1 # error not found
				
def getDistanceList(start,end,cond):
	ans = -1 #never found
	auxSum = 0;	freqAns = -1#never found
	freqI = 0 ; freqJ =0
	for i in range(len(start[0])):
		for j in range(len(end[0])):
			dist = getDistanceSense(start[0][i],end[0][j])
			ans = max(ans,dist)
			auxSum = auxSum + dist
			if(freqI<= start[1][i] and freqJ <= end[1][j]):
				freqI= start[1][i]
				freqJ= end[1][j]
				freqAns= dist
				
	auxSum = (auxSum) / ( len(start[0]) * len(end[0]))	
		
	if(cond==1):
		return (ans) # maximas relaciones
	elif(cond==2):
		return (auxSum) #mean
	elif(cond==3):
		return (freqAns) #frequency  
	return -1 # error never found


