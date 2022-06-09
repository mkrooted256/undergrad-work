#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <fstream>
#include <iostream>
#include <windows.h>

#include <vector>
#include <cassert>

#include "render.h"

// ------------------------

void prepare_bodies(std::vector<std::shared_ptr<Body>>& bodies) 
{
    // Yellow center sphere
    auto* geom = (Geometry*) new Sphere({0,0,0}, 30);
    auto* mat = new Material();
    mat->matte = Vec3f{ 250, 241, 53 } / 255;
    bodies.emplace_back(new Body(geom, mat));

    // Blue closer right sphere
    geom = (Geometry*) new Sphere({20, -30, 10}, 10);
    mat = new Material();
    mat->matte = Color{ 0.2, 0.2, 0.9 };
    bodies.emplace_back(new Body(geom, mat));
}

void prepare_lights(std::vector<std::shared_ptr<Light>>& lights)
{
    auto* light = new PointLight();
    light->loc = { 50, -100, 50 };
    light->color = { 1, 1, 1 };
    light->brightness = 1;

    lights.emplace_back(light);
}


void test1() {
    Sphere S({0,0,0}, 50);

    TraceResult tr{};
    bool hit = S.Intersect(Ray{{0,0,0}, Vec3f{0.9,0.3,0}.Ort()}, tr);

    if (!hit) std::cout<<"Miss";
    else std::cout << "hit at " << tr.hitpoint << " with n" << tr.normal << " after " << tr.t << std::endl;
}


int main()
{
//    test1();

//    Vec3f v{-100,0,100};
//    std::cout << clip3f(v, -1, 1) << std::endl;
//    return 0;

    std::unique_ptr<Scene> scene = std::make_unique<Scene>();

    prepare_bodies(scene->bodies);
    prepare_lights(scene->lights);

    Renderer renderer;
    renderer.scene = scene.get();

    renderer.width = 400;
    renderer.height = 300;
    renderer.fov = 60;
    renderer.camera = { {0, -100, 0}, {0, 1, 0} };
    renderer.camera_up = { 0, 0, 1 };
    renderer.camera_right = { 1, 0, 0 };

    renderer.backgroundColor = Color{0,0,0};
    renderer.globalIllumination = Color{1,1,1} * 0.1;

    std::cout << "Starting the render..." << std::endl;
    renderer.Render("hellocg.bmp");
    std::cout << "Render finished!" << std::endl;

    return 0;
}
