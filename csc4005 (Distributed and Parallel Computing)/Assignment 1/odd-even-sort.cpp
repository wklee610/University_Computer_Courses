#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <iostream>
#include <mpi.h>
#include <stdint.h>
#include <algorithm>
#include <vector>


using namespace std;


int comp_Odd(int *arr, int size){

	int sort_Odd = 1;                                           // odd sort

	for (int j = 0; j < size - 1; j += 2){
		if (arr[j] > arr[j + 1]) {
			int flip = arr[j];
			arr[j] = arr[j + 1];
			arr[j + 1] = flip;
			sort_Odd = 0;
		}
	}

	return sort_Odd;
}

int comp_Even(int *arr, int size){

	int sort_Even = 1;                                          // even sort

	for (int j = 1; j < size - 1; j += 2){
		if (arr[j] > arr[j + 1]) {
			int flip = arr[j];
			arr[j] = arr[j + 1];
			arr[j + 1] = flip;
			sort_Even = 0;
		}
	}

	return sort_Even;
}

int comp_Bound(int rank, int *arr, int size, int comp_Size){
	int num;
	int code = 1;
	
	if (rank == 0){
		MPI_Recv(&num, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		if (num < arr[size - 1]) {
			swap(num, arr[size - 1]);
			code = 0;
		}
		
        MPI_Send(&num, 1, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
	}
	
    else if (rank == comp_Size - 1){
		MPI_Send(&arr[0], 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD);
		MPI_Recv(&arr[0], 1, MPI_INT, rank - 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
	}
	
    else{

		MPI_Send(&arr[0], 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD);
		MPI_Recv(&num, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		if (num < arr[size - 1]){
			swap(num, arr[size - 1]);
			code = 0;
		}
		MPI_Send(&num, 1, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
		MPI_Recv(&arr[0], 1, MPI_INT, rank - 1, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
	}
	
    return code;
}


void doSortParallel(int *arr, int size){

	int sort_Odd = 0;
	int sort_Even = 0;
	int rank = -1;
	int comp_Size = 0;	
    int comp_bound_code = 0;
    
	
    
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &comp_Size);
	

	while (true){

		sort_Odd = comp_Odd(arr, size);

		if (size % 2 != 0 && comp_Size != 1){
			comp_bound_code = comp_Bound(rank, arr, size, comp_Size);
		}

		sort_Even = comp_Even(arr, size);

		if (size % 2 == 0 && comp_Size != 1){
			comp_bound_code = comp_Bound(rank, arr, size, comp_Size);
		}

		int code = sort_Odd + sort_Even + comp_bound_code;
		int result;

		MPI_Allreduce((void *) & code, (void *) & result, 1, MPI_INT, MPI_MIN, MPI_COMM_WORLD);

		if (result == 3){
			break;
		}
	}

	return;
}



int main(int argc, char *argv[]){


	int comp_Size, comp_Rank, partner;
	double T_process, T_sort;

	
    // def const
	const int ARRAY_SIZE = 20;
	const int MAX_VALUE = 100;
	int temp_size = ARRAY_SIZE;
	
	
    
    // init mpi
    MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &comp_Size);
	MPI_Comm_rank(MPI_COMM_WORLD, &comp_Rank);

	if (ARRAY_SIZE % comp_Size != 0){
		temp_size += (comp_Size - (ARRAY_SIZE % comp_Size));
	}

	const int ARRAY_TEMP_SIZE = const_cast<const int&>(temp_size);

	int size = ARRAY_TEMP_SIZE / comp_Size;
	int *sourceArray;




	// init array
	if (comp_Rank == 0){

    
		srand(time(NULL));
		sourceArray = new int[ARRAY_TEMP_SIZE];

		for (int i = 0; i < ARRAY_SIZE; i += 1){
			sourceArray[i] = rand() % MAX_VALUE;
		}

		if (ARRAY_TEMP_SIZE != ARRAY_SIZE){
			for (int i = ARRAY_SIZE; i < ARRAY_TEMP_SIZE; i += 1){
				sourceArray[i] = MAX_VALUE;
			}
		}

		for (int i = 0; i < ARRAY_SIZE; i++){
			cout << sourceArray[i] << " ";
		}

		cout << endl;

	}
	
    
    //start
    T_process = MPI_Wtime();
    
    int *data = new int[size];

	MPI_Scatter(sourceArray, size, MPI_INT, data, size, MPI_INT, 0, MPI_COMM_WORLD);
    doSortParallel(data, size);
    MPI_Gather(data, size, MPI_INT, sourceArray, size, MPI_INT, 0, MPI_COMM_WORLD);
    
    T_process = MPI_Wtime() - T_process;
	
    MPI_Reduce((void *) & T_process, (void *)&T_sort, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    
    //end
	
    if (comp_Rank == 0){
		
		cout<< "NAME: Hajun Lee\n";
    	cout<< "STUDENT ID: 117010437\n";
    	cout<< "Assignment 1, Odd-Even Transposition Sort, MPI Version.\n";

        printf("Total time: %f s\n", T_sort * 1000);
		
        for (int i = 0; i < ARRAY_SIZE; i++){
			cout << sourceArray[i] << " ";
		}

		cout << "" << endl;

	}

	delete[] data;

	if (comp_Rank == 0){
		delete[] sourceArray;
	}

	MPI_Finalize();
	
	return 0;

}
