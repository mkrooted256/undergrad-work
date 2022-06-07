#pragma once

#define clip(v, min, max) ( (v<min) ? (min) : ( (v>max) ? max : v ) )

struct Color {
    uint8_t r;
    uint8_t g;
    uint8_t b;

    Color() : r(0), g(0), b(0) {};
    Color(int R, int G, int B) { r=clip(R, 0, 255); g=clip(G, 0, 255); b=clip(B, 0, 255); }
};