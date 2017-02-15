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
				if (lemmas[k] in wordSets[i]): # the words is an adjective or an adverb or a noun or a verb
					offset = dbc.offsetSearch(lemmas[k], tags[k][0])
					if(len(offset)):
						for l in range (len(offset)):
							gloss  = dbc.glossSearch(offset[l][0])
							senses.append(gloss[0][0]) # single tuple with 1 element
					else:
						senses.append('-')	#sense not found
				else:
					senses.append('-')	#sense not found
				sentence.append(senses)
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
	text=text.strip()#end of line
	return text
	
def readFile(fileName,encode): 
	lines=[]
	with open(fileName,'r',encoding=encode) as f:
		for line in f:
			lines.append(cleanSentence(line))
	return lines	
    						

def splitSentence(sentence):
	sentences = [s for s in sentence.split(".") if s] # get all sentences for each opinion
	ans = []
	for i in range (len(sentences)): # get each word for every sentence
		words = [s for s in sentences[i].split(" ") if s]
		ans.append(words)
	return ans



