/*
 * File: YarnPattern.cpp
 * HAJUN LEE 117010437 Assignment 3
 * This program illustrates the use of the GPoint class to simulate
 * winding a piece of colored yarn around a set of pegs equally
 * spaced along the edges of the canvas.  At each step, the yarn is
 * stretched from its current peg to the one DELTA pegs further on.
 */

#include <iostream>
#include "gtypes.h"
#include "gwindow.h"
#include "vector.h"
#include "YarnPattern.h"
using namespace std;


/*
 * Function: initPegVector
 * Usage: initPegVector(pegs);
 * ---------------------------
 * Initializes the vector of pegs by moving around the border,
 * placing pegs every PEG_SEP pixels apart.
 */

void initPegVector(Vector<GPoint> & pegs) {

    long i = PEG_SEP;
    long j = 0;

    for (int k = 1; k <= N_ACROSS; k++) {

        i += PEG_SEP;
        pegs.add(GPoint(i,j));
        continue;
    }

    for (int k = 2; k <= N_DOWN; k++) {

        j += PEG_SEP;
        pegs.add(GPoint(i,j));
        continue;
    }

    for (int k = 2; k <= N_ACROSS; k++) {

        i -= PEG_SEP;
        pegs.add(GPoint(i,j));
        continue;

    }

    for (long k = 1; k <= N_DOWN; k++) {

        j -= PEG_SEP;
        pegs.add(GPoint(i,j));
        continue;
    }
}



/*
 * Function: ShowYarnPattern
 * Usage: ShowYarnPattern();
 * ---------------------------
 * Show the Yarn Pattern window accordding to initPegVector.
 */

void showYarnPattern(){
    GWindow gw((N_ACROSS) * PEG_SEP, (N_DOWN) * PEG_SEP);
    Vector<GPoint> pegs;
    initPegVector(pegs);
    int thisPeg = 0;
    int nextPeg = -1;
    gw.setColor("BLUE");
    gw.show();

    while (nextPeg != 0) {
        nextPeg = thisPeg + DELTA;

        if (nextPeg >= N_PEGS) {
            nextPeg -= N_PEGS;
        }

        gw.drawLine(pegs[nextPeg], pegs[thisPeg]);
        thisPeg = nextPeg;
    }
}
