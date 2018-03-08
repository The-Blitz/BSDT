fileName = 'markup.txt'	
with open(fileName,'r') as f:
	for line in f:
		unk = line.find("\"" + "unknown" + "\"")
		if(unk != -1) : print('-1') #unknown
		else:
			obj = line.find("\"" + "obj" + "\"")
			subj = line.find("\"" + "subj" + "\"")
			if(obj == -1 and subj == -1) : print('-1')#unknown
			elif(obj == -1) :  print('1')#subj
			elif(subj == -1) : print('0')#obj
			elif(obj < subj) :  print('0')#obj
			elif(obj > subj) :  print('1')#subj
