# coding=utf-8
import sentences as s
import freelingUser as fu
import graph as g
import corpusGenerator as cg
from queue import *


def procTextFile (filesent,flag): # flag: 0 separate opinion in sentences, 1 sentences per opinion together
	ans = []
	validWords = [] # adjectives, adverbs, nouns and verbs	
	fullSent = []	# all sentences per line
	sentence = s.splitSentence(filesent,flag)
	validTags = set()
	for j in range (len (sentence)):
		aux = s.procSentence(sentence[j])
		words,lemmas,tags=fu.procText(aux)
		for k in range ( len (tags) ):
			#print(words[k],lemmas[k],tags[k])
			if(tags[k][0]=='A' or tags[k][0]=='N' or tags[k][0]=='R' or (tags[k][0]=='V' and tags[k][1]!='A')): # ignore auxiliar verbs
				validTags.add(lemmas[k]+" "+str(k+1))			
		if(not flag):
			fullSent.append(aux)
			validWords.append(validTags)
			ans.append((words,lemmas,tags))
			validTags = set()
	if(flag):
		fullSent.append(aux)
		validWords.append(validTags)
		ans.append((words,lemmas,tags))
	return ans,validWords,fullSent

def getCategory(attr , subj):
	if('SubjectiveAssessmentAttribute' in attr): 
		return 'HS'
	elif(subj==0.0):
		return 'NS'
	elif(subj<=0.25):
		return 'LS'
	elif(subj<=0.50):
		return 'MS'
	else:
		return 'HS'

def mergeSenses(procSentences,flag): # this is related to subjectivity flag: 0 separate senses, 1 senses together , 2 senses mean
	dicts = []
	for sen in procSentences: # search in sentence
		pos=1
		offsetDict = dict()
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
					conta=0;contaN=1000;contaL=1000;contaM=1000;contaH=1000;
					for sense in offset:
						if(sense != '-' and sense != None):
							freq= len(offset) - conta
							subj,obj = s.dbc.searchSubjectivity(sense)
							subjOnto = 'SubjectiveAssessmentAttribute' in ontology[conta]
							if(subj==-1 and not(subjOnto)): 
								conta = conta+1	
								continue; #ignore sense
							if(subjOnto ): 
								HS.append(sense) #the ontology adds subjectivity value
								HSFreq.append(freq)
								contaH=min(contaH,conta+1)
							elif(subj==0.0):
								NS.append(sense)
								NSFreq.append(freq)
								contaN=min(contaN,conta+1)	
							elif(subj<=0.25):
								LS.append(sense)
								LSFreq.append(freq)
								contaL=min(contaL,conta+1)
							elif(subj<=0.50):
								MS.append(sense)
								MSFreq.append(freq)
								contaM=min(contaM,conta+1)
							else:
								HS.append(sense)
								HSFreq.append(freq)
								contaH=min(contaH,conta+1)
						conta = conta+1	
					auxOffset.append((NS,NSFreq,'NS',contaN)) ; auxOffset.append((LS,LSFreq,'LS',contaL))
					auxOffset.append((MS,MSFreq,'MS',contaM)) ; auxOffset.append((HS,HSFreq,'HS',contaH))	
					offsetDict[word[0]+" "+str(pos)] = auxOffset
				elif(flag==0):
					auxOffset = []
					conta=0
					for sense in offset:
						auxSense = [] 
						auxFreq = []
						freq= len(offset) - conta
						subj,obj = s.dbc.searchSubjectivity(sense)
						subjOnto = 'SubjectiveAssessmentAttribute' in ontology[conta]
						if(subj==-1 and not(subjOnto)): 
							conta = conta+1	
							continue; #ignore sense
						auxSense.append(sense) #kind of necessary because of the sum of list in the next function, which calls this one
						auxFreq.append(freq)   #kind of necessary because of the sum of list in the next function, which calls this one
						auxOffset.append( ( auxSense,auxFreq,getCategory(ontology[conta],subj),conta+1 ) )
						conta = conta+1
					offsetDict[word[0]+" "+str(pos)] = auxOffset
				elif(flag==2):
					conta=0
					total=0
					meanS=0.0
					for sense in offset:
						subj,obj = s.dbc.searchSubjectivity(sense)
						subjOnto = 'SubjectiveAssessmentAttribute' in ontology[conta]
						if(subj==-1 and not(subjOnto)): 
							conta = conta+1	
							continue; #ignore sense
						total = total+1	
						if(subjOnto): 
							meanS= meanS+1.0
						else:
							meanS=meanS+subj	
						conta = conta+1
					if(total>0):
						offsetDict[word[0]+" "+str(pos)] = getCategory(['NONACATEGORY'],meanS/total)
			pos=pos+1													 
		dicts.append(offsetDict)
	return dicts
	
def createSenseGraph(sentences , procSentences, mergeFlag):
	dicts = mergeSenses(procSentences,mergeFlag)
	cont=0
	graphs = [] # '-' connect sentences , '*' replaces sentence root

	for se in sentences:
		di = dicts[cont]
		senseGraph = g.Graph() #graph per sentence
		rel, depT = fu.dependencyParser(se)
		q = Queue()
		q.put(depT[0])	
		relation= depT[0][0]	# relation between words
		auxRoot = depT[0][1][0] ## dependency parser root
		auxPos  = depT[0][1][1] 
		if((auxRoot+" "+str(auxPos)) in di):
			for sense in di[auxRoot+" "+str(auxPos)]:
				if(len(sense[0])):
					senseGraph.addEdge(listToStr(sense[0]),auxRoot,auxPos,sum(sense[1]),sense[3],sense[2] , '-','-',0,0,0,'NS',0, relation)
					senseGraph.addEdge('-','-',0,0,0,'NS', listToStr(sense[0]),auxRoot,auxPos,sum(sense[1]),sense[3] ,sense[2],0, relation)
		else:
			senseGraph.addEdge('*',auxRoot,auxPos,0,0,'NS' , '-','-',0,0,0,'NS',0, relation)
			senseGraph.addEdge('-','-',0,0,0,'NS', '*',auxRoot,auxPos,0,0,'NS',0, relation)		
			
		while (not q.empty()):
			top = q.get()
				
			for word in top[2]:
				w1 = word[0][1][0]
				p1 = word[0][1][1]
				w2 = top[1][0]
				p2 = top[1][1]
				relation = word[0][0] # relation between words
				if((w1+" "+str(p1)) in di and (w2+" "+str(p2)) in di):
					for sense2 in di[ (w2+" "+str(p2)) ]:
						for sense1 in di[ (w1+" "+str(p1))  ]:
							if(len(sense1[0]) and len(sense2[0]) ):
								senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[3],sense1[2]  , listToStr(sense2[0]),w2,p2,sum(sense2[1]),sense2[3],sense2[2]   , g.getDistanceList(sense1,sense2,1), relation)
								senseGraph.addEdge(listToStr(sense2[0]),w2,p2,sum(sense2[1]),sense2[3],sense2[2]   , listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[3],sense1[2] , g.getDistanceList(sense2,sense1,1), relation)
				elif (auxRoot== w2 and not((w2+" "+str(p2)) in di) and (w1+" "+str(p1))  in di):
					for sense1 in di[ (w1+" "+str(p1))  ]:
						if(len(sense1[0])):
							senseGraph.addEdge('*',w2,p2,0,0,'NS' , listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[3],sense1[2]  ,0, relation)
							senseGraph.addEdge(listToStr(sense1[0]),w1,p1,sum(sense1[1]),sense1[3],sense1[2]   , '*',w2,p2,0,0,'NS',0, relation)			
				q.put(word[0])
		cont+=1			
		graphs.append(senseGraph)
							
	return graphs;			

def listToStr(auxList):
	return " ".join(str(x) for x in auxList)

def meanFeatures(sentences,procSentences,words,wordSet,counter):
	result= []
	dicts = mergeSenses(procSentences,2)
	cont=0
	sentSubj= []
	#f = open('relations3.txt','a+')
	for se in sentences:
		dictSubj = dict()
		di = dicts[cont]
		rel, depT = fu.dependencyParser(se)
		q = Queue()
		q.put(depT[0])	
		while (not q.empty()):
			top = q.get()
			for word in top[2]:
				w1 = word[0][1][0]
				p1 = word[0][1][1]
				w2 = top[1][0]
				p2 = top[1][1]
				relation = word[0][0] # relation between words
				if((w1+" "+str(p1)) in di and (w2+" "+str(p2)) in di): 
					result.append((words[cont][2][p1-1][0]+"-"+di[(w1+" "+str(p1))],words[cont][2][p2-1][0]+"-"+di[(w2+" "+str(p2))],relation))
					#f.write("%s\t%s\n" % ( ( str(counter)+" "+ w1 +"-"+str(p1)+" "+ w2 +"-"+str(p2) ), 
					#		words[cont][2][p1-1][0]+"-"+di[(w1+" "+str(p1))] +" " + 
					#		words[cont][2][p2-1][0]+"-"+di[(w2+" "+str(p2))] ) )
					dictSubj[p1] = di[(w1+" "+str(p1))] ; dictSubj[p2] = di[(w2+" "+str(p2))] ; #each word subjectivity
				q.put(word[0])
		cont=cont+1	
		sentSubj.append(dictSubj)
	#f.close()
								
	featDict = createDict()
	for feat in result:
		w1 = feat[0] ; w2 = feat[1] ; r = feat[2];
		auxF1 = w1+ " " +w2 ; auxF2 = w2+ " " +w1 ;
		if (auxF1 in featDict):
			featDict[auxF1] = featDict[auxF1] +1
		elif (auxF2 in featDict):	
			featDict[auxF2] = featDict[auxF2] +1	
	
	dictWord = createWordDict()
	cont=0
	for se in sentences:
		di = dicts[cont]
		word = words[cont][0]
		tags = words[cont][2]
		validWords = wordSet[cont]
		
		for n in validWords:
			p = int(n.split()[1])
			w = word[p-1];
			aux = w + " " + str(p)
			if aux in di:
				dictWord[tags[p-1][0] + "-" + di[aux]] +=1
		cont=cont+1
	
	#printFeat(dictWord,'X','wordList3.txt')		
											
	return featDict,sentSubj						
							
def findVertice(auxList , w,p):
	v = None
	val=0.0
	
	sortkeys = sorted(auxList.keys(),key=g.operator.attrgetter('pos','Nsense','id'))
	
	for i in range(len(sortkeys)):
		key=sortkeys[i];	value=auxList[sortkeys[i]];
		if (key.getWord()== w and key.getPos()==p and ( (val==value and abs(val-value) > 1e-6) or (val<value) ) ):
			v = key
			val = value
			
	return v		

def wordsSubjPR(gr,dictWord,auxWords,validWords,pos):
	pageRank= gr.pageRank()
	#printPageRank(pageRank,pos)
	dictSubj = dict()
	words  = auxWords[0]
	tags   = auxWords[2]

	for n in validWords:
		p = int(n.split()[1])
		w = words[p-1];
		vert = findVertice(pageRank,w,p)
		if vert is not None:
			dictSubj[w + " " + str(p)] = vert
			dictWord[tags[p-1][0] + "-" + vert.getCat()] +=1

	return dictSubj			

def printPageRank (pr,cont):
	f = open('prList1.txt','a+')
	sortkeys = sorted(pr.keys(),key=g.operator.attrgetter('pos','Nsense','id'))
	for i in range(len(pr)):
		f.write("%d %s %f\n" % (cont,sortkeys[i],pr[sortkeys[i]]))	
	f.close()

def getGraphInfo (sentGraphs,words,wordSet,pos):
	features = []
	cont = 0
	dictWord = createWordDict()
	for gr in sentGraphs:
		auxFeature = []
		vertDict = wordsSubjPR(gr , dictWord, words[cont], wordSet[cont], pos)
		edges = gr.getEdges()
		for (word1,pos1,word2,pos2,relation) in edges:
			vert1  = vertDict[word1 +" " + str(pos1)]
			vert2  = vertDict[word2 +" " + str(pos2)]
			auxFeature.append( (vert1.getWord() , vert1.getPos() , vert1.getCat() , vert2.getWord() , vert2.getPos() , vert2.getCat() , relation) )
		features.append(auxFeature)
		cont +=1
	#printFeat(dictWord,'X','wordList1.txt')	# will be changed to O or S in the file		
	return features		


def addTags(auxFeat, auxWords,auxPos):
	cont=1
	result = []
	sentSubj= []
	#f = open('relations1.txt','a+')
	for i in range(len(auxWords)):
		tags   = auxWords[i][2]
		dictSubj = dict()
		for k in range (len (auxFeat[i]) ):
			w1 = auxFeat[i][k][0]; p1 = auxFeat[i][k][1]; c1 = auxFeat[i][k][2]
			w2 = auxFeat[i][k][3]; p2 = auxFeat[i][k][4]; c2 = auxFeat[i][k][5]
			r  = auxFeat[i][k][6]
			result.append((tags[p1-1][0]+"-"+c1,tags[p2-1][0]+"-"+c2,r))
			#f.write("%s\t%s\n" % ((str(auxPos)+" "+ w1 +"-"+str(p1)  +" "+ w2+"-"+str(p2)) , (tags[p1-1][0]+"-"+c1) +" " + (tags[p2-1][0]+"-"+c2) ) )
			dictSubj[p1]=c1 ; dictSubj[p2]=c2 ;#each word subjectivity
		sentSubj.append(dictSubj)
	#f.close()		
	return result,sentSubj

def createDict():
	features = ['N-NS' , 'N-LS' ,'N-MS' ,'N-HS' ,'A-NS' ,'A-LS' ,'A-MS' ,'A-HS' ,'R-NS' ,'R-LS' ,'R-MS' ,'R-HS' ,'V-NS' ,'V-LS' ,'V-MS' ,'V-HS'] #possibilities
	'''dependencies =['spec','sn','f','sp','cc','suj','cd','S','s.a','sentence','coord','conj','v','atr','creg','mod',
	'morfema.pronominal','grup.nom','ci','sadv','ao','d','cpred','pass','et','cag','s','z','infinitiu','grup.a','inc','impers',
	'c','relatiu','r','neg','a','sa','n','gerundi','interjeccio','grup.adv','morfema.verbal','participi','p','w','voc','i','prep'] # freeling '''
	result = dict()
	for f1 in features:
		for f2 in features:
			#for d in dependencies:
				auxF1 = f1+ " " +f2#+ " " + d 
				auxF2 = f2+ " " +f1#+ " " + d 
				if ((not(auxF1 in result)) and (not(auxF2 in result))):
					result[auxF1] = 0
	return result			

def createWordDict():
	features = ['N-NS' , 'N-LS' ,'N-MS' ,'N-HS' ,'A-NS' ,'A-LS' ,'A-MS' ,'A-HS' ,'R-NS' ,'R-LS' ,'R-MS' ,'R-HS' ,'V-NS' ,'V-LS' ,'V-MS' ,'V-HS'] #possibilities
	result = dict()
	for f1 in features:
		result[f1] = 0
	return result

def getFeatures(auxGraphs,auxWords,wordSet, pos):

	auxInfo  =getGraphInfo(auxGraphs,auxWords,wordSet,pos)

	auxFeatures,sentSubj =  addTags(auxInfo , auxWords,pos)
	
	featDict = createDict()
	for feat in auxFeatures:
		w1 = feat[0] ; w2 = feat[1] ; r = feat[2];
		auxF1 = w1+ " " +w2 ; auxF2 = w2+ " " +w1 ;
		if (auxF1 in featDict):
			featDict[auxF1] = featDict[auxF1] +1
		elif (auxF2 in featDict):	
			featDict[auxF2] = featDict[auxF2] +1
									
	return featDict,sentSubj

def printFeat(feat,kind,nameFile):
	f = open(nameFile,'a+')
	f.write("%s\t"% (kind))	
	for aux in sorted(feat):
		if(feat[aux]):	f.write("%s\t%d\t" % (aux,feat[aux]))	
	f.write("\n")	
	f.close()

	
def sentToFeat(sentence,cont=0,flag=1): #cont: sentence in corpus , flag: 0 NOT WSD, 1 with WSD
	words,wordSet,sentences  = procTextFile(sentence,0)
	procSentences =  s.sentenceSenses (words,wordSet)
	if (flag):
		graphs  = createSenseGraph(sentences,procSentences,1)
		features,sentSubj = getFeatures(graphs,words,wordSet,cont)
	else:
		features,sentSubj = meanFeatures(sentences,procSentences,words,wordSet,cont) # get features with subjectivity's mean
	
	return features,sentSubj,words

def generate():
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')

	for i in range(1,len(objFile)+1):
		features,sentSubj,words = sentToFeat(objFile[i-1],i,1)
		#print("Oración", i , "procesada , sentidos juntos")
		#printFeat(features,'O','featList1.txt')


	for i in range(1,len(subjFile)+1):
		features,sentSubj,words = sentToFeat(subjFile[i-1],i,1)
		#print("Oración", 450+i , "procesada, sentidos juntos")
		#printFeat(features,'S','featList1.txt')
		
def corpusExcel():
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')
	objProcSentences = []
	subjProcSentences= []
	
	for i in range(1,len(objFile)+1):
		words,wordSet,sentences  = procTextFile(objFile[i-1],0)
		procSentences =  s.sentenceSenses (words,wordSet)
		objProcSentences.append(procSentences)
	
	for i in range(1,len(subjFile)+1):	
		words,wordSet,sentences  = procTextFile(subjFile[i-1],0)
		procSentences =  s.sentenceSenses (words,wordSet)
		subjProcSentences.append(procSentences)
	
	cg.generateExcelCorpus(objProcSentences,subjProcSentences)
	
def generateWordList(): #List of relevant words of sentences (Nouns, Verbs, Adjectives, adveRbs)
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')

	f = open('testReleW.txt','a+')

	for i in range(201,451):
		words,wordSet,sentences  = procTextFile(objFile[i-1],0)
		for j in range(0,len(words)):
			wo = words[j][0]
			le = words[j][1]
			tg = words[j][2]
			for k in range(1,len(wo) + 1):
				if( ( le[k-1] +" "+ str(k) ) in wordSet[j] ):
					f.write("%d %d %s %s %s\n" % (i,k,wo[k-1],le[k-1],tg[k-1][0]) )
		print("Oración", i ,"objetiva procesada" )
		
	for i in range(201,451):
		words,wordSet,sentences  = procTextFile(subjFile[i-1],0)
		for j in range(0,len(words)):
			wo = words[j][0]
			le = words[j][1]
			tg = words[j][2]
			for k in range(1,len(wo) + 1):
				if( ( le[k-1] +" "+ str(k) ) in wordSet[j] ):
					f.write("%d %d %s %s %s\n" % (i,k,wo[k-1],le[k-1],tg[k-1][0]) )
		print("Oración", i ,"subjetiva procesada" )			

	f.close()

#generateWordList()		
