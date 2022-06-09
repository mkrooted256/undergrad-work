#pragma once
#include <vector>
#include <memory>
#include <iostream>

#include "common.h"
#include "geometry.h"
#include "light.h"
#include "shading.h"

struct Body {
    std::unique_ptr<Geometry> geom;
    std::unique_ptr<Material> mat;

    Body() = default;
    Body(Geometry* g, Material* m) : geom(g), mat(m) {};
};

struct Scene {
    std::vector<std::shared_ptr<Body>> bodies;
    std::vector<std::shared_ptr<Light>> lights;
};

struct Tracer {
    int maxTracingDepth = 5;
    float maxDistance = 1e8;

    Body * Trace(Scene* scene, const Ray& ray, TraceResult& traceResult) {
        float tmin = maxDistance;
        Body *foundBody = nullptr;

        for (const std::shared_ptr<Body> &body: scene->bodies) {
            bool hit = body->geom->Intersect(ray, traceResult);
            if (hit && traceResult.t < tmin && ray.dir.Dot(traceResult.normal) < 0) {
                tmin = traceResult.t;
                foundBody = body.get();
            }
        }

        return foundBody;
    }
};
