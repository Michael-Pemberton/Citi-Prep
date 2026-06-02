#include <string>
#include <iostream>
#include <vector>

using namespace std; 


int factors(int input, int f) {
    int count = 0;
    int n = input;
    while (f<=n){
        if(n % f == 0){
            n /= f;
            count++;
        }
        else{
            return count;
        }
    }
    return count;
    
}

int main (){
    int input = 24;
    int f = 2;
    int output = factors(input, f);

    cout << output;

    return 0;
}