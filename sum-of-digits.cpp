#include <string>
#include <iostream>
#include <vector>

using namespace std; 


int sum_of_digits(int input) {
    int sum = 0;

    while(input>0){
        sum += input % 10;
        input /= 10;
    }
    return sum;
}

int main (){
    int input = 242210;

    int output = sum_of_digits(input);

    cout << output;

    return 0;
}