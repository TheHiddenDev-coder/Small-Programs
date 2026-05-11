#include <iostream>
#include <string>
#include <iomanip>
using str = std::string;

int main()
{
    int decision;
    double balance = 0.0; // initialize balance
    double amount;
    std::cout << "****************************************\n";
    std::cout << "\nFully Disfunctional Banking App (FDBA)\n";

    do {
        std::cout << "\nMenu:\n";
        std::cout << "1) Check Balance\n";
        std::cout << "2) Deposit\n";
        std::cout << "3) Withdraw\n";
        std::cout << "4) Exit\n";
        std::cout << "Enter your choice: ";
        std::cin >> decision;

        switch (decision)
        {
        case 1:
            std::cout << "Your balance is: $" << std::fixed << std::setprecision(2) << balance << "\n";
            break;
        case 2:
            std::cout << "Enter amount to deposit: $";
            std::cin >> amount;
            balance += amount;
            std::cout << "Deposited: $" << std::fixed << std::setprecision(2) << amount << "\n";
            break;
        case 3:
            std::cout << "Enter amount to withdraw: $";
            std::cin >> amount;
            if (amount > balance)
                std::cout << "Insufficient funds!\n";
            else
            {
                balance -= amount;
                std::cout << "Withdrew: $" << std::fixed << std::setprecision(2) << amount << "\n";
            }
            break;
        case 4:
            std::cout << "Exiting the application.\n";
            break;
        default:
            std::cout << "Invalid choice. Please try again.\n";
            break;
        }
    } while (decision != 4);

    return 0;
}
