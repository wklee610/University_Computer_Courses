#include <iostream>
#include <string>
#include <cctype>
#include <cassert>

#include "foreach.h"
#include "simpio.h"
#include "console.h"
#include "strlib.h"

#include "mergesort.h"
#include "buffer.h"
#include "pqueue.h"
#include "bigint.h"

/* Function prototypes */

void TestQ1();
void TestQ2();
void TestQ3();
void TestQ4();

/* Main program */

int main()
{
    TestQ1();
    TestQ2();
    TestQ3();
    TestQ4();
    return 0;
}


/* Simple test of Q1
 * Expected output: { 23, 34, 43, 56}
 *                  { 19, 25, 30, 37, 56, 58, 73, 95 }
 */

void TestQ1()
{
    int array1[] = {34, 43};
    int array2[] = {23, 56};
    int array3[] = {1,2,3,4};
    merge(array3, 4, array1, 2, array2, 2);
    printArray(array3, 4);

    int array[] = { 56, 25, 37, 58, 95, 19, 73, 30 };
    sort(array, 8);
    printArray(array, 8);
}


/* Simple test of Q2 */

void TestQ2()
{
    EditorBuffer buffer;
    while (true)
    {
       std::string cmd = getLine("*");
       if (cmd != "") executeCommand(buffer, cmd);
    }
}


/* Simple test of Q3 */

void TestQ3()
{
    PriorityQueue<std::string> pq;
    assert(pq.size() == 0);
    assert(pq.isEmpty());
    pq.enqueue("A", 1);
    assert(!pq.isEmpty());
    assert(pq.peek() == "A");
    assert(pq.dequeue() == "A");
    assert(pq.isEmpty());
    std::cout << "Priority queue test succeeded" << std::endl;
}


/* Simple test of Q4
 * Expected output: 25! = 15511210043330985984000000
 *                  25 + 4 = 29
 */

void TestQ4()
{
    std::cout << 25 << "! = " << fact(25).toString() << std::endl;
    auto a = BigInt(25);
    auto b = BigInt("4");
    std::cout << "25 + 4 = " << (a+b).toString() << std::endl;
}


