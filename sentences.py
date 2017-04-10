# coding=utf-8
import re
import dbConn as dbc;
import numpy as np;
from html.parser import HTMLParser

def verif(cont, text):
	auxSense=""
	for i in range(cont, len(text)):
		if(auxSense==""):
			senses= dbc.senseSearch(text[i])
		else:
			senses= dbc.senseSearch(auxSense+"_" +text[i])	
		if( (len(senses)==0 ) or (i>cont and senses[0][0][len(auxSense)] != "_" )  ):
			if(i==cont):	#unchecked words
				return text[i],i+1
				
			previous= dbc.senseSearch(auxSense)
			if(not existSense (previous , auxSense)): #checking if the current sense is valid	
				return text[cont], cont+1
				
			#return valid sense
			return auxSense,i
		if(auxSense==""):
			auxSense= text[i]
		else:
			auxSense= auxSense+"_" +text[i]
	return auxSense, len(text)

def existSense(senses, auxSense):
	for i in range(len(senses)):
		#print(senses[i][0])
		if(auxSense==senses[i][0]):	return True;
	return False;

def procSentence(text):
    sz= len(text)
    vis= np.zeros(sz)
    result="";
    for i in range(sz):
    	if vis[i]!=0:
    		continue
    	if i>0:	result= result+" "	
    	word,counter = verif(i,text)
    	for j in range(i,counter):
    		vis[j]=1
    	result= result+word
    return result

def sentenceSenses(sentences, wordSets):
	ans = []
	for i in range(len(sentences)): # all the opinions
		#print (wordSets[i])
		result = []
		for j in range (len (sentences[i])): # words in a single sentence
			sentence = []
			words  = sentences[i][j][0]
			lemmas = sentences[i][j][1]
			tags   = sentences[i][j][2]
			for k in range (len (lemmas) ):
				senses = []
				synonyms= []
				auxOffset= []
				auxOntology = []
				if (lemmas[k] in wordSets[i]): # the word is an adjective or an adverb or a noun or a verb
					offset = dbc.offsetSearch(lemmas[k], tags[k][0])
					if(len(offset)):
						for l in range (len(offset)):
							auxOffset.append(offset[l][0])
							ontology = (dbc.ontologySearch(offset[l][0]))
							if (len(ontology)): # if there is an ontology
								auxOntology.append(ontology[0][0])
							else:
								auxOntology.append('-')	
							gloss  = dbc.glossSearch(offset[l][0])
							senses.append(gloss[0][0]) # single tuple with 1 element
							
							syno   = dbc.synonymSearch(offset[l][0])
							if(len (syno) == 1) : synonyms.append('-') #the same
							else:
								auxiSyno = []
								for m in range (len (syno)):
									if(syno[m][0] != lemmas[k]): auxiSyno.append(syno[m][0])
								synonyms.append(auxiSyno)
					else:
						senses.append('-')	#sense not found
						synonyms.append('-')
						auxOffset.append('-')
						auxOntology.append('-')
				else:
					senses.append('-')	#sense not found
					synonyms.append('-')
					auxOffset.append('-')
					auxOntology.append('-')
				sentence.append(((words[k],lemmas[k],tags[k]),auxOffset,auxOntology,synonyms,senses))
			result.append(sentence)		 
		ans.append(result)
	return ans		
				

# clean html tags   
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()    
# clean html tags   

def cleanSentence(text):
	text=strip_tags(text)
	text=text.replace("'" ,"")
	text=text.replace("( . . . )" ,".")#split in sentences
	text=text.replace('\ufeff' ,"") #just 1 in utf-8
	text=text.replace("& ;#8203;&#8203;" ,"") #just1
	text=''.join([i if ord(i) < 256 else ' ' for i in text]) # removing not utf-8 characters
	text=text.strip()#end of line
	return text
	
def readFile(fileName,encode): 
	lines=[]
	with open(fileName,'r',encoding=encode) as f:
		for line in f:
			lines.append(cleanSentence(line))
	return lines	
    						

def splitSentence(sentence,flag):  # flag: 0 separate opinion in sentences, 1 sentences per opinion together
	sentences = [s for s in sentence.split(".") if s] # get all sentences for each opinion
	ans = []
	aux=[]
	for i in range (len(sentences)): # get each word for every sentence
		words = [s for s in sentences[i].split(" ") if s]
		if(flag):
			for j in range(len (words)):
				aux.append(words[j])
			aux.append(".")
		else:
			ans.append(words)
	if(flag):
		ans.append(aux)	
	return ans


