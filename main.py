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
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

import numpy as np
import pandas as pd
import features as fe
import tkinter
from tkinter import messagebox

import warnings
warnings.filterwarnings('ignore')

#np.set_printoptions(threshold=np.nan) show full dataset

def readData(fileName):
	data=[]
	featList=list(fe.createDict().keys())
	target=[]
	cont=0
	with open(fileName,'r',encoding='utf-8') as f:
		for line in f:
			feat = [l for l in line.split() if l]
			auxList = fe.createDict()
			target.append(feat[0])
			for i in range(1,len(feat),3):
				feature = feat[i]+" " + feat[i+1]
				auxList[feature] = int(feat[i+2])	
			data.append(auxList)	
			cont+=1

	npData=pd.DataFrame(data).values
	return npData,target,featList

def test_clasif(name,clasi,X_test,X_train,Y_test,Y_train,parameters,classes):
	with warnings.catch_warnings():
		gridCV = GridSearchCV(clasi,parameters,scoring='accuracy', cv = 5)
		gridCV.fit(X_train,Y_train)
		result = gridCV.predict(X_test)
		print(name)
		print(classification_report(result,Y_test,target_names=classes))
		print(confusion_matrix(result,Y_test))

def get_importances(clf,data,featList):
	importance=clf.feature_importances_
	indices = np.argsort(importance)[::-1]

	for f in range(data.shape[1]):
		print("%d. feature %s (%f)" % (f + 1, featList[indices[f]], importance[indices[f]]))

def mySplit(data,target):
	X_test=[];X_train=[];Y_test=[];Y_train=[];
	for i in range(data.shape[0]):# 500 
		if(i<88):
			X_train.append(data[i])
			Y_train.append(target[i])
		elif(i<163):
			X_test.append(data[i])
			Y_test.append(target[i])	
		elif(i<250):
			X_train.append(data[i])
			Y_train.append(target[i])
		elif(i<337):
			X_train.append(data[i])
			Y_train.append(target[i])
		elif(i<412):
			X_test.append(data[i])
			Y_test.append(target[i])	
		else:
			X_train.append(data[i])
			Y_train.append(target[i])
	X_test=pd.DataFrame(X_test).values
	X_train=pd.DataFrame(X_train).values		
	return X_test,X_train,Y_test,Y_train

def clasif_results():
	fileName  = 'Results/featList1.txt'
	data,target,featList=readData(fileName)
	clf = ExtraTreesClassifier(n_estimators=10,random_state=0)
	clf = clf.fit(data,target)
	model=SelectFromModel(clf,prefit=True)
	ex_data=model.transform(data)
	#get_importances(clf,data,featList)
	X_test,X_train,Y_test,Y_train= mySplit(ex_data,target)
	
	#svc = svm.SVC()
	#parameters={'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],	'kernel': ['linear','poly','rbf'],'gamma' : 10.0**-np.arange(1,4),'random_state':[0]}
	#test_clasif('svm',svc,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#lr  = LogisticRegression()
	#parameters={'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],'random_state':[0]}
	#test_clasif('logistic',lr,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#lda = LinearDiscriminantAnalysis()
	#parameters={'solver':['svd','lsqr','eigen']}
	#test_clasif('lda',lda,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective']);
	
	#knn = KNeighborsClassifier()
	#parameters={'n_neighbors':[1,3,5,7,9,11],'weights':['uniform','distance'],'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
	#test_clasif('k neighbors',knn,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#tree= DecisionTreeClassifier()
	#parameters={'criterion':['gini','entropy'],'splitter':['random','best'],'max_features':['sqrt','log2',None],'random_state':[0]}
	#test_clasif('decision tree',tree,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#bayes= GaussianNB()
	#parameters={'priors':[None]}
	#test_clasif('naive bayes',bayes,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#sgd = SGDClassifier()
	#parameters={'loss':['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 
	#'huber','epsilon_insensitive','squared_epsilon_insensitive'],'alpha':[0.0001,0.001,0.01,0.1,1],'epsilon':[0.01,0.1,1],'random_state':[0]}
	#test_clasif('sgd',sgd,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	#random= RandomForestClassifier()
	#parameters={'n_estimators':[5,10,15,20,25,30],'criterion':['gini','entropy'],'max_features':['sqrt','log2',None],'random_state':[0]}
	#test_clasif('random forest',random,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	

def init_clasif():
	fileName  = 'Results/featList1.txt'
	data,target,featList=readData(fileName)
	clf = ExtraTreesClassifier(n_estimators=10,random_state=0)
	clf = clf.fit(data,target)
	
	model=SelectFromModel(clf,prefit=True)
	ex_data=model.transform(data)
	X_test,X_train,Y_test,Y_train= mySplit(ex_data,target)
	
	#sgd = SGDClassifier()
	#parameters={'loss':['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 
	#'huber','epsilon_insensitive','squared_epsilon_insensitive'],'alpha':[0.0001,0.001,0.01,0.1,1],'epsilon':[0.01,0.1,1],'random_state':[0]}
	
	bayes= GaussianNB()
	parameters={'priors':[None]}
	
	gridCV = GridSearchCV(bayes,parameters,scoring='accuracy', cv = 5)
	gridCV.fit(X_train,Y_train)	


	print('se inicializo el clasificador')
	return gridCV,model

def clasif_sent(features):
	listFeat= []
	listFeat.append(features)
	
	realFeat=model.transform(pd.DataFrame(listFeat))
	#print(realFeat)
	
	result = app_clasif.predict(realFeat)
	#print(result)
	if(result[0]=='O'):	return 'objetivo'	
	if(result[0]=='S'):	return 'subjetivo'




sentence = ''
app_clasif = None
model = None

class Application(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		container = tkinter.Frame(self)
		self.title("BSDT")
		self.minsize(width=800, height=100)
		self.resizable(width=False, height=False)
		self.protocol("WM_DELETE_WINDOW", self.close_window)
		container.pack(side="top", fill="both", expand = True)
		self.frames = {}
		for F in (FirstScreen, TextScreen,AnsScreen):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
            
		self.show_frame(FirstScreen)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
	
	def close_window(self):
		#tkinter.tkMessageBox.askokcancel()
		print('closing')
		self.quit()
	
	def process(self):
		self.frames[TextScreen].textFrame.getText()
		self.frames[AnsScreen].textFrame.showText()
		self.show_frame(AnsScreen)	
	
	def restart(self):
		global sentence
		sentence=''
		self.frames[TextScreen].textFrame.clear()
		self.frames[AnsScreen].textFrame.clear()
		self.show_frame(FirstScreen)	

class entryBox(tkinter.Frame):
	def __init__(self,parent):
		tkinter.Frame.__init__(self,parent)
		self.text = tkinter.Text(self,bg=parent.cget('bg'), bd=0,fg='black',height=1, width=80)
		self.text.insert('1.0', "Por favor escriba la oración que desee evaluar:")
		self.text.config(state='disabled')
		self.text.pack()
		self.entry = tkinter.Entry(self, width=70)
		self.entry.pack()
		
	def getText(self):
		global sentence
		sentence =self.entry.get()
		self.clear()
		
	def clear(self):
		self.entry.delete(0, 'end')		
		
class resultBox(tkinter.Frame):
	def __init__(self,parent):
		tkinter.Frame.__init__(self,parent)
		scroll = tkinter.Scrollbar(self)
		scroll.pack(side = 'top')
		self.text = tkinter.Text(self,bg="white", bd=0,fg='black',height=1, width=80,yscrollcommand =scroll.set)
		scroll.config(command = self.text.yview, orient='horizontal')
		self.text.tag_configure("NS", background="white")
		self.text.tag_configure("LS", background="green", foreground="white")
		self.text.tag_configure("MS", background="yellow", foreground="white")
		self.text.tag_configure("HS", background="red", foreground="white")
		self.typeText=tkinter.Text(self,bg=parent.cget('bg'), bd=0,fg='black',height=1, width=80)
	
	def showText(self):
		features,sentSubj,words = fe.sentToFeat(sentence)

		for s in range(len(words)):
			for w in range(len(words[s][0])):
				self.text.insert('end',words[s][0][w]+" ",sentSubj[s].get(w+1, "NS"))
		self.text.config(state='disabled')
		self.text.pack()
		
		result = clasif_sent(features)
		#print(result)
		self.typeText.insert('end',"La oración es de tipo "+result+".")
		self.typeText.config(state='disabled')
		self.typeText.pack()
		
	def clear(self):
		self.text.config(state='normal')
		self.text.delete(1.0,'end')
		self.typeText.config(state='normal')
		self.typeText.delete(1.0,'end')	
		
class FirstScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		tkinter.Frame.__init__(self,parent)
		start= tkinter.Button(self, text = "Inicio", command= lambda: controller.show_frame(TextScreen) , height=2, width=20)
		quit = tkinter.Button(self, text = "Salir", command = lambda: controller.close_window(),height=2, width=20)
		start.pack(side=tkinter.LEFT,padx=100, pady=0)
		quit.pack( side=tkinter.RIGHT,padx=100, pady=0)

class TextScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		tkinter.Frame.__init__(self,parent)
		self.textFrame =  entryBox(self)
		self.textFrame.pack()
		start = tkinter.Button(self, text = "Empezar", command = lambda:controller.process() ,height=2, width=20)
		quit= tkinter.Button(self,  text = "Volver al Inicio", command= lambda: controller.restart() , height=2, width=20)
		start.pack(side=tkinter.LEFT,padx=100, pady=0)
		quit.pack( side=tkinter.RIGHT,padx=100, pady=0)


class AnsScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		tkinter.Frame.__init__(self,parent)
		self.textFrame =  resultBox(self)
		self.textFrame.pack()
		restart= tkinter.Button(self,  text = "Volver al Inicio", command= lambda: controller.restart() , height=2, width=20)
		quit = tkinter.Button(self, text = "Salir", command = lambda: controller.close_window(),height=2, width=20)
		restart.pack(side=tkinter.LEFT,padx=100, pady=0)
		quit.pack( side=tkinter.RIGHT,padx=100, pady=0)	
	
def main():
	global app_clasif,model
	app_clasif,model = init_clasif()
	app = Application()
	app.mainloop()
	#clasif_results()
	
	
if __name__ == "__main__":
    
    main()
