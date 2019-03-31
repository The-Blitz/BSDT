#with open('sumo.txt','r',encoding='utf-8') as f:
#	for line in f:
#		line = line.strip('\n')
#		line = line.split('\t')
#		if(line[3] == "SubjectiveAssessmentAttribute"): 
#		    #print(line[0],line[1],line[2],line[3],line[4] )
#			print("spa" + line[0][3:] )		

ontodict = set()
with open('resultsumo.txt','r',encoding='utf-8') as f:
	for line in f:
		line = line.strip('\n')
		line = line.split('\t')
		ontodict.add(line[0])


with open('result-Freq.txt','r',encoding='utf-8') as f:
	for line in f:
		line = line.strip('\n')
		line = line.split(' ')
		if(line[3] in ontodict):
		    print(line[3] , line[4]) 
		    

