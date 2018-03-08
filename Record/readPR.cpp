#include <bits/stdc++.h>

using namespace std;

void read1 () { //get value per word in pagerank from corpus
fstream file ;
	string line;
	file.open("fin11.txt",ios_base::in );
	
	int ind=1,pos=-1,freq=-1,ord=-1;
	string sense="",lemma="",subj="";
	double val=-1.0;
	
	int ind1=0,pos1=0,freq1=0,ord1=0;
	string sense1="",lemma1="",subj1="";
	double val1=0.0;
	
	while (getline(file, line)){
		istringstream iss(line);
		iss>>ind1>>sense1>>lemma1>>pos1>>freq1>>ord1>>subj1>>val1;
		//if(pos1==0) continue;
		if(ind!=ind1){
			if(pos!=0 && sense!="*")
				{cout<<ind<<" "<<sense<<" "<<lemma<<" "<<pos<<" "<<freq<<" "<<ord<<" "<<subj<<" "<<val<<endl;}
			ind=-1;pos=-1;freq=-1;ord=-1;
			sense="";lemma="";subj="";
			val=-1.0;
		}
		if(pos==pos1){
			if(val<val1){
				ind=ind1;sense=sense1;lemma=lemma1;pos=pos1;
				freq=freq1;ord=ord1;subj=subj1;val=val1;
			}
		}
		else if(pos!=pos1 && pos!=-1){
			if(pos!=0 && sense!="*")
				{cout<<ind<<" "<<sense<<" "<<lemma<<" "<<pos<<" "<<freq<<" "<<ord<<" "<<subj<<" "<<val<<endl;}
			ind=ind1;sense=sense1;lemma=lemma1;pos=pos1;
			freq=freq1;ord=ord1;subj=subj1;val=val1;
		}
		else if(pos==-1){
			ind=ind1;sense=sense1;lemma=lemma1;pos=pos1;
			freq=freq1;ord=ord1;subj=subj1;val=val1;
		}
	}
	cout<<ind<<" "<<sense<<" "<<lemma<<" "<<pos<<" "<<freq<<" "<<ord<<" "<<subj<<" "<<val<<endl;
	file.close();
}

void read2 () { //get relevant info for each word of corpus
fstream file ;
	string line;
	file.open("fin12.txt",ios_base::in );
	
	int ind=1,pos=-1,freq=-1,ord=-1;
	string sense="",lemma="",subj="";
	double val=-1.0;
		
	while (getline(file, line)){
		istringstream iss(line);
		iss>>ind>>sense>>lemma>>pos>>freq>>ord>>subj>>val;
		cout<<ind<<" "<<pos<<" "<<lemma<<" "<<sense<<" "<<subj<<endl;
	}
	file.close();
}
void read3 (string filename) { //read corpus with my own labeled data 
	fstream file ;
	string line;
	file.open(filename.c_str(),ios_base::in );
	map<string,set<string> > lista;
	string a,b,c,d,e,f,g;
	while (getline(file, line)){
		istringstream iss(line);
		iss>>a>>b>>c>>d>>e>>f>>g;
		if(g!="-"){ //&& f[f.size()-1]=='n'){
			cout<<a<<" "<<c<<" "<<d<<" "<<g<<endl;
			//lista[d].insert(f);
		}		
	}
	//get lemmas with all their values in corpus
	/*
	//cout<<lista.size()<<endl;
	for(map<string,set<string> >::iterator it=lista.begin();it!=lista.end();it++){
		//int tam=(it->second).size();
		//if(tam==1)cout<<it->first<<" "<<tam;
		//cout<<it->first;
		for(set<string>::iterator it2=(it->second).begin();it2!=(it->second).end();it2++)
			//cout<<" "<<*it2;
			cout<<*it2<<endl;
		//cout<<endl;
	}
	file.close();
	*/
}


int main(){
	//read1();
	read2();
	//read3("corpusActual.txt");
	return 0;
}
	
