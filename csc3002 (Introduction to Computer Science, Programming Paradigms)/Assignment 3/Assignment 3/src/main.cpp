#include <iostream>
#include <console.h>
#include <iomanip>
#include "GymnasticsJudge.h"
#include "YarnPattern.h"
using namespace std;


/* Main program */

int main() {
   cout << "Begin testing Question 1: remove comments------" << endl;

   showYarnPattern();

   cout << "End testing Question 1: remove comments------" << endl;

   cout << "Begin testing Question 2: remove comments------" << endl;

   double scores[MAX_JUDGES];
   int nJudges = readScores(scores, MAX_JUDGES);
   if (nJudges < 3) {
      cout << "You must enter scores for at least three judges." << endl;
   } else {
      double total = sumArray(scores, nJudges);
      double smallest = findSmallest(scores, nJudges);
      double largest = findLargest(scores, nJudges);
      double average = (total - smallest - largest) / (nJudges - 2);
      cout << "The average after eliminating "
           << fixed << setprecision(2) << smallest << " and "
           << setprecision(2) << largest << " is "
           << setprecision(2) << average << "." << endl;
   }

   cout << "End testing Question 2: remove comments------" << endl;

   return 0;
}









