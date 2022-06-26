/*
 * This is a driver to test pass1 and the Label Table functions.
 *
 * Author: Alyce Brady
 * Date: 2/18/99
 * Modified by: Caitlin Braun and Giancarlo Anemone to test pass2 of the assembler.
 */

#include <stdio.h>
#include <string.h> 
#include "LabelTable.h"

LabelTable pass1 (char * filename);
LabelTable pass2 (char * filename, LabelTable table);


int compare_files(FILE* fp1, FILE* fp2)
{
	char char1 = fgetc(fp1);
	char char2 = fgetc(fp2);

	while(char1 != EOF && char2 != EOF){
		if(char1 != char2){
			return -1;
		}
        char1 = fgetc(fp1);
        char2 = fgetc(fp2);
	}
	return 0;
}
int main (int argc, char * argv[])
{   
    if(argc < 4)
    {
        printf("Please enter an input file, an output file, and expected output file \n");
    }
    LabelTable table;
    table = pass1(argv[1]);
    (void)pass2(argv[1], table);

    FILE* fp1;
    FILE* fp2;
    fp1 = fopen(argv[3], "r");
    fp2 = fopen(argv[2], "r");

    if(fp1 == NULL || fp2 == NULL){
    	printf("Error: Files are not open correctly \n");
    }

    int res = compare_files(fp1, fp2);

    if(res == 0){
    	printf("ALL PASSED! CONGRATS :) \n");
    }else{
    	printf("YOU DID SOMETHING WRONG :( \n");
    }

    fclose(fp1);
    fclose(fp2);
    
    return 0;
}


