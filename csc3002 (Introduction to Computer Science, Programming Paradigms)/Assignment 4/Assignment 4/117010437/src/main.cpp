#include <iostream>
#include <console.h>
#include <iomanip>
#include "testing/SimpleTest.h"
#include <gwindow.h>
#include "hfractal.h"
using namespace std;


int main() {
    if (runSimpleTests(SELECTED_TESTS)) {
            return 0;
    }
    return 1;
}






