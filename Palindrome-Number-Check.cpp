#include <string>
#include <iostream>
#include <vector>

using namespace std; 


string palindrome(int input) {
    string converted = to_string(input);
    int n = converted.length();
    if(n % 2 == 0){return "false";}
    for(int left = 0, right = n-1; left <= right; left++, right--){
        if(converted[left]!=converted[right]){
            return "false";
        }
    }

    return "true"; 
    
}

int main (){
    int input = 12321;

    string output = palindrome(input);

    cout << output;

    return 0;
}