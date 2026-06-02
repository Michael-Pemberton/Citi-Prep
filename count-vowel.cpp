#include <string>
#include <iostream>
#include <vector>

using namespace std; 


int count_vowel(string input) {
    int n = input.length();
    string vowels = "aeiou";
    int count = 0;
    for(int i = 0; i<n; i++){
        if(vowels.find(tolower(input[i]))!=string::npos){
            count++;
        }
    }
    return count;

}

int main (){
    string input = "CodingExercise";

    int output = count_vowel(input);

    cout<<output;

    return 0;
}