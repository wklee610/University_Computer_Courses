#include <iostream>
#include <console.h>
#include <iomanip>
#include "testing/SimpleTest.h"
using namespace std;


int main() {
    srand(1999'12'08);
    if (runSimpleTests(SELECTED_TESTS)) {
            return 0;
    }
    return 1;
}






