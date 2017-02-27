# coding=utf-8
import sentences as s;
import freelingUser as fu;

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
	
	
	
def main():
	#fileName = 'Corpus/spanish_objectives_filmaffinity_2500'
	fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	#fileName = 'Corpus/spanish_subjectives_filmaffinity_2500'
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')
	
	objWords,objWordSet,objSentences  = procTextFile(objFile)
	subjWords,subjWordSet,subjSentences = procTextFile(subjFile)
	#print (s.sentenceSenses (objWords,objWordSet))
	#print (s.sentenceSenses (subjWords,subjWordSet))
	for ls in objSentences:
		for se in ls: 
			print (se,fu.dependencyParser(se))
	for ls in subjSentences:
		for se in ls: 
			print (se,fu.dependencyParser(se))
	
if __name__ == "__main__":
    
    main()


