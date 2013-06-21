#include <string.h>
#include <stdlib.h>
#include <file.h>
typedef struct{
	int index;
	int value;
	int weight;
	double estimate;
	int isSelected;
	} State;
	
typedef State *PState;

typedef struct{
	double Ratio;
	int Index;
	} RatioIndex;

void solve(int argc, char** argv){
	int i;
	char* filename;
	for(i = 0; i < argc; i++){
		if(strstr(argc[i], "-file=") != null){
			filename = argc[i][6];
			}
		}
	
	
	
	}

int main(int argc, char** argv){
	solve(argc, argv);
	
	}	
