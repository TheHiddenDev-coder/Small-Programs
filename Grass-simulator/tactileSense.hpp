#pragma once
#include "grass.hpp"

struct TactileSense {
    void touch(Grass& g) {
        g.isTouched = true;
    }
};