# coding=utf-8
import sentences as s
import freelingUser as fu
import graph as g
import pandas as pd
from queue import *


def procTextFile (filename,flag): # flag: 0 separate opinion in sentences, 1 sentences per opinion together
	ans = []
	validWords = [] # adjectives, adverbs, nouns and verbs	
	fullSent = []	# all sentences per line
	positions = []
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
			if(not flag):
				fullSent.append(auxSent)
				validWords.append(validTags)
				ans.append(result)
				result = []
				validTags = set()
				auxSent = []
				positions.append(i+1)
		if(flag):
			fullSent.append(auxSent)
			validWords.append(validTags)
			ans.append(result)
			positions.append(i+1)	
	return ans,validWords,fullSent,positions

def mergeSenses(procSentences,flag): # this is related to subjectivity
	dicts = []
	for opi in procSentences: # search in opinion
		offsetDict = dict()
		for sen in opi: # search in sentence
			for w in sen:	# search in word
				word= w[0]
				offset= w[1]
				ontology = w[2]
				if( not(len(offset)==1 and offset[0]=='-') ): # there should be an offset
					if(flag==1):
						NS = [] ; NSFreq = []
						LS = [] ; LSFreq = []
						MS = [] ; MSFreq = []
						HS = [] ; HSFreq = []
						auxOffset = []
						conta=0
						for sense in offset:
							if(sense != '-' and sense != None):
								freq= len(offset) - conta
								subj,obj = s.dbc.searchSubjectivity(sense)
								if(ontology[conta]=='SubjectiveAssessmentAttribute'): 
									HS.append(sense) #the ontology adds subjectivity value
									HSFreq.append(freq)
								elif(subj==0.0):
									NS.append(sense)
									NSFreq.append(freq)	
								elif(subj<=0.25):
									LS.append(sense)
									LSFreq.append(freq)
								elif(subj<=0.50):
									MS.append(sense)
									MSFreq.append(freq)
								else:
									HS.append(sense)
									HSFreq.append(freq)
							conta = conta+1	
						auxOffset.append((NS,NSFreq)) ; auxOffset.append((LS,LSFreq))
						auxOffset.append((MS,MSFreq)) ; auxOffset.append((HS,HSFreq))	
						offsetDict[word[0]] = auxOffset
					else:
						auxOffset = []
						conta=0
						for sense in offset:
							auxSense = [] 
							auxFreq = []
							freq= len(offset) - conta
							auxSense.append(sense)
							auxFreq.append(freq) #kind of necessary because of the sum of list in the next function, which calls this one
							auxOffset.append((auxSense,auxFreq))
							conta = conta+1
						offsetDict[word[0]] = auxOffset	 
		dicts.append(offsetDict)
	return dicts
	
def createSenseGraph(sentences , procSentences):
	dicts = mergeSenses(procSentences,1)
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
					if(len(sense[0])):
						senseGraph.addEdge(listToStr(sense[0]),auxRoot,auxPos,sum(sense[1]) , '-','-',0,0)
						senseGraph.addEdge('-','-',0,0, listToStr(sense[0]),auxRoot,auxPos,sum(sense[1])  )
			else:
				senseGraph.addEdge('*',auxRoot,auxPos,0 , '-','-',0,0)
				senseGraph.addEdge('-','-',0,0, '*',auxRoot,auxPos,0)		
			
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
								if(len(sense1[0]) and len(sense2[0]) ):
									senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1])  , listToStr(sense2[0]),w2,p2,sum(sense2[1])  , g.getDistanceList(sense1,sense2,1))
									senseGraph.addEdge(listToStr(sense2[0]),w2,p2,sum(sense2[1])  , listToStr(sense1[0]),w1,p1,sum(sense1[1])  , g.getDistanceList(sense2,sense1,1))
					elif (auxRoot== w2 and not(w2 in di) and w1 in di):
						for sense1 in di[ w1]:
							if(len(sense1[0])):
								senseGraph.addEdge('*',w2,p2,0 , listToStr(sense1[0]),w1,p1,sum(sense1[1]) )
								senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1])  , '*',w2,p2,0)			
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
	
	objWords,objWordSet,objSentences,objPos  = procTextFile(objFile,1)
	subjWords,subjWordSet,subjSentences,subjPos = procTextFile(subjFile,1)
		
	objProcSentences =  s.sentenceSenses (objWords,objWordSet)
	subjProcSentences = s.sentenceSenses (subjWords,subjWordSet)

	objGraphs  = createSenseGraph(objSentences,objProcSentences)
	subjGraphs = createSenseGraph(subjSentences,subjProcSentences)
	
	cont=1
	for gr in objGraphs:
		auxi= gr.pageRank()
		sortkeys = sorted(auxi.keys(),key=g.operator.attrgetter('pos','id'))
		for i in range(len(auxi)):
			print(cont,sortkeys[i],auxi[sortkeys[i]])
		cont+=1	
		
	cont=1		
	for gr in subjGraphs:
		auxi= gr.pageRank()
		sortkeys = sorted(auxi.keys(),key=g.operator.attrgetter('pos','id'))
		for i in range(len(auxi)):
			print(cont,sortkeys[i],auxi[sortkeys[i]])
		cont+=1					

if __name__ == "__main__":
    
    main()


