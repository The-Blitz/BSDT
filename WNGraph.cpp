#include <bits/stdc++.h>

using namespace std;

map< string , map <string ,int >  > graph;

map< string , map <string ,int >  >  read () {
	map< string , map <string ,int >  >   aux;
	fstream file ;
	string line;
	file.open("WordNetEdges/ili-wnet30g_rels.txt",ios_base::in );
	while (getline(file, line)){
		string u,v;
		istringstream iss(line);
		iss>>u>>v;
		u= "spa" + u.substr(5);
		v= "spa" + v.substr(5);
		aux[u][v]=1;
		aux[v][u]=1;
	}
	file.close();
	
	
	file.open("WordNetEdges/ili-wnet30_rels.txt", ios_base::in );
	
	while (getline(file, line)){
		string u,v;
		istringstream iss(line);
		iss>>u>>v;
		u= "spa" + u.substr(5);
		v= "spa" + v.substr(5);
		aux[u][v]=1;
		aux[v][u]=1;
	}
	
	file.close();
	
	return aux;
}

map<string,int> dijkstra(map< string , map <string ,int >  >  graph , string start){
	set< pair<int , string> > q;
	map<string , int > distances;
	for (map< string , map <string ,int >  >::iterator it1=graph.begin(); it1!=graph.end();it1++){
		distances[it1->first] = 9999999;
	}
	distances[start] = 0;
	q.insert(make_pair(0,start));
	
	while(!q.empty()){
		pair<int,string> top = *q.begin();
		string v= top.second;	int d = top.first;
		q.erase(q.begin());
		for (map <string ,int >::iterator it2=(graph[v]).begin(); it2!=(graph[v]).end();it2++){
			string w = it2->first ; int cost = it2->second;
			if(distances[w] > distances[v] + cost){
				if(distances[w] != 9999999){
					q.erase(q.find(make_pair(distances[w], w)));
				}
				distances[w] = distances[v] + cost;
				q.insert(make_pair(distances[w], w));
			}
		} 
	}
	return distances;
}

int main (int argc, char *argv[]) {
	int cont=1;
	int lim1 =atoi(argv[1]);
	int lim2 =atoi(argv[2]);
	map< string , map <string ,int >  >   graph = read();
	for (map< string , map <string ,int >  >::iterator it1=graph.begin(); it1!=graph.end();it1++){
		cont++;
		if(cont<lim1) continue;
		if(cont>lim2) break;
		cout<<it1->first<<endl;
		map <string ,int >  aux = dijkstra (graph, it1->first);
		fstream file ;
		string filename= "Distances/"+it1->first+".txt";
		file.open(filename.c_str(),ios_base::out);	
		for (map <string ,int >::iterator it2=aux.begin(); it2!=aux.end();it2++){
			file<<it2->first <<" "<<it2->second<<endl;
		}
		file.close();
	}
	return 0;
}
