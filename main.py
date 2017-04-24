import features as fe

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
					auxList[featList[i-1]] = feat[i]	
				data.append(auxList)	
			cont+=1	
	return data,target

def main():
	#TODO
	fileName  = 'featList.txt'
	data,target=readData(fileName)	


if __name__ == "__main__":
    
    main()
