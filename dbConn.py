# coding=utf-8
import MySQLdb;

def senseSearch(text): # text = word or phrase you're looking for
	db = MySQLdb.connect("localhost","root","admin","mcr30" )
	cursor= db.cursor()
	cursor.execute("SELECT * FROM `wei_spa-30_variant` where upper(word) like upper('" + text +"%')" )
	ans=cursor.fetchall()
	db.close()
	return ans;

def offsetSearch(lemma , tag) : # the id or offset related to the wordnet 
	 db = MySQLdb.connect("localhost","root","admin","mcr30" )
	 cursor= db.cursor()
	 cursor.execute("SELECT offset FROM `wei_spa-30_variant` where upper(word) like upper('" + lemma +"') and upper(pos) like upper('" + tag +"') "  )
	 ans=cursor.fetchall()
	 db.close()
	 return ans;
	 
def synonymSearch(offset):
	 db = MySQLdb.connect("localhost","root","admin","mcr30" )
	 cursor= db.cursor()
	 cursor.execute("SELECT word FROM `wei_spa-30_variant` where upper(offset) like upper('" + offset +"')"  )
	 ans=cursor.fetchall()
	 db.close()
	 return ans;	 
	 
def glossSearch (offset) : # the meaning of the sense you're looking for	
	 db = MySQLdb.connect("localhost","root","admin","mcr30" )
	 cursor= db.cursor()
	 cursor.execute("SELECT gloss FROM `wei_spa-30_synset` where upper(offset) like upper('" + offset +"')"  )
	 ans=cursor.fetchall()
	 db.close()
	 return ans;

def searchSubjectivity(text): # text = sense ID
	db = MySQLdb.connect("localhost","root","admin","mcr30" )
	cursor= db.cursor()
	cursor.execute("SELECT * FROM `subjectivity` where id='" + text +"'")
	ans=cursor.fetchall()
	db.close()
    # table ( id , subj ,obj )
	subj=ans[0][1]
	obj =ans[0][2]
	return subj,obj;
