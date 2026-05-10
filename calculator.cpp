

#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    double a = 0.0; // Default a to 0.0
    double b = 0.0; // Default b to 0.0
    char op;      // Variable to store the operator
    double result;

    cout << "What operation would you like to perform? (+ - * /): "; // Prompt user for operation
    cin >> op; // Read operation from user
    cout << "Enter the first number: "; // Prompt user for first number
    cin >> a; // Read first number from user
    cout << "Enter the second number: "; // Prompt user for second number
    cin >> b; // Read second number from user
    switch (op) {
        case '+':
            result = a + b;
            cout << fixed << setprecision(1) << a << " + " << b << " = " << result << endl;
            break;
        case '-':
            result = a - b;
            cout << fixed << setprecision(1) << a << " - " << b << " = " << result << endl;
            break;
        case '*':
            result = a * b;
            cout << fixed << setprecision(1) << a << " * " << b << " = " << result << endl;
            break;
        case '/':
            if (b != 0) {
                result = a / b;
                cout << fixed << setprecision(1) << a << " / " << b << " = " << result << endl;
            } else {
                cout << "Error: Division by zero is undefined." << endl;
            }
            break;
        default:
            cout << "Error: Invalid operator." << endl;
    }
}

    return 0;
}

