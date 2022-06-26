
#include <iostream>
#include <string>
#include <vector>
#include "banishLetters.h"
using namespace std;

/*
 * Please add detailed function description
 *
 */
void banishLetters(string str, istream& is, ostream& os) {
 string s;
 vector<char> vec;

 for (int i = 0; i < str.size(); i++)
  vec.push_back(str[i]);

 while (getline(is, s)) {
  for (char& elem : vec) {
   while (s.find(elem, 0) != string::npos) {
    s.erase(s.find(elem, 0), 1);
   }
   char elem2;
   if (elem >= 'A' && elem <= 'Z')
    elem2 = elem + 32;
   else if (elem >= 'a' && elem <= 'z')
    elem2 = elem - 32;
   else
    continue;
   while (s.find(elem2, 0) != string::npos) {
    s.erase(s.find(elem2, 0), 1);
   }
  }
  os << s << endl;
 }
}
