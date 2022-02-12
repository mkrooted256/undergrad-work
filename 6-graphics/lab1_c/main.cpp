#include "SDL2/SDL.h"
#include <cstdio>
#include <iostream>

bool init();

void close();

SDL_Window *gWindow = nullptr;
SDL_Surface *gScreenSurface = nullptr;
SDL_Surface *gHelloWorld = nullptr;
SDL_Renderer *gRenderer = nullptr;

int PADDING = 10;
int SCREEN_W = 480 + PADDING;
int SCREEN_H = 480 + PADDING;
int LAB_W = 120;
int LAB_H = 120;
int factor = 4;

const char *PROJECT = "Lab1: Line rendering.";


bool init() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return false;
    }

    gWindow = SDL_CreateWindow(PROJECT, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                               SCREEN_W, SCREEN_H, SDL_WINDOW_SHOWN );
    if (gWindow == nullptr) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return false;
    }
    gScreenSurface = SDL_GetWindowSurface(gWindow);

    gRenderer = SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED);
    if (gRenderer == nullptr) {
        printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
        return false;
    }

    SDL_FillRect( gScreenSurface, nullptr, SDL_MapRGB( gScreenSurface->format, 0xFF, 0xFF, 0xFF ) );

    return true;
}

void close() {
    //Deallocate surface
    SDL_FreeSurface(gHelloWorld);
    gHelloWorld = nullptr;

    //Destroy window
    SDL_DestroyWindow(gWindow);
    gWindow = nullptr;

    //Quit SDL subsystems
    SDL_Quit();
}


void show_lab() {
    SDL_Surface *smol_surf = SDL_CreateRGBSurfaceWithFormat(
            0, LAB_W, LAB_H, 8, gScreenSurface->format->format
    );

    SDL_Rect target_rect{PADDING, PADDING, factor * LAB_W, factor * LAB_H};

    SDL_FillRect(smol_surf, nullptr, SDL_MapRGB(gScreenSurface->format,0xff, 0, 0));
    SDL_BlitScaled(smol_surf, nullptr, gScreenSurface, &target_rect);
}

void loop() {
    SDL_Event e;
    while (true) {
        while (SDL_PollEvent(&e) != 0) {
            //User requests quit
            if (e.type == SDL_QUIT) {
                return;
            }
        }
    }
}

int main(int argc, char *args[]) {
    printf("Hello, World!\n");

    if (!init()) {
        printf("Failed to initialize!\n");
        return 1;
    }

    show_lab();
    SDL_RenderClear( gRenderer );
    SDL_SetRenderDrawColor(gRenderer, 0,0,0,0xff);
    SDL_RenderDrawLine(gRenderer, PADDING/2, PADDING/2, PADDING/2, SCREEN_H);
    SDL_RenderDrawLine(gRenderer, PADDING/2, PADDING/2, SCREEN_W, PADDING/2);
    SDL_RenderFlush(gRenderer);

    SDL_UpdateWindowSurface(gWindow);



    loop();
    close();

    return 0;
}
