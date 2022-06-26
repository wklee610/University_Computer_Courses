//
//  main.cpp
//  huffman
//
//  Created by Hajun Lee on 2020/12/22.
//  Copyright © 2020 Hajun Lee. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <iostream>
#define MAX_TREE_HT 256

char dict[258][258] = {0};

//정의하기 Letter = 글자 / child = 트리 자식수 / frqy = frequency
struct HuffmanNode {
    char Letter;
    char child;
    long unsigned frqy;
    
    struct HuffmanNode *left, *right;
    
};

struct MinHeap {
    long unsigned size;
    long unsigned capacity;
    struct HuffmanNode** array;
};

struct HuffmanNode* newNode(char Letter, long unsigned frqy)
{
    struct HuffmanNode* temp
        =(struct HuffmanNode*)malloc(sizeof(struct HuffmanNode));
    temp->left = temp->right = NULL;
    temp->Letter = Letter;
    temp->frqy = frqy;
    temp->child = Letter;
    return temp;
}

struct MinHeap* makeMinHeap(long unsigned capacity)
{
    struct MinHeap* minHeap
        = (struct MinHeap*)malloc(sizeof(struct MinHeap));
    minHeap->size = 0;
    minHeap->capacity = capacity;
    minHeap->array
        = (struct HuffmanNode**)malloc(minHeap->capacity * sizeof(struct HuffmanNode*));
    return minHeap;
}

void swapHuffmanNode(struct HuffmanNode** a,
    struct HuffmanNode** b)
{
    struct HuffmanNode* t = *a;
    *a = *b;
    *b = t;
}

void minHeapify(struct MinHeap* minHeap, int idx)

{

    int minimum = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < minHeap->size && (minHeap->array[left]->
        frqy < minHeap->array[minimum]->frqy || (minHeap->array[left]->
        frqy == minHeap->array[minimum]->frqy && minHeap->array[left]->
        child < minHeap->array[minimum]->child)))
            minimum = left;

    if (right < minHeap->size && (minHeap->array[right]->
        frqy < minHeap->array[minimum]->frqy || (minHeap->array[right]->
        frqy == minHeap->array[minimum]->frqy && minHeap->array[right]->
        child < minHeap->array[minimum]->child)))
            minimum = right;

    if (minimum != idx) {
        swapHuffmanNode(&minHeap->array[minimum],
                        &minHeap->array[idx]);
        minHeapify(minHeap, minimum);
    }
}

int isSizeOne(struct MinHeap* minHeap)
{

    return (minHeap->size == 1);
}

struct HuffmanNode* extractMin(struct MinHeap* minHeap)

{
    struct HuffmanNode* temp = minHeap->array[0];
    minHeap->array[0]
        = minHeap->array[minHeap->size - 1];

    --minHeap->size;
    minHeapify(minHeap, 0);

    return temp;
}

void putMinHeap(struct MinHeap* minHeap,
                struct HuffmanNode* HuffmanNode)

{
    ++minHeap->size;
    int i = minHeap->size - 1;

    while (i && (HuffmanNode->frqy < minHeap->array[(i - 1) / 2]->frqy || (HuffmanNode->frqy == minHeap->array[(i - 1) / 2]->frqy && HuffmanNode->child < minHeap->array[(i - 1) / 2]->child))) {

        minHeap->array[i] = minHeap->array[(i - 1) / 2];
        i = (i - 1) / 2;
    }
    minHeap->array[i] = HuffmanNode;
}

void runMinHeap(struct MinHeap* minHeap)
{
    int n = minHeap->size - 1;
    int i;

    for (i = (n - 1) / 2; i >= 0; --i)
        minHeapify(minHeap, i);
}

void printArr(int arr[], int n)
{
    int i;
    for (i = 0; i < n; ++i)
        printf("%d", arr[i]);
}

int Leaf(struct HuffmanNode* root)

{
    return !(root->left) && !(root->right);
}

struct MinHeap* makeAndrunMinHeap(char Letter[], int frqy[], int size)

{
    struct MinHeap* minHeap = makeMinHeap(size);

    for (int i = 0; i < size; ++i)
        minHeap->array[i] = newNode(Letter[i], frqy[i]);
    minHeap->size = size;
    runMinHeap(minHeap);

    return minHeap;
}

struct HuffmanNode* runHuffmanTree(char Letter[], int frqy[], int size)

{
    struct HuffmanNode *left, *right, *top;
    struct MinHeap* minHeap = makeAndrunMinHeap(Letter, frqy, size);

    while (!isSizeOne(minHeap)) {

        left = extractMin(minHeap);
        right = extractMin(minHeap);
        top = newNode('$', left->frqy + right->frqy);

        top->left = left;
        top->right = right;
        top->child = left->child;

        putMinHeap(minHeap, top);
    }
    return extractMin(minHeap);
}

void printCodes(struct HuffmanNode* root, char arr[], int top)
{
    if (root->left) {
        arr[top] = '0';
        printCodes(root->left, arr, top + 1);
    }
    if (root->right) {
        arr[top] = '1';
        printCodes(root->right, arr, top + 1);
    }
    if (Leaf(root)) {
        memcpy(dict[(int)root->Letter], arr, top);
    }
}

void HuffmanCodes(char Letter[], int frqy[], int size)
{
    struct HuffmanNode* root
        = runHuffmanTree(Letter, frqy, size);

    char arr[MAX_TREE_HT];
    int top = 0;

    printCodes(root, arr, top);
}





int main()
{

    char arr[258];
    int frqy[258];
    
   char s[100010]="";
   char c;
   int len = 0;
   while (true) {
    c = getchar();
    if (c == EOF || c == '\n' || c == '\0' || c == '\r') {
        break;
    }
    s[len++] = c;
   }
   
   int size = 0;
   for (int i = 0; i < len; i ++) {
   int idx = -1;
    for (int j = 0; j < size; j ++) {
        if (arr[j] == s[i]) {
            idx = j;
            break;
        }
    }
    if (idx == -1) {
        arr[size] = s[i];
        frqy[size] = 0;
        idx = size ++;
    }
    frqy[idx] ++;
   }

    HuffmanCodes(arr, frqy, size);

    for (int i = 0; i <len; i++) {
        std::cout << dict[(int)s[i]];
    }
    std::cout << std::endl;
    return 0;
}
