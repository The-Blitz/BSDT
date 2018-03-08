#include <bits/stdc++.h>

using namespace std;

vector<pair<string, string> > read (string filename) {
	vector<pair<string, string> > res;
	fstream file ;
	string line;
	file.open(filename.c_str(),ios_base::in );
	
	string ind,pos,lemma,offset,subj;
	
	while (getline(file, line)){
		istringstream iss(line);
		iss>>ind>>pos>>lemma>>offset>>subj;
		//res.push_back(make_pair((ind+" "+lemma+" "+pos),subj));
		string aux="";
		aux = aux + char(offset[offset.size()-1] - 32)+"-"+ subj;
		res.push_back(make_pair((ind+" "+lemma+"-"+pos), aux ));
	}
	file.close();
	return res;
}

void readDiff(string filename){
	fstream file ;
	string line;
	file.open(filename.c_str(),ios_base::in );
	string ind1,lemma1,pos1,subj1,ind2,lemma2,pos2,subj2;
	map<string,int>diffDict;
		while (getline(file, line)){
		istringstream iss(line);
		iss>>ind1>>lemma1>>pos1>>subj1>>ind2>>lemma2>>pos2>>subj2;
		diffDict[lemma1]++; 
	}
	vector< pair<int,string> > diff;
	for(map<string,int >::iterator it=diffDict.begin();it!=diffDict.end();it++){
		diff.push_back(make_pair(it->second , it->first));
	}
	
	sort(diff.begin(),diff.end());
	reverse(diff.begin(),diff.end());
	for(int i=0; i<10;i++){
		cout<<diff[i].second<<" "<<diff[i].first<<"\n";
	}
	file.close();
	
}

void readRela(string filename){
	vector<pair<string, string> > vect1 = read("result-A.txt");
	map<string,string> cont;
	
	for(int i=0; i<vect1.size();i++){
		cont[vect1[i].first]=vect1[i].second;
	}
	fstream file ;
	string line;
	file.open(filename.c_str(),ios_base::in );
	string ind,lemma1,lemma2,feat1, feat2;
	while (getline(file, line)){
		istringstream iss(line);
		iss>>ind>>lemma1>>lemma2>>feat1>>feat2;
		string aux1 = ind+" "+lemma1;
		string aux2 = ind+" "+lemma2;
		if(cont.count(aux1) and cont.count(aux2)){
			cout<<ind<<" "<<lemma1<<" "<<lemma2<<" "<<cont[aux1]<<" "<<cont[aux2]<<"\n";
		}
	}
	file.close();
}

int main(){
	/*
	vector<pair<string, string> > vect1 = read("result-A.txt");
	vector<pair<string, string> > vect2 = read("result-J.txt");
	vector<pair<string, string> > vect3 = read("result-S.txt");	
	int cont=0;

	int equal=0;
	int found=0;
	*/
	// compare data with right values ( juntos.txt vs anotacion.txt)
	
	/*for(int i=0; i<vect2.size();i++){
		string s1=vect2[i].first; string s2=vect2[i].second;
		int cont1=cont;
		while(cont1<vect1.size()){
			string s3=vect1[cont1].first; string s4=vect1[cont1].second;
			cont1++;
			if(s3==s1){
				found++;
				if(s2==s4)equal++;
				else{
					cout<<s1<<" "<<s2<<" "<<s3<<" "<<s4<<"\n";
				}	
				break;
			}
		}
		if(cont1<vect1.size())	cont=cont1;
	}*/
	
	// compare data with right values ( separados.txt vs anotacion.txt)
	
	/*for(int i=0; i<vect3.size();i++){
		string s1=vect3[i].first; string s2=vect3[i].second;
		int cont1=cont;
		while(cont1<vect1.size()){
			string s3=vect1[cont1].first; string s4=vect1[cont1].second;
			cont1++;
			if(s3==s1){
				found++;
				if(s2==s4)equal++;
				else{
					cout<<s1<<" "<<s2<<" "<<s3<<" "<<s4<<"\n";
				}		
				break;
			}
		}
		if(cont1<vect1.size())	cont=cont1;
	}*/		
	
	//cout<<found<<" "<<equal<<endl;
	
	//readDiff("diffSA.txt");
	
	readRela("relations3.txt");
	return 0;
}
	
