/*
 * File: bigint.h
 * --------------
 * This interface exports the BigInt class, which makes it possible to
 * represent nonnegative integers of arbitrary magnitude.
 */

#ifndef _bigint_h
#define _bigint_h

#include <string>

class BigInt {

public:

/*
 * Constructor: BigInt
 * Usage: BigInt big(str); BigInt big(int);
 * -----------------------
 * Creates a new BigInt from an int or a string of decimal digits.
 */

   BigInt(std::string str);
   BigInt(int k);

/*
 * Destructor: ~BigInt
 * -------------------
 * Frees the memory used by a BigInt when it goes out of scope.
 */

   ~BigInt();

/*
 * Method: toString
 * Usage: string str = bigint.toString();
 * --------------------------------------
 * Converts a BigInt object to the corresponding string.
 */

   std::string toString() const;

   BigInt operator+(const BigInt & b2) const;
   BigInt operator*(const BigInt & b2) const;

/* Private section */

/*
 * Implementation notes: BigInt data structure
 * -------------------------------------------
 * The BigInt data structure stores the digits in the number in
 * a linked list in which the digits appear in reverse order with
 * respect to the items in the list.  Thus, the number 1729 would
 * be stored in a list like this:
 *
 *     start
 *    +-----+    +-----+    +-----+    +-----+    +-----+
 *    |  o--+--->|  9  |  ->|  2  |  ->|  7  |  ->|  1  |
 *    +-----+    +-----+ /  +-----+ /  +-----+ /  +-----+
 *               |  o--+-   |  o--+-   |  o--+-   | NULL|
 *               +-----+    +-----+    +-----+    +-----+
 */

private:

/*
 * Type: Cell
 * ----------
 * This structure type holds a single digit in the linked list.
 */

   struct Cell
   {
      Cell *leadingDigits;
      int Digit;
   };

/* Instance variables */

   Cell *start;          /* Linked list of digits */
};

BigInt fact(int n);

#endif
