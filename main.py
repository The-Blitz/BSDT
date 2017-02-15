# coding=utf-8
import sentences as s;
import freelingUser as fu;

def procTextFile (filename):
	ans = []
	words = [] # adjectives, adverbs, nouns and verbs	
	for i in range(len(filename)):
		sentence = s.splitSentence(filename[i])
		result = []
		validTags = set()
		for j in range (len (sentence)):
			aux = s.procSentence(sentence[j])
			words,lemmas,tags=fu.procText(aux)
			result.append( (words,lemmas,tags) )
			for k in range ( len (tags) ):
				if(tags[k][0]=='A' or tags[k][0]=='N' or tags[k][0]=='R' or tags[k][0]=='V'):
					#print(words[k],lemmas[k])
					validTags.add(lemmas[k])
		#print(result)
		#print(validTags)	
		ans.append(result)
		words.append(validTags)	
	return ans,words
	
	
	
def main():
	fileName = 'Corpus/spanish_objectives_filmaffinity_2500'
	#fileName  = 'Corpus/objTest.txt'
	objFile = s.readFile(fileName,'utf-8')
	#fileName = 'Corpus/spanish_subjectives_filmaffinity_2500'
	fileName  = 'Corpus/subjTest.txt'
	subjFile  =s.readFile(fileName,'utf-8')
	
	objSentences,objWords  = procTextFile(objFile)
	subjSentences,subjWords = procTextFile(subjFile)


if __name__ == "__main__":
    
    main()


