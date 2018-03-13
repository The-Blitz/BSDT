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
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import validation_curve
from sklearn.preprocessing import normalize
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import features as fe
import tkinter
from tkinter import messagebox

import warnings
warnings.filterwarnings('ignore')

np.set_printoptions(threshold=np.nan) #show full dataset

def readData(fileName): # relations as features
	data=[]
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
	return npData,target
	
def readData2(fileName): # words as features
	data=[]
	target=[]
	cont=0
	with open(fileName,'r',encoding='utf-8') as f:
		for line in f:
			feat = [l for l in line.split() if l]
			auxList = fe.createWordDict()
			target.append(feat[0])
			for i in range(1,len(feat),2):
				feature = feat[i]
				#if(feature[2:]=='NS'):continue #ignore NS
				auxList[feature] = int(feat[i+1])	
			data.append(auxList)	
			cont+=1

	npData=pd.DataFrame(data).values
	return npData,target

def readData3(fileName1,fileName2): # relations and words together as features
	data=[]
	target=[]
	cont=0
	with open(fileName1,'r',encoding='utf-8') as f1, open(fileName2,'r',encoding='utf-8') as f2:
		for line1,line2 in zip(f1,f2):
			feat1 = [l for l in line1.split() if l]
			feat2 = [l for l in line2.split() if l]
			auxList1 = fe.createDict()
			auxList2 = fe.createWordDict()
			target.append(feat1[0]) # feat1[0] and feat2[0] are the same
			for i in range(1,len(feat1),3):
				feature = feat1[i]+" " + feat1[i+1]
				auxList1[feature] = int(feat1[i+2])	
			for i in range(1,len(feat2),2):
				feature = feat2[i]
				auxList2[feature] = int(feat2[i+1])
			auxList={**auxList1, **auxList2}			
			data.append(auxList)	
			cont+=1

	npData=pd.DataFrame(data).values
	return npData,target		

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

def get_importances(clf,data):
	#featList=sorted(list(fe.createDict().keys()))
	featList=sorted( list(fe.createDict().keys()) + list(fe.createWordDict().keys()) )
	importance=clf.feature_importances_
	indices = np.argsort(importance)[::-1]

	for f in range(data.shape[1]):
		print("%d. feature %s (%f)" % (f + 1, featList[indices[f]], importance[indices[f]]))

def plotValidationCurve(name,param,clf,X,y):
	#param_range = [1,10,100]
	param_range = np.logspace(-6, 6, 4)
	train_scores, test_scores = validation_curve(clf, X, y, param_name=param, param_range=param_range, cv=10,scoring="accuracy",n_jobs=1)
	train_scores_mean = np.mean(train_scores, axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	test_scores_mean = np.mean(test_scores, axis=1)
	test_scores_std = np.std(test_scores, axis=1)

	plt.title("Validation Curve with " + name)
	plt.xlabel(param)
	plt.ylabel("Score")
	plt.ylim(0.0, 1.1)
	lw = 2
	plt.semilogx(param_range, train_scores_mean, label="Training score",
    	         color="darkorange", lw=lw)
	plt.fill_between(param_range, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2,
                 color="darkorange", lw=lw)
	plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
             	color="navy", lw=lw)
	plt.fill_between(param_range, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.2,
                 color="navy", lw=lw)
	plt.legend(loc="best")
	#plt.show()
	plt.savefig('image.jpg')

def plotROCCurve(models , predictions , test):
	for i in range(len(models)):
		fpr, tpr, thresholds = roc_curve(test, predictions[i], pos_label='S')
		roc_auc  = auc(fpr, tpr)
		plt.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % (models[i], roc_auc))
		
	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.0])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.legend(loc=0, fontsize='small')
	#plt.show()
	plt.savefig('image.jpg')
	
	
def searchParameters(X_test,X_train,Y_test,Y_train):	
	#plotValidationCurve('random' , 'n_estimators' , random , X_train, Y_train)
	
	#predictions = []
	
	mlp  = MLPClassifier()
	parameters={'hidden_layer_sizes': [(12),(8,4,2),(9,3)], 'activation': ["logistic", "relu", "tanh"], 
	'solver' : ['adam'],'alpha':[0.01,0.1,1,10,100], 'learning_rate': ["constant", "invscaling", "adaptive"],'random_state': [42]}
	prob=test_clasif('mlp',mlp,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	svc = svm.SVC()
	parameters={'C': [0.00001, 0.0001,0.001, 0.01, 0.1, 1],	'kernel': ['linear','poly','rbf'],
	'gamma' : [0.001 , 0.01 , 0.1],'random_state':[0] , 'probability':[True]}
	prob=test_clasif('svm',svc,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	lr  = LogisticRegression()
	parameters={'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],'random_state':[0]}
	prob=test_clasif('logistic',lr,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	lda = LinearDiscriminantAnalysis()
	parameters={'solver':['svd','lsqr']}
	prob=test_clasif('lda',lda,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective']);
	#predictions.append(prob)
	
	knn = KNeighborsClassifier()
	parameters={'n_neighbors':[5,9,11,15,20,25,33],'weights':['uniform','distance'],'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
	prob=test_clasif('k neighbors',knn,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	tree= DecisionTreeClassifier()
	parameters={'criterion':['gini','entropy'],'splitter':['random','best'],'max_features':['sqrt','log2',None],'random_state':[0]}
	prob=test_clasif('decision tree',tree,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	bayes= GaussianNB()
	parameters={'priors':[None]}
	prob=test_clasif('naive bayes',bayes,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	sgd = SGDClassifier()
	parameters={'loss':['log', 'modified_huber'],'alpha':[0.00001,0.0001,0.001,0.01,0.1,1],'epsilon':[0.01,0.1,1],'random_state':[0]}
	prob=test_clasif('sgd',sgd,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	random= RandomForestClassifier()
	parameters={'n_estimators':[5,10,15,20,25,30],'criterion':['gini','entropy'],'max_features':['sqrt','log2',None],'random_state':[0]}
	prob=test_clasif('random forest',random,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	#predictions.append(prob)
	
	#plotROCCurve(['mlp','svm','logistic' , 'lda', 'knn','decision tree','Naive Bayes' , 'sgd' , 'random forest'], predictions,Y_test)

def showResults(X_test,X_train,Y_test,Y_train):

	mlp  = MLPClassifier()
	parameters={'hidden_layer_sizes': [(12,)], 'activation': ["tanh"], 'solver' : ['adam'],'alpha':[0.1], 'learning_rate': ["constant"],'random_state': [42]}
	prob=test_clasif('mlp',mlp,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])
	
	svc = svm.SVC()
	parameters={'C': [1],	'kernel': ['rbf'],'gamma' : [0.01],'random_state':[0] , 'probability':[True]}
	prob=test_clasif('svm',svc,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])	
	
	sgd = SGDClassifier()
	parameters={'loss':['modified_huber'],'alpha':[1],'epsilon':[0.01],'random_state':[0]}
	prob=test_clasif('sgd',sgd,X_test,X_train,Y_test,Y_train,parameters,['objective','subjective'])

	#vclf = VotingClassifier(estimators=[('mlp', mlp), ('svm', svc), ('sgd', sgd)], voting='soft')
	#scores = cross_val_score(vclf,X_train,Y_train,scoring='accuracy', cv = 10)
	#print("%0.3f (+/-%0.03f) "% (scores.mean(), scores.std() * 2))
	

def normalization(trainData,testData):
	scaler = StandardScaler()
	norm_train = scaler.fit_transform(trainData)
	norm_test = scaler.transform(testData)
	return norm_train,norm_test

def dimReduction(trainData,testData,trainTarget):
	clf = ExtraTreesClassifier(n_estimators=10,random_state=0)	
	clf = clf.fit(trainData,trainTarget) 
	model=SelectFromModel(clf,prefit=True) 
	ex_trainData=model.transform(trainData) 
	ex_testData=model.transform(testData) 
	#get_importances(clf,trainData)
	return ex_trainData,ex_testData

def normAndRed(trainData,testData,trainTarget):
	norm_train,norm_test=normalization(trainData,testData)
	ex_trainData,ex_testData=dimReduction(norm_train,norm_test,trainTarget)	
	return ex_trainData,ex_testData
	
def clasif_results():
	trainFile1S  = 'Semcor/featSemcor.txt'
	trainFile2S  = 'Semcor/wordSemcor.txt'
	trainFile1A  = 'Record/Results/featListA.txt'
	trainFile2A  = 'Record/Results/wordListA.txt'	
	testFile1   = 'Results/Test/featList1.txt'
	testFile2   = 'Results/Test/wordList1.txt'
	
	#trainData,trainTarget=readData(trainFile1A)
	#testData,testTarget=readData(testFile1)	
	#trainData,trainTarget=readData2(trainFile2A)
	#testData,testTarget=readData2(testFile2)	
	#trainData,trainTarget=readData3(trainFile1A,trainFile2A)
	#testData,testTarget=readData3(testFile1,testFile2)
	
	trainData1,trainTarget1=readData3(trainFile1S,trainFile2S)
	trainData2,trainTarget2=readData3(trainFile1A,trainFile2A)
	testData,testTarget=readData3(testFile1,testFile2)	
	
	trainData   = np.concatenate((trainData1,trainData2))
	trainTarget = trainTarget1 + trainTarget2	
	
	X_test = testData 
	X_train = trainData
	Y_test = testTarget
	Y_train = trainTarget
	
	#X_train,X_test=normalization(X_train,X_test)
	#X_train,X_test=dimReduction(X_train,X_test,Y_train)
	#X_train,X_test=normAndRed(X_train,X_test,Y_train)
	
	#searchParameters(X_test,X_train,Y_test,Y_train)
	showResults(X_test,X_train,Y_test,Y_train)

def init_clasif():
	trainFile  = 'Semcor/featSemcor.txt'
	data,target=readData(trainFile)
	clf = ExtraTreesClassifier(n_estimators=10,random_state=0)
	clf = clf.fit(data,target)
	
	model=SelectFromModel(clf,prefit=True)
	ex_data=model.transform(data)
	
	#sgd = SGDClassifier()
	#parameters={'loss':['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 
	#'huber','epsilon_insensitive','squared_epsilon_insensitive'],'alpha':[0.0001,0.001,0.01,0.1,1],'epsilon':[0.01,0.1,1],'random_state':[0]}
	
	bayes= GaussianNB()
	parameters={'priors':[None]}
	
	gridCV = GridSearchCV(bayes,parameters,scoring='accuracy', cv = 10)
	gridCV.fit(ex_data,target)	


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
	#global app_clasif,model
	#app_clasif,model = init_clasif()
	#app = Application()
	#app.mainloop()
	clasif_results()
	
	
if __name__ == "__main__":
    
    main()
