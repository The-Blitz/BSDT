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

def generateGraph():
	fileName  = 'WordNetEdges/ili-wnet30g_rels.txt'
	file1 = readFile(fileName,'utf-8')
	
	fileName  = 'WordNetEdges/ili-wnet30_rels.txt'
	file2  = readFile(fileName,'utf-8')	
	
	gr = g.Graph()

	for i in file1:
		gr.addEdge(i[0] , i[1] , 1)
		gr.addEdge(i[1] , i[0] , 1)
	
	for i in file2:
		gr.addEdge(i[0] , i[1] , 1)
		gr.addEdge(i[1] , i[0] , 1)
	return gr


gr = generateGraph()

fileV = open('vertList.txt','r')

for v in fileV:
	v = v[:len(v)-1] # remove '\n'
	f = open("Distances/"+v+'.txt','w')
	delta, previous = g.dijkstra(gr, v)
	for key,value in delta.items():
		f.write("%s %s\n" % (key,value))
	f.close()




	
