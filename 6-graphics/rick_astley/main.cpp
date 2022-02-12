//Using SDL2 and standard IO
#include "SDL2/SDL.h"
#include <cstdio>

//Screen dimension constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;

void load_media(SDL_Surface *pics[3]) {
    //Load splash image
    pics[1] = SDL_LoadBMP( "res/rickroll.bmp" );
    pics[0] = SDL_LoadBMP( "res/rickroll_l.bmp" );
    pics[2] = SDL_LoadBMP( "res/rickroll_r.bmp" );
}


int main( int argc, char* args[] ) {
    //The window we'll be rendering to
    SDL_Window *window = nullptr;

    //The surface contained by the window
    SDL_Surface *screenSurface = nullptr;
    SDL_Surface *pics[3];
    load_media(pics);

    //Initialize SDL2
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL2 could not initialize! SDL_Error: %s\n", SDL_GetError());
    }
    else {
        //Create window
        window = SDL_CreateWindow("SDL2 Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH,
                                  SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
        if (!window || !pics[1]) {
            printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        }
        else {
            //Get window surface
            screenSurface = SDL_GetWindowSurface( window );

            //Fill the surface white
            SDL_FillRect( screenSurface, nullptr, SDL_MapRGB( screenSurface->format, 0xFF, 0xFF, 0xFF ) );

            SDL_Rect rect1{SCREEN_WIDTH/4, SCREEN_HEIGHT/4, SCREEN_WIDTH/2, SCREEN_HEIGHT/2};
            SDL_BlitScaled( pics[1], nullptr, screenSurface, &rect1 );

            //Update the surface
            SDL_UpdateWindowSurface( window );

            //Main loop flag
            bool quit = false;

            //Event handler
            SDL_Event e;
            SDL_Keycode last_valid_keycode = SDLK_UNKNOWN;

            while (!quit) {
                //Handle events on queue
                while( SDL_PollEvent( &e ) != 0 )
                {
                    bool updated = false;

                    //User requests quit
                    if( e.type == SDL_QUIT ) {
                        quit = true;
                        printf("Exiting....");
                        break;
                    } else if( e.type == SDL_KEYDOWN ) {
                        switch (e.key.keysym.sym) {
                            case SDLK_RIGHT: {
                                if (last_valid_keycode == SDLK_RIGHT) break;
                                updated = true;
                                printf("RIGHT!\n");
                                SDL_BlitScaled(pics[2], nullptr, screenSurface, &rect1);
                                last_valid_keycode = SDLK_RIGHT;
                                break;
                            }
                            case SDLK_LEFT: {
                                if (last_valid_keycode == SDLK_LEFT) break;
                                updated = true;
                                printf("LEFT!\n");
                                SDL_BlitScaled(pics[0], nullptr, screenSurface, &rect1);
                                last_valid_keycode = SDLK_LEFT;
                                break;
                            }
                        }
                    } else if( e.type == SDL_KEYUP ) {
                        if (last_valid_keycode == e.key.keysym.sym) {
                            printf("KEYUP!\n");
                            updated = true;
                            SDL_BlitScaled(pics[1], nullptr, screenSurface, &rect1);
                            last_valid_keycode = SDLK_UNKNOWN;
                        }
                    }

                    if (updated) {
                        SDL_UpdateWindowSurface( window );
                        updated = false;
                    }
                }
            }
        }
    }


    SDL_FreeSurface( pics[0] );
    SDL_FreeSurface( pics[1] );
    SDL_FreeSurface( pics[2] );
    //Destroy window
    SDL_DestroyWindow( window );

    //Quit SDL2 subsystems
    SDL_Quit();

    return 0;
}
