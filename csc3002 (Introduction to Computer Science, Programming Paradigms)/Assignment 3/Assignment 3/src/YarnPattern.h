/*
 * File: YarnPattern.h
 * ------------------
 * This program averages a set of gymnastic scores after eliminating
 * the lowest and highest scores.
 */

#ifndef _YarnPattern_h
#define _YarnPattern_h

#include <iostream>
#include "gtypes.h"
#include "gwindow.h"
#include "vector.h"
using namespace std;

/* Constants */

const int N_ACROSS = 61;          /* How many pegs horizontally */
const int N_DOWN = 41;            /* How many pegs vertically   */
const int DELTA = 77;             /* How many pegs to advance   */
const int PEG_SEP = 12;           /* Pixels separating each peg */
const int N_PEGS = 2 * N_ACROSS + 2 * N_DOWN - 4;


/*
 * Function: initPegVector
 * Usage: initPegVector(pegs);
 * ---------------------------
 * Initializes the vector of pegs by moving around the border,
 * placing pegs every PEG_SEP pixels apart.
 */

void initPegVector(Vector<GPoint> & pegs);

void showYarnPattern();

#endif
