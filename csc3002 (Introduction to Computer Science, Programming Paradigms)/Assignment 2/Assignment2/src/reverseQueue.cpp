
#include <iostream>
#include "reverseQueue.h"
#include "stack.h"
using namespace std;

/*
 * Please add detailed function description
 */

void reverseQueue(Queue<string> & queue) {
    string str1 = queue.front();
    string str2 = queue.back();
    while (queue.front() != str2) {
        queue.enqueue(queue.front());
        queue.dequeue();
    }
}

/*
 * Please add detailed function description
 */
void listQueue(Queue<string> & queue) {
    Vector<string> vec;
    while(!queue.isEmpty()){
        cout << queue.front() << endl;
        vec.push_back(queue.front());
        queue.dequeue();
    }
    for(string elem:vec)
        queue.enqueue(elem);
}
