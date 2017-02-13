# coding=utf-8
import sentences as s;
import freelingUser as fu;

#falta split (para más oraciones y tokenizar cada una)
def procTextFile (filename):
	ans = []
	for i in range(len(filename)):
		sentence = s.splitSentence(filename[i])
		result = []
		for j in range (len (sentence)):
			aux = s.procSentence(sentence[j])
			words,lemmas,tags=fu.procText(aux)
			result.append( (words,lemmas,tags) )
		print(result)	
		ans.append(result)	
	
	
def main():
	fileName = 'Corpus/spanish_objectives_filmaffinity_2500'
	objFile = s.readFile(fileName,'latin-1')
	fileName = 'Corpus/spanish_subjectives_filmaffinity_2500'
	subjFile  =s.readFile(fileName,'utf-8')
	
	objSentences  = procTextFile(objFile)
	subjSentences = procTextFile(subjFile)


if __name__ == "__main__":
    
    main()


