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
				#print(words[k],lemmas[k],tags[k])
				if(tags[k][0]=='A' or tags[k][0]=='N' or tags[k][0]=='R' or (tags[k][0]=='V' and tags[k][1]!='A')): # ignore auxiliar verbs
					validTags.add(lemmas[k])			
		#print(result)
		#print(validTags)
		fullSent.append(auxSent)
		validWords.append(validTags)
		ans.append(result)
	return ans,validWords,fullSent
	
def createSenseGraph(sentences , procSentences):
	dicts = []
	for opi in procSentences: # search in opinion
		offsetDict = dict()
		for sen in opi: # search in sentence
			for w in sen:	# search in word
				word= w[0]
				offset= w[1]
				if( not(len(offset)==1 and offset[0]=='-') ): # there should be an offset
					offsetDict[word[0]] = offset
		dicts.append(offsetDict)
	
	cont=0
	
	graphs = [] 
	
	for ls in sentences:
		di = dicts[cont]
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
					if(word[0][1] in di and top[1] in di):
						senseGraph.addEdge(top[1] , word[0][1])
						senseGraph.addEdge(word[0][1], top[1])
					q.put(word[0])
		cont+=1			
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
	
	objProcSentences =  s.sentenceSenses (objWords,objWordSet)
	subjProcSentences = s.sentenceSenses (subjWords,subjWordSet)

	objGraphs  = createSenseGraph(objSentences,objProcSentences)
	subjGraphs = createSenseGraph(subjSentences,subjProcSentences)
	
	cont=1
	for g in objGraphs:
		for v in g:
			for w in v.getConnections():
				print("(%d, %s , %s , %s )" % (cont,v.getId(), w.getId(),v.getWeight(w)))
		cont+=1		
		
	cont=1		
	for g in subjGraphs:
		for v in g:
			for w in v.getConnections():
				print("(%d, %s , %s , %s )" % (cont,v.getId(), w.getId(),v.getWeight(w)))	
		cont+=1					
	
if __name__ == "__main__":
    
    main()


