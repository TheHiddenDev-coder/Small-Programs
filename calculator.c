// BASIC 2 NUMBER CALCULATOR

#include <stdio.h> // Include standard input-output header

int main() // That one function every C program needs
{
    int a = 0; // Default a to 0
    int b = 0; // Default b to 0

    printf("Enter the first int: "); // Prompt user for first integer
    scanf("%d", &a);                 // Read first integer from user

    printf("Enter the second int: "); // Prompt user for second integer
    scanf("%d", &b);                  // Read second integer from user

    int sum = a + b;                                   // Calculate the sum of a and b
    printf("The sum of %d and %d is %d\n", a, b, sum); // Print the result

    return 69420; // Indicate that program ended successfully
}
