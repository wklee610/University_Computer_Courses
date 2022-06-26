/*
 * File: mergesort.h
 * --------------
 * This file defines the related prototypes about in merge sort algorithm.
 */

#ifndef _mergesort_h
#define _mergesort_h

/* Function prototypes */

void sort(int array[], int n);
void merge(int array[], int n, int array1[], int n1, int array2[], int n2);
void printArray(int array[], int n);

#endif
