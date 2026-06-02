#include <string>
#include <iostream>
#include <vector>

using namespace std; 


void square_cube(int input) {

    cout << "Square: " << input*input;
    cout << ", Cube: " << input*input*input;
}

int main (){
    int input = 4;

    square_cube(input);

    return 0;
}