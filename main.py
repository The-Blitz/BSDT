# coding=utf-8
import sentences as s
import freelingUser as fu
import graph as g
import pandas as pd
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

def mergeSenses(procSentences): # this is related to subjectivity
	dicts = []
	for opi in procSentences: # search in opinion
		offsetDict = dict()
		for sen in opi: # search in sentence
			for w in sen:	# search in word
				word= w[0]
				offset= w[1]
				ontology = w[2]
				if( not(len(offset)==1 and offset[0]=='-') ): # there should be an offset
					NS = []
					LS = []
					MS = []
					HS = []
					auxOffset = []
					conta=0
					for sense in offset:
						if(sense != '-' and sense != None):
							subj,obj = s.dbc.searchSubjectivity(sense)
							if(ontology[conta]=='SubjectiveAssessmentAttribute'): HS.append(sense) #the ontology adds subjectivity value
							elif(subj==0.0): NS.append(sense)	
							elif(subj<=0.25): LS.append(sense)
							elif(subj<=0.50): MS.append(sense)
							else: HS.append(sense)
						conta = conta+1	
					auxOffset.append(NS)
					auxOffset.append(LS)
					auxOffset.append(MS)
					auxOffset.append(HS)	
					offsetDict[word[0]] = auxOffset
		dicts.append(offsetDict)
	return dicts
	
def createSenseGraph(sentences , procSentences):
	dicts = mergeSenses(procSentences)
	cont=0
	graphs = [] # '-' connect sentences , '*' replaces sentence root
	
	for ls in sentences:
		di = dicts[cont]
		senseGraph = g.Graph() #graph per opinion
		for se in ls:
			# senseGraph = g.Graph()  #graph per sentece
			rel, depT = fu.dependencyParser(se)
			q = Queue()
			q.put(depT[0])
						
			auxRoot = depT[0][1][0] ## dependency parser root
			auxPos  = depT[0][1][1] 
			if(auxRoot in di):
				for sense in di[auxRoot]:
					if(len(sense)):
						senseGraph.addEdge(listToStr(sense),auxRoot,auxPos , '-','-',0)
						senseGraph.addEdge('-','-',0, listToStr(sense),auxRoot,auxPos )
			else:
				senseGraph.addEdge('*',auxRoot,auxPos , '-','-',0)
				senseGraph.addEdge('-','-',0, '*',auxRoot,auxPos)		
			
			while (not q.empty()):
				top = q.get()
				
				for word in top[2]:
					w1 = word[0][1][0]
					p1 = word[0][1][1]
					w2 = top[1][0]
					p2 = top[1][1]
					if(w1 in di and w2 in di):
						for sense2 in di[ w2 ]:
							for sense1 in di[ w1 ]:
								if(len(sense1) and len(sense2) ):
									senseGraph.addEdge(listToStr(sense1),w1,p1 , listToStr(sense2),w2,p2 , g.getDistanceList(sense1,sense2))
									senseGraph.addEdge(listToStr(sense2),w2,p2 , listToStr(sense1),w1,p1 , g.getDistanceList(sense2,sense1))
					elif (auxRoot== w2 and not(w2 in di) and w1 in di):
						for sense1 in di[ w1]:
							if(len(sense1)):
								senseGraph.addEdge('*',w2,p2 , listToStr(sense1),w1,p1)
								senseGraph.addEdge(listToStr(sense1),w1,p1 , '*',w2,p2)			
					q.put(word[0])
		cont+=1			
		graphs.append(senseGraph)
						
					
	return graphs;			

def listToStr(auxList):
	return " ".join(str(x) for x in auxList)
	
def generateExcelCorpus(objSent,subjSent):
	numlist   = []
	wordlist  = []
	lemmalist = []
	taglist   = []
	senselist = []
	
	for i in range(len(objSent)):
		for j in range (len (objSent[i])): 
			for k in range (len (objSent[i][j]) ):
				words = objSent[i][j][k][0]
				senses= objSent[i][j][k][1]
			
				numlist.append(str(i+1) + " obj")
				wordlist.append(words[0])
				lemmalist.append(words[1])
				taglist.append(words[2])
				if(len(senses)==1 and senses[0]=='-') :
					senselist.append("-")
				else:
					senselist.append(" ")	
				
	for i in range(len(subjSent)):
		for j in range (len (subjSent[i])): 
			words  = subjSent[i][j]
			for k in range (len (subjSent[i][j]) ):
				words = subjSent[i][j][k][0]
				senses= subjSent[i][j][k][1]
			
				numlist.append(str(i+1) + " subj")
				wordlist.append(words[0])
				lemmalist.append(words[1])
				taglist.append(words[2])
				if(len(senses)==1 and senses[0]=='-') :
					senselist.append("-")
				else:
					senselist.append(" ")
					
	df = pd.DataFrame({'sentence': numlist, 'word': wordlist , 'lemma': lemmalist  , 'tag': taglist  , 'sense': senselist })
	df = df[['sentence', 'word','lemma','tag','sense']]
	df.to_excel('corpusExcel2.xlsx', sheet_name='sheet1', index=False)				

	
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
				print("(%d, %s , %s , %s )" % (cont, v, w, v.getWeight(w)))
		cont+=1		
		
	cont=1		
	for g in subjGraphs:
		for v in g:
			for w in v.getConnections():
				print("(%d, %s , %s , %s )" % (cont, v ,w , v.getWeight(w)))	
		cont+=1					

if __name__ == "__main__":
    
    main()


