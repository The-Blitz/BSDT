from nltk.corpus import semcor
from nltk.corpus import sentiwordnet as swn
from nltk.parse.stanford import StanfordDependencyParser

def createDict(): #Can't import from parent module 
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

def printFeat(feat,kind):
	f = open('featSemcor.txt','a+')
	f.write("%s\t"% (kind))	
	for aux in sorted(feat):
		if(feat[aux]):	f.write("%s\t%d\t" % (aux,feat[aux]))	
	f.write("\n")	
	f.close()

def getCategory(subj):
	if(subj==0.0):
		return 'NS'
	elif(subj<=0.25):
		return 'LS'
	elif(subj<=0.50):
		return 'MS'
	else:
		return 'HS'

def createFile():
	s= semcor._items(None, 'word', True, False, False) # just words of sentences
	for i in range(20138):
		print(' '.join(word for word in s[i]))

#20138 first sentence that uses just verbs

#s = semcor.sents()
#print(s[20137]) #last expression kitchen_sink

sentTag = semcor._items(None, 'chunk', True, True, False)  # tagged expresions of sentences
sentSen = semcor._items(None, 'chunk', True, False, True)  # senses of sentences
sentWord= semcor._items(None, 'chunk', True, False, False) # expresions/words of sentences

corpusT = []
corpusS = []
corpusW = []
sentSubj = []

featSentences = []

#tags: V: verb ; N: noun ; J: adjective ; R: adverb 

fileName = 'subjSemcor.txt'	
with open(fileName,'r') as f:
	i=0 ; contO= 0 ; contS=0;
	for line in f:
		flag = int(line) # unknown = -1 ; obj = 0 ; subj = 1
		if(flag != -1): 
			if(contO==934 and flag==0): continue ; # equal 
			elif(contS==934 and flag==1): continue ; # equal 
			corpusT.append(sentTag[i])
			corpusS.append(sentSen[i])
			corpusW.append(sentWord[i])
			aux = 'O' if flag==0 else 'S'
			if(aux=='O'): contO+=1
			elif(aux=='S'): contS+=1
			sentSubj.append(aux)
		i+=1	

#print(len(corpusW)) #8365 sentences -> 1868 sentences equal obj and subj

for i in range(len(corpusW)):
	aux = []
	for j in range(len(corpusW[i])):
		#print(corpusW[i][j])
		wordS = corpusS[i][j]
		wordT = corpusT[i][j]
		result = 'No tag'
		if( not (wordT.label() is None) and (wordT.label()[0]=='V' or wordT.label()[0]=='N' or wordT.label()[0]=='J' or wordT.label()[0]=='R') ): 
			#print(wordT)	
			isLemma = (type(wordS) != type([])) and (type(wordS.label())!= type(str())) #ignoring words without lemmas and some lemmas with ".00" difficult to handle
			tag = wordT.label()[0]
			if(isLemma):
				sense = wordS.label().synset().name()
				objScore = (swn.senti_synset(sense)).obj_score()
				subjScore = 1.0 - objScore
				#print(objScore , subjScore , tag)
			else: # assuming the ignored words has no subjectivity value
				objScore = 1.0
				subjScore = 0.0
				#print(wordT)
			result = tag + '-' + getCategory(subjScore) if tag!='J' else 'A-' + getCategory(subjScore)
		
		checkWord = ''
		for word in corpusW[i][j]:
			auxWord = ''.join(filter(str.isalnum, word))
			if(auxWord!=''):
				if(checkWord!=''):	checkWord = checkWord+'_' +auxWord
				else: checkWord = auxWord
		if(checkWord != ''):
			#small fix
			if(checkWord == 'gotta') : checkWord = 'got_to'	
			elif(checkWord == 'cannot') : checkWord = 'can_not'	
			elif(checkWord == 'Lemme') : checkWord = 'let_me'
			#small fix			
			aux.append( (checkWord , result) )
	featSentences.append(aux)	


path_to_jar = 'stanford-parser-full-2017-06-09/stanford-parser.jar'
#path_to_models_jar = 'stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
path_to_models_jar = 'stanford-english-corenlp-2017-06-09-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)


for n in range(len(sentSubj)):
	featDict = createDict()
	sentence = ' '.join(word for word,tag in featSentences[n])
	#print(sentence)
	result = dependency_parser.raw_parse(sentence)
	parserTree = next(result)
	#parseList = list(parserTree.triples())
	#print (parseList)
	
	for k in parserTree.nodes.values():
		x = k["address"]
		y = k["head"]
		if x <= 0 or y <= 0 : continue 
		w1 = featSentences[n][x-1][1] ; w2 = featSentences[n][y-1][1] ; 
		if w1!='No tag' and w2!='No tag' :
			auxF1 = w1+ " " +w2 ; auxF2 = w2+ " " +w1 ;
			if (auxF1 in featDict):
				featDict[auxF1] = featDict[auxF1] +1
			elif (auxF2 in featDict):	
				featDict[auxF2] = featDict[auxF2] +1
			#print(w1 + " " + w2 )
	print('Sentence ' + str(n+1) )		
	printFeat(featDict,sentSubj[n])




