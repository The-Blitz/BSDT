import features as fe


def main():
	#TODO
	features = fe.generate()
	cont =1
	for feat in features:
		for aux in feat:
			if (feat[aux]>0):
				print(cont,aux,feat[aux])
		cont +=1		

	print("Nuevo Main")


if __name__ == "__main__":
    
    main()
