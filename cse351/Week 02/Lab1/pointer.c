/*
 * Chun-Wei Chen
 * CSE 351
 * 04/10/13
 */

/*
 * CSE 351 HW1 (Data Lab - Pointers)
 *
 * <Please put your name and userid here>
 *
 * pointer.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, the following function declaration should prevent a
 * compiler warning. In general, it's not good practice to ignore
 * compiler warnings, but in this case it's OK.
 */
int printf(const char *, ...);

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to this homework by
editing the collection of functions in this source file.

INTEGER CODING RULES:

  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code
  must conform to the following style:

  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. For 1-3, only Unary integer operations *, & and Binary integer
      operations - + * are allowed. For the last three, you may also
      use shifts (<<, >>), ~, ==, and ^.

  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, ?: or sizeof.
  6. Use any data type other than those already in the declarations provided.

  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting an integer by more
     than the word size.

/*
 * STEP 2: Modify the following functions according the coding rules.
 *
 * Test the code below in your own 'main' program.
 *
 */

#endif

/*
 * Return the size of an integer in bytes.
 */
int intSize() {
    int intArray[10];
    int *ptr1;
    int *ptr2;
    
    ptr1 = &(intArray[0]);
    ptr2 = &(intArray[1]);
    
    return (long)(ptr2) - (long)(ptr1);
}

/*
 * Return the size of a double in bytes.
 */
int doubleSize() {
  double doubArray[10];
  double * doubPtr1;
  double * doubPtr2;
  /*
   * Use two pointers point to first two element in the array, 
   * and then subtract the address of the element the second 
   * points to by the address of the element the first 
   * points to to get the size of double.
   */
  doubPtr1 = doubArray;
  doubPtr2 = doubPtr1 + 1;
  return (char*) doubPtr2 - (char*) doubPtr1;
}

/*
 * Return the size of a pointer in bytes.
 */
int pointerSize() {
  double * ptrArray[10];
  double ** ptrPtr1;
  double ** ptrPtr2;
  /*
   * Use two pointers point to first two element in the array, 
   * and then subtract the address of the element the second 
   * points to by the address of the element the first 
   * points to to get the size of pointer.
   */
  ptrPtr1 = ptrArray;
  ptrPtr2 = ptrPtr1 + 1;
  return (char*) ptrPtr2 - (char*) ptrPtr1;
}

/*
 * Modify intArray[5] to be the value 351 using only &intArray and pointer arithmetic.
 */
int changeValue() {
    int intArray[10];
    int * intPtr1 = intArray;
    int * intPtr2;
    
    intPtr2 = intPtr1 + 5;
    *intPtr2 = 351;
    
    return intArray[5];
}


/*
 * Return 1 if ptr1 and ptr2 are within the *same* 64-byte aligned  block (or
 * word) of memory. Return zero otherwise.
 * Operators / and % and loops are NOT allowed.
 */
int withinSameBlock(int * ptr1, int * ptr2) {
  /*
   * Two pointers are within the same block of memory if their 
   * addresses are the same except the last six bits. So mask 
   * out the last six bits in order to compare the equality.
   */
  long p1 = (long)ptr1;
  long p2 = (long)ptr2;
  long mask;
  mask = 0xFFFFFFFFFFFFFFC0;
  p1 = p1 & mask;
  p2 = p2 & mask;
  int res;
  res = !(p1 ^ p2);
  return res;
}

/*
 * Return 1 if ptr points to an element within the specified intArray, 0 otherwise.
 */
int withinArray(int * intArray, int size, int * ptr) {
  /*
   * If the pointer points to an element within the array, the 
   * sign of difference between the address of first element in the array
   * and the address of element the pointer points to (p3 - p1) will be 
   * the same as the sign of difference between the address of last 
   * element in the array and the address of element the pointer 
   * points to (p2 - p3).
   */
    int p1 = (long) intArray;
    int p2 = p1 + 4 * (size - 1);
    int p3 = (long) ptr;
    int diff_ptr2start = p3 - p1; 
    int diff_end2ptr = p2 - p3;
    
    diff_ptr2start = !(diff_ptr2start >> 31);
    diff_end2ptr = !(diff_end2ptr >> 31);
    return diff_end2ptr & diff_ptr2start;
}
/*
 * Return x with the n bits that begin at position p inverted (i.e., turn 0 into
 * 1 and vice versa) and the rest left unchanged. Consider the indices of x to
 * begin with the low-order bit numbered as 0.
 */
int invert(int x, int p, int n) {
  /*
   * Create the mask which has n 1's bits at the last n bits, 
   * and then shift left the value of the mask by p, and use 
   * ^ to x and the mask to invert n bits begin at position p.
   */
  int mask = (-1)^(-1 << n);
  mask = mask << p;
  int res;
  res = x ^ mask;
  return res;
}
