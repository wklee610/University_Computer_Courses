/*
 * File: bigint.cpp
 * ----------------
 * This file implements the bigint.h interface.
 */

#include <cctype>
#include <string>
#include "bigint.h"
#include "error.h"
#include "strlib.h"

/*
 * Implementation notes: BigInt constructor
 * ----------------------------------------
 * Creates a new BigInt from an int or a string of decimal digits.
 */

BigInt::BigInt(std::string str)
{
    /*
     *  Please add function body
     */
}

BigInt::BigInt(int k)
{
    /*
     *  Please add function body
     */
}

/*
 * Implementation notes: BigInt destructor
 * ---------------------------------------
 * Frees the memory used by a BigInt when it goes out of scope.
 */

BigInt::~BigInt()
{
    /*
     *  Please add function body
     */
}

/*
 * Implementation notes: toString
 * ------------------------------
 * Converts a BigInt object to the corresponding string.
 */

std::string BigInt::toString() const
{
    /*
     *  Please add function body
     */
}

BigInt BigInt::operator+(const BigInt & b2) const
{
    /*
     *  Please add function body
     */
}

BigInt BigInt::operator*(const BigInt & b2) const
{
    /*
     *  Please add function body
     */
}


BigInt fact(int n)
{
   BigInt result("1");
   for (int i = 1; i <= n; i++)
   {
      result = result * BigInt(i);
   }
   return result;
}
