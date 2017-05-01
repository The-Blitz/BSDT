# coding=utf-8
import sentences as s
import freelingUser as fu
import graph as g
import pandas as pd
from queue import *


def procTextFile (filesent,flag): # flag: 0 separate opinion in sentences, 1 sentences per opinion together
	ans = []
	validWords = [] # adjectives, adverbs, nouns and verbs	
	fullSent = []	# all sentences per line

	sentence = s.splitSentence(filesent,flag)
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
	if(flag):
		fullSent.append(auxSent)
		validWords.append(validTags)
		ans.append(result)
	return ans,validWords,fullSent

def getCategory(attr , subj):
	if(attr=='SubjectiveAssessmentAttribute'): 
		return 'HS'
	elif(subj==0.0):
		return 'NS'
	elif(subj<=0.25):
		return 'LS'
	elif(subj<=0.50):
		return 'MS'
	else:
		return 'HS'

def mergeSenses(procSentences,flag): # this is related to subjectivity flag: 0 separate senses, 1 senses together
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
								if(subj==-1): continue; #ignore sense
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
						auxOffset.append((NS,NSFreq,'NS')) ; auxOffset.append((LS,LSFreq,'LS'))
						auxOffset.append((MS,MSFreq,'MS')) ; auxOffset.append((HS,HSFreq,'HS'))	
						offsetDict[word[0]] = auxOffset
					else:
						auxOffset = []
						conta=0
						for sense in offset:
							auxSense = [] 
							auxFreq = []
							freq= len(offset) - conta
							subj,obj = s.dbc.searchSubjectivity(sense)
							if(subj==-1): continue; #ignore sense
							auxSense.append(sense) #kind of necessary because of the sum of list in the next function, which calls this one
							auxFreq.append(freq)   #kind of necessary because of the sum of list in the next function, which calls this one
							auxOffset.append( ( auxSense,auxFreq,getCategory(ontology[conta],subj) ) )
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
						senseGraph.addEdge(listToStr(sense[0]),auxRoot,auxPos,sum(sense[1]),sense[2] , '-','-',0,0,'NS')
						senseGraph.addEdge('-','-',0,0,'NS', listToStr(sense[0]),auxRoot,auxPos,sum(sense[1]) ,sense[2] )
			else:
				senseGraph.addEdge('*',auxRoot,auxPos,0,'NS' , '-','-',0,0,'NS')
				senseGraph.addEdge('-','-',0,0,'NS', '*',auxRoot,auxPos,0,'NS')		
			
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
									senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[2]  , listToStr(sense2[0]),w2,p2,sum(sense2[1]),sense2[2]   , g.getDistanceList(sense1,sense2,1))
									senseGraph.addEdge(listToStr(sense2[0]),w2,p2,sum(sense2[1]),sense2[2]   , listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[2] , g.getDistanceList(sense2,sense1,1))
					elif (auxRoot== w2 and not(w2 in di) and w1 in di):
						for sense1 in di[ w1]:
							if(len(sense1[0])):
								senseGraph.addEdge('*',w2,p2,0,'NS' , listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[2]  )
								senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[2]   , '*',w2,p2,0,'NS')			
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

def findVertices(auxList , w1, p1, w2,p2):
	v1 = None
	val1=0.0
	v2 = None
	val2=0.0
	for key,value in auxList.items():
		if (key.getWord()== w1 and key.getPos()==p1 and val1<value):
			v1 = key
			val1 = value
	
	for key,value in auxList.items():
		if (key.getWord()== w2 and key.getPos()==p2 and val2<value):
			v2 = key
			val2 = value
	
	return v1,v2		


def printPageRank (pr,cont):
	f = open('prList1.txt','a+')
	sortkeys = sorted(pr.keys(),key=g.operator.attrgetter('pos','id'))
	for i in range(len(pr)):
		f.write("%d %s %f\n" % (cont,sortkeys[i],pr[sortkeys[i]]))	
	f.close()

def getGraphInfo (sentGraphs,pos):
	features = []
	for gr in sentGraphs:
		auxFeature = []
		pageRank= gr.pageRank()
		printPageRank(pageRank,pos)
		edges = gr.getEdges()
		for (word1,pos1,word2,pos2) in edges:
			vert1 , vert2 = findVertices(pageRank,word1,pos1,word2,pos2)
			auxFeature.append( (vert1.getWord() , vert1.getPos() , vert1.getCat() , vert2.getWord() , vert2.getPos() , vert2.getCat() ) )
		features.append(auxFeature)
	return features		


def addTags(auxFeat, auxWords,auxPos):
	cont=1
	result = []
	for i in range(len(auxWords)):
		for j in range (len (auxWords[i])): 
			words  = auxWords[i][j][0]
			tags   = auxWords[i][j][2]
			for k in range (len (auxFeat[i]) ):
				w1 = auxFeat[i][k][0]; p1 = auxFeat[i][k][1]; c1 = auxFeat[i][k][2]
				w2 = auxFeat[i][k][3]; p2 = auxFeat[i][k][4]; c2 = auxFeat[i][k][5]
				result.append((tags[p1-1][0]+"-"+c1,tags[p2-1][0]+"-"+c2))
				#print(i,auxPos,w1,w2, (tags[p1-1][0]+"-"+c1,tags[p2-1][0]+"-"+c2))
	return result

def createDict():
	features = ['N-NS' , 'N-LS' ,'N-MS' ,'N-HS' ,'A-NS' ,'A-LS' ,'A-MS' ,'A-HS' ,'R-NS' ,'R-LS' ,'R-MS' ,'R-HS' ,'V-NS' ,'V-LS' ,'V-MS' ,'V-HS'] #possibilities
	result = dict()
	for f1 in features:
		for f2 in features:
			auxF1 = f1+ " " +f2 
			auxF2 = f2+ " " +f1
			if ((not(auxF1 in result)) and (not(auxF2 in result))):
				result[auxF1] = 0
	return result			

def getFeatures(auxGraphs,auxWords, pos):

	auxInfo  =getGraphInfo(auxGraphs,pos)

	auxFeatures =  addTags(auxInfo , auxWords,pos)
	
	featDict = createDict()
	for feat in auxFeatures:
		w1 = feat[0] ; w2 = feat[1]
		auxF1 = w1+ " " +w2 ; auxF2 = w2+ " " +w1
		if (auxF1 in featDict):
			featDict[auxF1] = featDict[auxF1] +1
		elif (auxF2 in featDict):	
			featDict[auxF2] = featDict[auxF2] +1
									
	return featDict

def printFeat(feat,kind):
	f = open('featList1.txt','a+')
	if (kind=='I'):
		f.write("sentence ")	
		for aux in sorted(feat):
			f.write("% s " % (aux))	
		f.write("\n")	
	else:
		f.write("    %s    " % (kind))	
		for aux in sorted(feat):
			f.write("     %d    " % (feat[aux]))	
		f.write("\n")	
	f.close()

	
def sentToFeat(sentence,cont):
	words,wordSet,sentences  = procTextFile(sentence,0)
	procSentences =  s.sentenceSenses (words,wordSet)
	graphs  = createSenseGraph(sentences,procSentences)
	features = getFeatures(graphs,words,cont)
	return features

def generate():
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')
	printFeat(createDict(),'I') #Begin file
	for i in range(1,len(objFile)+1):
		features = sentToFeat(objFile[i-1],i)
		#print("Oración", i , "procesada , sentidos juntos")
		printFeat(features,'O')


	for i in range(1,len(subjFile)+1):
		features = sentToFeat(subjFile[i-1],i)
		#print("Oración", 125+i , "procesada, sentidos juntos")
		printFeat(features,'S')


