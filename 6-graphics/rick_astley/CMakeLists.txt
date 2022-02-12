cmake_minimum_required(VERSION 3.21)
project(lab1)

set(CMAKE_CXX_STANDARD 14)

set(SDL2_DIR "C:/Users/mkrooted/Development/SDL2")

# -w suppresses all warnings
# -Wl,-subsystem,windows gets rid of the console window
set(COMPILER_FLAGS "-Wl,-subsystem,windows")
set(CMAKE_CXX_FLAGS "${COMPILER_FLAGS}")

add_executable(lab1 main.cpp)

add_library(SDL2 ${SDL2_DIR}/lib/libSDL2.a)
add_library(SDL2main ${SDL2_DIR}/lib/libSDL2main.a)
set_target_properties(SDL2 PROPERTIES LINKER_LANGUAGE CXX)
set_target_properties(SDL2main PROPERTIES LINKER_LANGUAGE CXX)

target_include_directories(lab1 PRIVATE ${SDL2_DIR}/include)
target_link_libraries(lab1 PRIVATE mingw32 SDL2main SDL2)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")