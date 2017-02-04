import sys
from Freeling import freeling;

def procText (text):
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
	sid=sp.open_session();
	mf=freeling.maco(op);

	# activate mmorpho odules to be used in next call
	mf.set_active_options(False, True, True, True,  # select which among created 
                      	  True, True, False, True,  # submodules are to be used. 
						  True, True, True, True ); # default: all created submodules are used
	
	# create tagger, sense anotator, and parsers
	tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
	sen=freeling.senses(DATA+LANG+"/senses.dat");
	
	l = tk.tokenize(text);
	ls = sp.split(sid,l,True);
	ls = mf.analyze(ls);
	ls = tg.analyze(ls);
	ls = sen.analyze(ls);

	for s in ls :
		ws = s.get_words();
		for w in ws :
			print(w.get_form()+" "+w.get_lemma()+" "+w.get_tag());
	print ("");

	sp.close_session(sid);


procText("Vería esa película una_y_otra_vez")



