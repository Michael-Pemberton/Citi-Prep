#include <string>
#include <iostream>
#include <vector>

using namespace std; 


string prime_number(int input) {
    int left = 2;
    int right = input;
    if (input <= 2){return "not prime";}
    while (left<=right){
        if(input % left == 0){
            cout << left << "\n";
            cout << input/left << "\n"; 
            return "not prime";
        }
        else{
            left += 1;
            right = input/left+1;
        }
    }
    return "Prime";
    
}

int main (){
    int input = 10597;
    string output = prime_number(input);

    cout << output;

    return 0;
}