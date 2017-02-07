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
				return (text[i],i+1)
			#checking words and phrases
			return auxSense,i
		if(auxSense==""):
			auxSense= text[i]
		else:
			auxSense= auxSense+"_" +text[i]
	return auxSense, len(text)


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
	text=text.replace("& ;#8203;&#8203;" ,"") #just1
	#lin=text.split(' ')	
	print(text)
	#print (lin)
	
def readFile(fileName): 
	with open(fileName,'r') as f:
		for line in f:
			cleanSentence(line)
    			
#sentence = ["Vería" , "esa" , "película" , "una" , "y" , "otra" , "vez" , "sin" , "parar"]
#sentence  = ["dime" , "si" , "te", "sientes" , "cansada"]
#result=procSentence(sentence)
#print (result)


