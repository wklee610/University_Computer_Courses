//
//  main.cpp
//  dijkstra
//
//  Created by Hajun Lee on 2020/12/22.
//  Copyright © 2020 Hajun Lee. All rights reserved.
//
#include<iostream>
#include <cstdio>
#include <queue>
#define MAX_VALUE 99999999

using namespace std;

int N, M, s;

class Vertex {
public:
    int index;
    int dist;
    int post = 0;
    
    Vertex(int index, int dist, int post) : index(index), dist(dist), post(post)
    {
        
    };
    Vertex(int index) : index(index)
    {
        dist = MAX_VALUE;
    }
    
    void setDist(int d) {
        dist = d;
    };
    bool operator >(const Vertex& v) const
    {
        return dist > v.dist;
    }
    bool operator < (const Vertex& v)
    {
        return dist < v.dist;
    }
};
