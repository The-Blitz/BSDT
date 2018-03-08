def printFeat(feat,kind):
	#f = open('featListA.txt','a+')
	f = open('wordListA.txt','a+')
	f.write("%s\t"% (kind))	
	for aux in sorted(feat):
		if(feat[aux]):	f.write("%s\t%d\t" % (aux,feat[aux]))	
	f.write("\n")	
	f.close()

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

#print relations as features
'''	
featDict = createDict()	

cont=1

with open('relations-A.txt','r',encoding='utf-8') as f: # read prlist 
	for line in f:
		line = line.strip('\n')
		line = line.split(' ')
		ind   = int(line[0])
		feat1 = line[len(line)-2]
		feat2 = line[len(line)-1]
		if(cont+1<=ind or cont<=ind+199):
			if(cont<=200):	
				aux=cont
				if(cont==200): aux = aux-200	
				for i in range(aux,ind):
					printFeat(featDict,'O')
					featDict = createDict()
					cont+=1
			else:
				aux=cont-200	
				for i in range(aux,ind):
					printFeat(featDict,'S')
					featDict = createDict()
					cont+=1						
			

		aux1 = feat1 + " " + feat2
		aux2 = feat2 + " " + feat1
		if(aux1 in featDict):
			featDict[aux1] = featDict[aux1] +1
		elif(aux2 in featDict):	
			featDict[aux2] = featDict[aux2] +1	
			
printFeat(featDict,'S')			
'''

#print words as features

featDict = createWordDict()	

cont=1

with open('result-A.txt','r',encoding='utf-8') as f: # read prlist 
	for line in f:
		line = line.strip('\n')
		line = line.split(' ')
		ind   = int(line[0])
		feat1 = line[len(line)-2][-1:].upper() # tag
		feat2 = line[len(line)-1]	# category
		if(cont+1<=ind or (cont<=ind+199 and cont!=ind)):
			if(cont<=200):	
				aux=cont
				if(cont==200): aux = aux-200	
				for i in range(aux,ind):
					printFeat(featDict,'O')
					featDict = createWordDict()
					cont+=1
			else:
				aux=cont-200	
				for i in range(aux,ind):
					printFeat(featDict,'S')
					featDict = createWordDict()
					cont+=1						
			

		aux1 = feat1 + "-" + feat2
		aux2 = feat2 + "-" + feat1
		if(aux1 in featDict):
			featDict[aux1] = featDict[aux1] +1
		elif(aux2 in featDict):	
			featDict[aux2] = featDict[aux2] +1	
			
printFeat(featDict,'S')			
					
