#pragma once
#include "color.h"

struct Display {
    int W;
    int H;
    Color * buf;
    Color ** rows;

    Display(int w, int h) {
        W = w;
        H = h;
        const int s = w*h;
        buf = new Color[s];
        rows = new Color*[h];
        
        Color * row = buf;
        for ( int i=0 ; i < h; ++i ) {
            rows[i] = buf;
            buf += w;
        }
    }

    void Fill(Color c) {
        int y=0;
        for (int i=0; i<H; i++) {
            for (int j=0; j<W; j++) {
                buf[y + j] = c;
            }
            y+=W;
        }
    }

    void Set(int x, int y, Color c) {
        rows[y][x] = c;
    }
};
