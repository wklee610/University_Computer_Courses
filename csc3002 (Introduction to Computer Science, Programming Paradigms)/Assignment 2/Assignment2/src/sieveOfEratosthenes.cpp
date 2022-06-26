#include <iostream>
#include "sieveOfEratosthenes.h"

/*
 * Function: sieveOfEratosthenes
 * Usage: sieveOfEratosthenes(isPrime);
 * ------------------------------------
 * Takes a Vector<bool> provided by the client and fills in its
 * elements with true for the primes and false for the nonprimes.
 */

void sieveOfEratosthenes(Vector<bool>& isPrime) {
    for (int i = 2; i < isPrime.size(); i++)
        isPrime[i] = true;
    for (int i = 2; i < isPrime.size(); i++) {
        if (isPrime[i] == false)
            continue;
        for (int n = 2; n <= (isPrime.size() - 1) / i ; n++) {
            isPrime[i * n] = false;
        }
    }
}
