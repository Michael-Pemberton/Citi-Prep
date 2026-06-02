#include <string>
#include <iostream>
#include <vector>

using namespace std; 


void max_min(int input[]) {
    int max = input[0];
    int min = input[0];
    int n = sizeof(input);
    for(int i = 1; i<n; i++){
        if(input[i]>max){
            max = input[i];
        }
        if(input[i]<min){
            min = input[i];
        }
    }
    cout<<"Maximum: "<< max << ", Minimum: "<<min;

}

int main (){
    int input[] = {7, 2, 10, -1, 5};

    max_min(input);

    return 0;
}