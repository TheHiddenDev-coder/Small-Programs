#include <iostream>
#include "grass.hpp"
#include "tactileSense.hpp"

int main() {
    Grass grass;
    TactileSense hand;
    hand.touch(grass);

    if (grass.isTouched) {
        std::cout << "grass has been touched." << '\n';
    }
}