#include <string>
#include <iostream>
#include <vector>

using namespace std; 


vector<vector<int>> split_even_odd(vector<int> input) {

    int n = input.size();
    vector<vector<int>> output(2); // first is even, second is odd

    for(int i = 0; i < n; i++){
        if (input[i] % 2 == 0) {
            output[0].push_back(input[i]);
        }
        else {output[1].push_back(input[i]);}
    }

    return output;
}

int main (){
    vector<int> input = {12, 5, 8, 21, 14, 3};
    vector<vector<int>> output = split_even_odd(input);

    cout << "Even sub-array: ";
    for (int num : output[0]) {
        cout << num << " ";
    }

    cout << "\nOdd sub-array: ";
    for (int num : output[1]) {
        cout << num << " ";
    }

    return 0;
}