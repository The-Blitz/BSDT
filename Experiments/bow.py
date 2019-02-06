#TESTING BAG OF WORDS
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report,confusion_matrix
import numpy
import math
from html.parser import HTMLParser

import warnings
warnings.filterwarnings('ignore')


def readFile1(fileName,encode): #READ ANNOTATION
	lines=[]
	words = []
	cont=1
	with open(fileName,'r',encoding=encode) as f:	
		for line in f:
			line=line.strip()
			line = [l for l in line.split(" ") if l]
			if(cont== int(line[0]) ): words.append(line[2])
			else:
				cont = (cont%200) +1
				lines.append(words)
				words=[]
				words.append(line[2])
	lines.append(words)		
	return lines


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
	
def readFile2(fileName,encode): #READ TEST SENTENCES
	lines=[]
	with open(fileName,'r',encoding=encode) as f:
		for line in f:
			line = cleanSentence(line)
			line = [l for l in line.split(" ") if l]
			lines.append(line)
	return lines	


def genBOW(sentences):
    words = []
    for sentence in sentences:
        words.extend(sentence)
        
    words = sorted(list(set(words)))
    return words

def genTF(sentences,vocab): #generate TF 
	tf = []
	for s in sentences:
		feq_vector = numpy.zeros(len(vocab))
		for w in s:
			for i,word in enumerate(vocab):
				if word == w: 
					feq_vector[i] += 1
		
		for i,word in enumerate(vocab):			
			feq_vector[i] = feq_vector[i] / len(s)
			
		tf.append(feq_vector)	
		#print("{0}\n{1}\n".format(s,numpy.array(feq_vector)))
	return tf
    	

def genIDF(sentences,vocab): #generate IDF
	idf = numpy.ones(len(vocab))
	
	for i,w in enumerate(vocab):
		cont = 1
		for s in sentences:
			if w in s: cont = cont + 1

		idf[i] = idf[i] * math.log( len(sentences) / cont) 	
		
	return idf

def genTFIDF(sentences, vocab): # TFIDF
	tfidf = []
	tf = genTF(sentences,vocab)
	idf = genIDF(sentences,vocab)
	
	for v in tf:
		vect = numpy.ones(len(vocab))
		for i,num in enumerate(v):
			vect[i] = vect[i] * num *idf[i]	
		tfidf.append(vect)
	return tfidf	

def test_clasif(name,clasi,X_test,X_train,Y_test,Y_train,parameters,classes):
	le = LabelEncoder()
	Y_train=le.fit_transform(Y_train)
	Y_test=le.transform(Y_test)
	with warnings.catch_warnings():
		gridCV = GridSearchCV(clasi,parameters,scoring='accuracy', cv = 10)
		gridCV.fit(X_train,Y_train)
		result = gridCV.predict(X_test)
		bestParams=gridCV.best_params_
		#print(bestParams)
		
		means = gridCV.cv_results_['mean_test_score']
		stds = gridCV.cv_results_['std_test_score']
		for mean, std, params in zip(means, stds, gridCV.cv_results_['params']):
			if(params==bestParams):
				print("%0.3f (+/-%0.03f) for %r"
				% (mean, std * 2, params))
		
		print(name)
		print(classification_report(result,Y_test,target_names=classes))
		print(confusion_matrix(result,Y_test))
	return gridCV.predict_proba(X_test)[:,1]	

def decidedFunction(X_test,X_train,Y_test,Y_train):
	svc = svm.SVC()
	parameters={'C': [0.01],	'kernel': ['linear'],'gamma' : [0.001],'random_state':[0] , 'probability':[True]}
	prob=test_clasif('svm',svc,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])	

	
	
	
	
fileNameTrain  = 'result-A.txt'
fileNameTest  = 'testSent.txt'
sentences1 = readFile1(fileNameTrain,'utf-8')
sentences2 = readFile2(fileNameTest,'utf-8')
vocab = genBOW(sentences1)

x_train = genTFIDF(sentences1,vocab)
y_train = [ 'O' if (i//200==0) else "S" for i in range(0,400) ]
x_test = genTFIDF(sentences2,vocab)
y_test = [ 'O' if (i//250==0) else "S" for i in range(0,500) ]

decidedFunction(x_test,x_train,y_test,y_train)

