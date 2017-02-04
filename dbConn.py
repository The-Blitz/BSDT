import MySQLdb;

def senseSearch(text): # text = word or phrase you're looking for
	db = MySQLdb.connect("localhost","root","admin","mcr30" )
	cursor= db.cursor()
	cursor.execute("SELECT * FROM `wei_spa-30_variant` where upper(word) like upper('" + text +"%')" )
	ans=cursor.fetchall()
	db.close()
	return ans;

def searchSubjectivity(text): # text = sense ID
	db = MySQLdb.connect("localhost","root","admin","mcr30" )
	cursor= db.cursor()
	cursor.execute("SELECT * FROM `subjectivity` where id='" + text +"'")
	ans=cursor.fetchall()
	db.close()
	#	posScore + negScore
	subj=ans[0][1] + ans[0][2];
	obj = 1 - subj;
	return subj,obj;
	

#aux=senseSearch("sueño"); 17 rows
#print (aux[16][2]);
#subj, obj= searchSubjectivity(aux[16][2]);
#print ("subjectivity = " + str(subj) + " objectivity = " +str(obj));

