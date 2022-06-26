#include "priorityqueue.h"
#include "testing/SimpleTest.h"
#include <algorithm>
#include <queue>
#include <vector>

PROVIDED_TEST("priority queue basic", PQ) {
    std::vector<int> data {};
    PriorityQueue<int> queue {};
    for (int i = 0; i < 1000; ++i) {
        data.push_back( rand() );
        queue.push( data.back() );
    }
    EXPECT_EQUAL( queue.size(), 1000 );
    std::vector<int> sorted {};
    while ( !queue.empty() ) {
        sorted.push_back( queue.top() );
        queue.pop();
    }
    std::sort ( data.begin(), data.end(), std::greater {} );
    EXPECT( data == sorted );
}

PROVIDED_TEST("priority queue clear", PQ) {
    PriorityQueue<int> queue {};
    for (int i = 0; i < 1000; ++i) {
        queue.push( rand() );
    }
    queue.clear();
    EXPECT( queue.empty() );
}

PROVIDED_TEST("priority queue copy ctor and operator", PQ) {
    std::vector<int> data {};
    PriorityQueue<int> queue {};
    for (int i = 0; i < 1000; ++i) {
        data.push_back( rand() );
        queue.push( data.back() );
    }
    EXPECT_EQUAL( queue.size(), 1000 );
    PriorityQueue<int> copied { queue };
    PriorityQueue<int> assigned;
    assigned = queue;
    {
        std::vector<int> sorted {};
        while ( !copied.empty() ) {
            sorted.push_back( copied.top() );
            copied.pop();
        }
        std::sort ( data.begin(), data.end(), std::greater {} );
        EXPECT( data == sorted );
    }

    {
        std::vector<int> sorted {};
        while ( !assigned.empty() ) {
            sorted.push_back( assigned.top() );
            assigned.pop();
        }
        std::sort ( data.begin(), data.end(), std::greater {} );
        EXPECT( data == sorted );
    }
}
