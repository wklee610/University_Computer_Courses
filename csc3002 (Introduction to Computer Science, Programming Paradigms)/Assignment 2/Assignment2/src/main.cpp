#include <iostream>
#include <console.h>
//#include "test.h"
#include <iomanip>
#include <fstream>
#include "strlib.h"
#include "simpio.h"
#include "filelib.h"     // promptUserForFile
#include "removeComments.h"
#include "banishLetters.h"
#include "sieveOfEratosthenes.h"
#include "reverseQueue.h"

using namespace std;


int main() {
    /*
     * Test Question 1: remove comments
     */
    cout << "Begin testing Question 1: remove comments------" << endl;
    ifstream infile1;
    promptUserForFile(infile1, "Input file: ");
    removeComments(infile1, cout);
    infile1.close();
    cout << "End testing Question 1: remove comments------" << endl;

    /*
     * Test Question 2: banish letters
     */
    cout << "Begin testing Question 2: remove comments------" << endl;
    ifstream infile2;
    ofstream outfile;
    promptUserForFile(infile2, "Input file: ");
    promptUserForFile(outfile, "Output file: ");
    string banish = getLine("Letters to banish: ");
    banishLetters(banish, infile2, outfile);
    infile2.close();
    outfile.close();
    cout << "End testing Question 2: remove comments------" << endl;

    /*
     * Test Question 3: sieve of eratosthenes
     */
    cout << "Begin testing Question 3: sieve of eratosthenes------" << endl;
    const int MAX_VALUE = 1000;
    Vector<bool> isPrime(MAX_VALUE + 1);
    sieveOfEratosthenes(isPrime);
    for (int i = 0; i <= MAX_VALUE; i++) {
       if (isPrime[i])
           cout << i << endl;
    }
    cout << "End testing Question 3: sieve of eratosthenes------" << endl;

    /*
     * Test Question 4: reverse queue
     */
    cout << "Begin testing Question 3: sieve of eratosthenes------" << endl;
    Queue<string> queue;
    queue.enqueue("Genesis");
    queue.enqueue("Exodus");
    queue.enqueue("Leviticus");
    queue.enqueue("Numbers");
    queue.enqueue("Deuteronomy");
    listQueue(queue);
    reverseQueue(queue);
    listQueue(queue);
    cout << "End testing Question 3: sieve of eratosthenes------" << endl;
    return 0;
}


