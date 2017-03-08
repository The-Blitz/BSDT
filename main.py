# coding=utf-8
import sentences as s
import freelingUser as fu
import graph as g
from queue import *


def procTextFile (filename):
	ans = []
	validWords = [] # adjectives, adverbs, nouns and verbs	
	fullSent = []	# all sentences per line
	for i in range(len(filename)):
		sentence = s.splitSentence(filename[i])
		result = []
		validTags = set()
		auxSent = []
		for j in range (len (sentence)):
			aux = s.procSentence(sentence[j])
			auxSent.append(aux)
			words,lemmas,tags=fu.procText(aux)
			result.append( (words,lemmas,tags) )
			for k in range ( len (tags) ):
				if(tags[k][0]=='A' or tags[k][0]=='N' or tags[k][0]=='R' or tags[k][0]=='V'):
					#print(words[k],lemmas[k])
					validTags.add(lemmas[k])			
		#print(result)
		#print(validTags)
		fullSent.append(auxSent)
		validWords.append(validTags)
		ans.append(result)
	return ans,validWords,fullSent
	
def createSenseGraph(sentences):
	graphs = [] 
	for ls in sentences:
		senseGraph = g.Graph() #graph per opinion
		for se in ls:
			# senseGraph = g.Graph()  #graph per sentece
			rel, depT = fu.dependencyParser(se);
			q = Queue()
			q.put(depT[0])
			senseGraph.addEdge(depT[0][1] , '-')
			senseGraph.addEdge('-' , depT[0][1])
			while (not q.empty()):
				top = q.get()
				for word in top[2]:
					senseGraph.addEdge(top[1] , word[0][1])
					senseGraph.addEdge(word[0][1], top[1])
					q.put(word[0])
		graphs.append(senseGraph)				
							
	return graphs;			
	
def main():
	#fileName = 'Corpus/spanish_objectives_filmaffinity_2500'
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	#fileName = 'Corpus/spanish_subjectives_filmaffinity_2500'
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')
	
	objWords,objWordSet,objSentences  = procTextFile(objFile)
	subjWords,subjWordSet,subjSentences = procTextFile(subjFile)
	
	#objProcSentence =  s.sentenceSenses (objWords,objWordSet)
	#subjProcSentence = s.sentenceSenses (subjWords,subjWordSet)

	objGraphs  = createSenseGraph(objSentences)	
	subjGraphs = createSenseGraph(subjSentences)		
	
	cont=1
	for g in objGraphs:
		for v in g:
			for w in v.getConnections():
				print("(%d %s , %s , %s )" % (cont,v.getId(), w.getId(),v.getWeight(w)))
		cont+=1		
		
	cont=1		
	for g in subjGraphs:
		for v in g:
			for w in v.getConnections():
				print("(%d %s , %s , %s )" % (cont,v.getId(), w.getId(),v.getWeight(w)))	
		cont+=1					
	
if __name__ == "__main__":
    
    main()


