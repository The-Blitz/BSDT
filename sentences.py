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
		if( (len(senses)==0 ) or (i>cont and noSense(senses,auxSense) ) or (text[i]=='.') ):
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

def existSense(senses, auxSense): #if the exact sense exist
	for i in range(len(senses)):
		#print(senses[i][0])
		if(auxSense.lower()==senses[i][0].lower()):	return True;
	return False;

def noSense(senses,auxSense): # if the current sense or possible connections with it doesn't exist
	for i in range(len(senses)):
		auxi = senses[i][0][:len(auxSense)]
		if(auxSense.lower()==auxi.lower()):	return False;
	return True;

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
	result = []
	for j in range (len (sentences)): # words in a single sentence
		sent=[]
		words  = sentences[j][0]
		lemmas = sentences[j][1]
		tags   = sentences[j][2]
		for k in range (len (lemmas) ):
			senses = []
			synonyms= []
			auxOffset= []
			auxOntology = []
			if ((lemmas[k]+' '+str(k+1)) in wordSets[j]): # the word is an adjective or an adverb or a noun or a verb
				offset = dbc.offsetSearch(lemmas[k], tags[k][0])
				if(len(offset)):
					for l in range (len(offset)):
						auxOffset.append(offset[l][0])
						ontology = (dbc.ontologySearch(offset[l][0]))
						if (len(ontology)): # if there is an ontology
							auxiOnt = []
							for m in range( len(ontology) ):
								auxiOnt.append(ontology[m][0])
							auxOntology.append(auxiOnt)
						else:
							auxOntology.append('-')	
							
						gloss  = dbc.glossSearch(offset[l][0])
						if (gloss[0][0]!='None'): # if there is a gloss
							senses.append(gloss[0][0]) # single tuple with 1 element
						else:
							senses.append('-')	
							
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
			sent.append(((words[k],lemmas[k],tags[k]),auxOffset,auxOntology,synonyms,senses))
		result.append(sent)		 
	return result		
				

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
		words = [s.lower() for s in sentences[i].split(" ") if s] # lower all words
		if (not words):	continue;
		if(flag):
			for j in range(len (words)):
				aux.append(words[j]) 
			aux.append(".")
		else:
			words.append(".")
			ans.append(words)
	if(flag):
		ans.append(aux)	
	return ans


