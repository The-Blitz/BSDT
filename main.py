import sentences as s;
import freelingUser as fu;


#falta split (para más oraciones y tokenizar cada una)
sentence = ["Vería" , "esa" , "película" , "una" , "y" , "otra" , "vez" , "sin" , "parar"]

result=s.procSentence(sentence)

words,lemmas,tags=fu.procText(result)
print (words,lemmas,tags)
