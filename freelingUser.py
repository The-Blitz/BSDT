# coding=utf-8
import sys
from Freeling import freeling;

def initFreeling():
	FREELINGDIR = "/usr/local";
	DATA = FREELINGDIR+"/share/freeling/";
	LANG="es";

	freeling.util_init_locale("default");
	
	# create options set for maco analyzer. Default values are Ok, except for data files.
	op= freeling.maco_options("es");
	op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
				   DATA + LANG + "/probabilitats.dat");

	# create analyzers
	tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
	sp=freeling.splitter(DATA+LANG+"/splitter.dat");
	#sid=sp.open_session();
	mf=freeling.maco(op);

	# activate mmorpho odules to be used in next call
	mf.set_active_options(False, True, True, True,  # select which among created 
                      	  True, True, False, True,  # submodules are to be used. 
						  True, True, True, True ); # default: all created submodules are used
	
	# create tagger, sense anotator, and parsers
	tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
	sen=freeling.senses(DATA+LANG+"/senses.dat");

	# create dependency parser
	parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
	#dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());
	dep=freeling.dep_treeler(DATA+LANG+"/dep_treeler/dependences.dat");
	return (tk,sp,mf,tg,sen,parser,dep)

def procText (text):
	ls= analyze(text)
	words=[]	
	lemmas=[]
	tags=[]
	for s in ls :
		ws = s.get_words();
		for w in ws :
			words.append(w.get_form())
			lemmas.append(w.get_lemma())
			tags.append(w.get_tag())
			#print(w.get_form()+" "+w.get_lemma()+" "+w.get_tag());
	#print ("");

	return words,lemmas,tags;

def analyze(text):
	tk,sp,mf,tg,sen,parser,dep = initFreeling()
	sid=sp.open_session();
	l = tk.tokenize(text);
	ls = sp.split(sid,l,True);
	ls = mf.analyze(ls);
	ls = tg.analyze(ls);
	ls = sen.analyze(ls);
	ls = parser.analyze(ls);
	ls = dep.analyze(ls);
	sp.close_session(sid);
	return ls;

## ------------  output a parse tree ------------
def getDepTree(dtree, depth):
	depT = []
	aux  = [] #save the related nodes
	node = dtree.begin()

	info = node.get_info();
	link = info.get_link();
	linfo = link.get_info();

	w = node.get_info().get_word();
	nch = node.num_children();
	
	if (nch > 0) :
		for i in range(nch) :
			d = node.nth_child_ref(i);
			if (not d.begin().get_info().is_chunk()) :
				aux.append( getDepTree(d, depth+1) );

		ch = {};
		for i in range(nch) :
			d = node.nth_child_ref(i);
			if (d.begin().get_info().is_chunk()) :
				ch[d.begin().get_info().get_chunk_ord()] = d;

		for i in sorted(ch.keys()):
			aux.append( getDepTree(ch[i], depth + 1) );
			
		depT.append((info.get_label() , (w.get_form(),w.get_position()+1) , aux ));
	else:
		depT.append((info.get_label() , (w.get_form(),w.get_position()+1) , [] ));
	
	return depT


def dependencyParser(text):
	ls= analyze(text)
	relations = [] # relations in predicates
	for s in ls:
		pred = s.get_predicates()
		for p in pred:
			posVerb = p.get_position() # predicate's main verb (nucleus in spanish)
			for a in p:
				pos = a.get_position()
				relations.append((s[posVerb].get_form(), s[pos].get_form() , a.get_role()))
				#print (s[posVerb].get_form(), s[pos].get_form() , a.get_role())
				
	for s in ls:
		dp = s.get_dep_tree()
		depTree = getDepTree(dp, 0)
		#print (depTree)
		
	return relations, depTree



