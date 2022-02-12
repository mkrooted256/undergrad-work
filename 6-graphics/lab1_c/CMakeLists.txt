cmake_minimum_required(VERSION 3.21)
project(lab1)

set(CMAKE_CXX_STANDARD 14)

set(SDL_DIR "C:/Users/mkrooted/Development/SDL2")

add_executable(lab1 main.cpp)
target_link_directories(lab1 PRIVATE ${SDL_DIR}/lib)
target_link_libraries(lab1 mingw32 SDL2main SDL2)
target_include_directories(lab1 PRIVATE ${SDL_DIR}/include)
