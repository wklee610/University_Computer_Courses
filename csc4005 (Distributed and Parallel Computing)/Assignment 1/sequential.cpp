#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <time.h>



using namespace std;

const int ARR_SIZE = 20000;                     //const array

int main(int argc, char* argv[]){
    
    
    
    cout<< "NAME: Hajun Lee\n";
    cout<< "STUDENT ID: 117010437\n";
    cout<< "Assignment 1, Odd-Even Transposition Sort, Sequential Version.\n";
    
    
    
    int arr[ARR_SIZE];
    time_t start_t, end_t;
    srand(10000);
                                                //random
    for (int i = 0; i < ARR_SIZE; i++){
        arr[i]=rand();
    }

    start_t = time(NULL);                       //start timer
    
    
                                                //sort   
    for (int i = 0; i < ARR_SIZE; i++){
        for (int j = ARR_SIZE - 1; j > i; j--){
            if (arr[j] <= arr[j - 1]){
                int k = arr[j - 1];
                arr[j - 1] = arr[j];
                arr[j] = k;
            }
        }  
    }

    end_t = time(NULL);                         //end timer


    int total_t = end_t - start_t;              //find total time
    
    
 
    cout<< "Total time is : ";
    cout<<  total_t;
    cout<< "" << endl;
}