#include <iostream>
#include <string>
#include "removeComments.h"
using namespace std;

/*
 * Please add detailed function description
 *
 */
void removeComments(istream& is, ostream& os) {
    string s;
    while (true) {
        is >> s;
        if (!is)
            break;
        else {
            if (s == "/*") {
                do {
                    if (!is)
                        break;
                    is >> s;
                } while (s != "*/");
            }
            else if (s == "//")
                getline(is, s);
            else {
                os << s;
                getline(is, s);
                os << s << endl;
            }
        }
    }
}
