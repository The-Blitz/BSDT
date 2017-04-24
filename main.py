from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn import datasets
from sklearn import svm
import numpy as np
import pandas as pd

def readData(fileName):
	data=[]
	featList=[]
	target=[]
	cont=0
	with open(fileName,'r',encoding='utf-8') as f:
		for line in f:
			feat = [l for l in line.split() if l]
			if(cont==0):
				for i in range(1,len(feat),2):
					featList.append(feat[i]+ "-" +feat[i+1])
			else:
				auxList = dict()
				target.append(feat[0])
				for i in range(1,len(feat)):
					auxList[featList[i-1]] = int(feat[i])	
				data.append(auxList)	
			cont+=1
	
	npData=pd.DataFrame(data).values
	return npData,target

def main():
	#TODO
	fileName  = 'featList.txt'
	data,target=readData(fileName)	
	#X_train, X_test, y_train, y_test = train_test_split(data,target, test_size=0.40)
	svc = svm.SVC(kernel='linear', C=1)#.fit(X_train, y_train) 
	#ans_poly=svc.predict(X_test)
	#acc_poly=svc.score(X_test,y_test)
	#print (ans_poly ,"accuracy=", acc_poly)
	scores = cross_val_score(svc, data, target, cv=5)
	print ("Usando cross validation: " , ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)))
	result = cross_val_predict(svc, data, target, cv=5)
	#print(result)


if __name__ == "__main__":
    
    main()
