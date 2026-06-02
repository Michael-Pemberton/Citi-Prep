#include <string>
#include <iostream>

using namespace std; 


string even_or_odd(int number) {
    if(number % 2 == 0){
        return "even";
    }
    else return "odd";
}

int main (){
    int number = 2;
    cout << even_or_odd(number);
    return 0;
}