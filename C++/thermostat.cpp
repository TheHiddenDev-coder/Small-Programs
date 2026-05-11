//    My old thermostat script, which I initially wrote in Python
//    Now, it also reads user input

#include <iostream>
using namespace std;

int main()
{
    double temp;
    cout << "Enter the temperature: ";
    cin >> temp;

    if (!(cin >> temp))
    {
        cout << "Is that a temperature, Jimmy?"; // Truly charming
        return 1;
    }

    if (temp > 70)
    {
        cout << "How are you still alive!?";
    }
    else if (temp < 70 && temp >= 40)
    {
        cout << "It's sweltering! Stay inside";
    }
    else if (temp < 40 && temp >= 30)
    {
        cout << "It's hot!";
    }
    else if (temp < 30 && temp >= 20)
    {
        cout << "It's nice!";
    }
    else if (temp < 20 && temp >= 5)
    {
        cout << "It's cold!";
    }
    else if (temp < 5)
    {
        cout << "It's freezing! Stay inside!";
    }
    else
    {
        cout << "Call tech support, as your thermometer seems to not read a value";
    }
}
