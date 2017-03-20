import os.path

class Vertex:
    def __init__(self,key,w,p):
        self.id = key
        self.connectedTo = {}
        self.word = w
        self.pos = p

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + " " +str(self.word)+ " " + str(self.pos) 

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
    	return self.id
    
    def getWord(self):
    	return self.word
    
    def getPos(self):
    	return self.pos
    
    def getWeight(self,nbr):
    	return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key,word,pos):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,word,pos)
        self.vertList[key+"-"+str(pos)] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,fword,fpos,t,tword,tpos,cost=0):
        if (f+"-"+str(fpos)) not in self.vertList:
            nv = self.addVertex(f,fword,fpos)
        if (t+"-"+str(tpos)) not in self.vertList:
            nv = self.addVertex(t,tword,tpos)
        self.vertList[f+"-"+str(fpos)].addNeighbor(self.vertList[t+"-"+str(tpos)], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


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
				
def getDistanceList(start,end):
	ans = -1 #never found
	for i in start:
		for j in end:
			ans = max(ans,getDistanceSense(i,j))
	return ans
              
