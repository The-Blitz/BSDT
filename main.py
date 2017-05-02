from sklearn import model_selection as ms
from sklearn import datasets
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.decomposition import PCA

import numpy as np
import pandas as pd
import features as fe
import warnings
warnings.filterwarnings('ignore')

def readData(fileName):
	data=[]
	featList=[]
	target=[]
	cont=0
	with open(fileName,'r',encoding='utf-8') as f:
		for line in f:
			feat = [l for l in line.split() if l]
			auxList = fe.createDict()
			target.append(feat[0])
			for i in range(1,len(feat),4):
				feature = feat[i]+" " + feat[i+1] + " "+ feat[i+2]
				auxList[feature] = int(feat[i+3])	
			data.append(auxList)	
			cont+=1
	
	npData=pd.DataFrame(data).values
	return npData,target

def test_clasif(name,clasi,data,target):
	with warnings.catch_warnings():
		result = ms.cross_val_predict(clasi, data, target, cv=5)
		print(name)
		print(classification_report(result,target))
		print(confusion_matrix(result,target))

def main():
	#TODO
	fileName  = 'test.txt'
	data,target=readData(fileName)
	print(data)
	'''
	svc = svm.SVC(kernel='linear', C=1)
	lr  = LogisticRegression()
	lda = LinearDiscriminantAnalysis()
	knn = KNeighborsClassifier()
	tree= DecisionTreeClassifier()
	bayes= GaussianNB()
	sgd = SGDClassifier()
	

	test_clasif('svm',svc,data,target);test_clasif('logistic',lr,data,target);test_clasif('lda',lda,data,target);
	test_clasif('k neighbors',knn,data,target);test_clasif('decision tree',tree,data,target);test_clasif('naive bayes',bayes,data,target);
	test_clasif('sgd',sgd,data,target);
	'''

if __name__ == "__main__":
    
    main()
