/*
 * File: GymJudge.cpp
 * HAJUN LEE 117010437 Assignment 3
 * This program averages a set of gymnastic scores after eliminating
 * the lowest and highest scores.
 */

#include <iostream>
#include <iomanip>
#include <string>
#include "error.h"
#include "simpio.h"
#include "strlib.h"
#include "GymnasticsJudge.h"

using namespace std;

/*
 * Function: sumArray
 * Usage: double sum = sumArray(array, n);
 * ---------------------------------------
 * This function returns the sum of the first n elements in array.
 */

double sumArray(double array[], int n) {
    double s = 0;
	int i = 0;

	while (i < n) {
		s += array[i];
		i += 1;
	}

    return s;
}

/*
 * Function: findLargest
 * Usage: double largest = findLargest(array, n);
 * ----------------------------------------------
 * This function returns the largest value in the first n elements in array.
 */

double findLargest(double array[], int n) {
    double l = array[0];
	int i = 0;

	while (i < n) {
		if (array[i] > l) {
            l = array[i];
		}

        i += 1;
	}

    return l;
}

/*
 * Function: findSmallest
 * Usage: double smallest = findSmallest(array, n);
 * ------------------------------------------------
 * This function returns the smallest value in the first n elements in array.
 */

double findSmallest(double array[], int n) {
    double s = array[0];
	int i = 0;

	while (i < n) {
		if (array[i] < s) {
            s = array[i];
		}

        i += 1;
	}

    return s;
}

/*
 * Function: readScores
 * Usage: int nJudges = readScores(scores, max);
 * ---------------------------------------------
 * This function reads in scores for each of the judges.  The array
 * scores must be declared by the caller and must have an allocated
 * size of max.  The return value is the number of scores.  From the
 * user's perspective, the numbering of the judges begins with 1
 * because that style of numbering is more familiar; internally,
 * the array index values begin with 0.
 */

int readScores(double scores[], int max) {
    cout << "Enter score for each judge in the range 0 to 10" << endl;
	cout << "Enter a blank line to signal the end of the list" << endl;
    int nJudges = 0;

    while (nJudges <= max) {
        cout <<"Judge #" << nJudges + 1 << ": ";
        string str;
        getline(cin, str);

        if (str == "") {
            break;
        }
		 
        double score = atof(str.c_str());
        scores[nJudges] = score;
        nJudges += 1;
    }

    return nJudges;
}
