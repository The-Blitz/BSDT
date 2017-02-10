# coding=utf-8
import sentences as s;
import freelingUser as fu;


#falta split (para más oraciones y tokenizar cada una)
sentence = ["Vería" , "esa" , "película" ,"de" , "baja", "estofa", "una" , "y" , "otra" , "vez" , "sin" , "parar"]

result=s.procSentence(sentence)
words,lemmas,tags=fu.procText(result)
print (words,lemmas,tags)


fileName = 'Corpus/spanish_objectives_filmaffinity_2500'
objFile = s.readFile(fileName,'latin-1')
fileName = 'Corpus/spanish_subjectives_filmaffinity_2500'
subjFile  =s.readFile(fileName,'utf-8')


#for i in range(len(subjFile)):
#	aux = fu.procText(subjFile[i])
#	print (aux)

#aux = fu.procText(subjFile[0])
#print (aux)
#print (s.procSentence(aux[0]))
