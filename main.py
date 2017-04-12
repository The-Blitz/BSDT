import features as fe


def main():
	#TODO
	features = fe.generate()
	cont =1
	f = open('featList1.txt','a+')
	for feat in features:
		for aux in feat:
			if (feat[aux]>0):
				f.write("%d %s %d\n" % (cont,aux,feat[aux]))
		cont +=1		
	f.close()
	print("Nuevo Main")


if __name__ == "__main__":
    
    main()
