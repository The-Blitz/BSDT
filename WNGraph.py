import graph as g;


def readFile(fileName,encode): 
	lines=[]
	with open(fileName,'r',encoding=encode) as f:
		for line in f:
			line = line.split(' ')
			u = 'spa' +  line[0][5:]
			v = 'spa' +  line[1][5:]
			lines.append((u,v))
	return lines
	
fileName  = 'WordNetEdges/ili-wnet30g_rels.txt'
file1 = readFile(fileName,'utf-8')

fileName  = 'WordNetEdges/ili-wnet30_rels.txt'
file2  = readFile(fileName,'utf-8')	


def generateGraph():

	gr = g.Graph()

	for i in file1:
		gr.addEdge(i[0] , i[1] , 1)
		gr.addEdge(i[1] , i[0] , 1)
	
	for i in file2:
		gr.addEdge(i[0] , i[1] , 1)
		gr.addEdge(i[1] , i[0] , 1)
	
	#for v in gr:
	#	for w in v.getConnections():
	#		print("( %s , %s , %s )" % (v.getId(), w.getId(),v.getWeight(w)))
	return gr

def floydWarshall(graph):
	
	for v in graph:
		print (v)



floydWarshall ( generateGraph() )








	
