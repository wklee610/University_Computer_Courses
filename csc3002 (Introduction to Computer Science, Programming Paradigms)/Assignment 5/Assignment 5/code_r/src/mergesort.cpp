/*
 * File: MergeSort.cpp
 * -------------------
 * This file implements the merge sort algorithm using arrays rather
 * than vectors.
 */

#include "mergesort.h"
#include <iostream>

/*
 * Function: sort
 * Usage: sort(array, n);
 * ----------------------
 * Sorts the first n elements of the array into increasing order using
 * the merge sort algorithm
 */

void sort(int array[], int n)
{
    int middle = n/2;

    if(n <= 1)
        return array;

    int array1[middle];
    int array2[n-(middle+1)];
 
    for(int i = 0; i < middle; i++)
        array1[i] = array[i];

    for(int i = middle; i < n; i++)
        array2[i - (middle+1)] = array[i];
 
    sort(array1, middle);
    sort(array2, n-(middle+1));
    merge(array, n, array1, middle, array2, n-(middle+1));
}


/*
 * Function: merge
 * Usage: merge(array, n, array1, n1, array2, n2)
 * ----------------------------
 * This function merges two sorted arrays "array1" and "array2" into the
 * array "array". The integer after the array parameter is the corresponding
 * size.
 */

void merge(int array[], int n, int array1[], int n1, int array2[], int n2)
{	
	int i, j, k;
	i = j = k = 0;
    while(i < n1 || j < n2) {
        if(array1[i] < array2[j])
            array[k++] = array1[i++];

        else
            array[k++] = array2[j++];
	}



/*
 * Function: printArray
 * Usage: printArray(array, n);
 * ----------------------------
 * Prints the elements of the array on a single line with the elements
 * enclosed in braces and separated by commas.
 */

void printArray(int array[], int n)
{
   std::cout << "{ ";
   for (int i = 0; i < n; i++)
   {
      if (i > 0) std::cout << ", ";
      std::cout << array[i];
   }
   std::cout << " }" << std::endl;
}
