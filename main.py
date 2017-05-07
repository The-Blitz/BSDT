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

def clasif_results():
	fileName  = 'test.txt'
	data,target=readData(fileName)
	clf = ExtraTreesClassifier()
	clf.fit(data,target)
	model=SelectFromModel(clf,prefit=True)
	ex_data=model.transform(data)
	#print(clf.feature_importances_)
	#print(ex_data.shape)
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

sentence = ''

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
		text = tkinter.Text(self,bg=parent.cget('bg'), bd=0,fg='black',height=1, width=80)
		text.insert('1.0', "Por favor escriba la oración que desee evaluar:")
		text.config(state='disabled')
		text.pack()
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
		self.entry = tkinter.Entry(self, width=70)
	
	def showText(self):
		self.entry.insert(0,sentence)
		self.entry.config(state='readonly',readonlybackground='white')
		self.entry.pack()
	
	def clear(self):
		self.entry.config(state='normal')
		self.entry.delete(0, 'end')		
		
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
	#app = Application()
	#app.mainloop()
	#features,sentSubj,words = fe.sentToFeat('Un festival, de caracterizaciones cachoNDAS')
	#print(sentSubj,words)

if __name__ == "__main__":
    
    main()
