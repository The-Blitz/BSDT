# coding=utf-8
import dbConn as dbc;
import numpy as np;

def verif(cont, text):
	auxSense=""
	for i in range(cont, len(text)):
		if(auxSense==""):
			senses= dbc.senseSearch(text[i])
		else:
			senses= dbc.senseSearch(auxSense+"_" +text[i])	
		if( (len(senses)==0 ) or (i>cont and senses[0][0][len(auxSense)] != "_" )  ):
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
    result=[];
    for i in range(sz):
    	if vis[i]!=0:
    		continue
    	word,counter = verif(i,text)
    	for j in range(i,counter):
    		vis[j]=1
    	if word :
    		result.append(word)
    return result
   

sentence = ["Vería" , "esa" , "película" , "una" , "y" , "otra" , "vez"]
#sentence  = ["dime" , "si" , "te", "sientes" , "cansada"]
result=procSentence(sentence)
print (result)
