#pragma once

#include "color.h"
#include <cassert>

#define M_PI (3.141592653589793)
#define EPS (1e-6)
#define is_smol(f) ((-EPS < f) && (f < EPS))

struct Vec3f {
    float x;
    float y;
    float z;

    Vec3f operator*(float k) const { return { x*k, y*k, z*k }; }
    // friend Vec3f operator*(float k, const Vec3f& v) const { return v*k; }
    Vec3f operator/(float k) const { return { x/k, y/k, z/k }; }

    Vec3f& operator+=(const Vec3f& v) { x+=v.x; y+=v.y; z+=v.z; return *this; }
    Vec3f& operator-=(const Vec3f& v) { x-=v.x; y-=v.y; z-=v.z; return *this; }
    Vec3f operator+(const Vec3f& v) const { Vec3f o; return o+=v; }
    Vec3f operator-(const Vec3f& v) const { Vec3f o; return o-=v; }
    Vec3f operator-() const { return { -x, -y, -z }; }

    float Dot(const Vec3f& v) const { return x*v.x + y*v.y + z*v.z; }
    Vec3f Cross(const Vec3f& v) const { return { y*v.z - z*v.y, z*v.x - x*v.z, x*v.y - y*v.x }; }

    float Normsq() const { return x*x + y*y + z*z; };
    float Norm() const { return sqrt(x*x + y*y + z*z); };
    Vec3f Ort() const { return *this / Norm(); } // TODO: fast inverse sqrt

    float Angle(const Vec3f& v) const { return Dot(v) / sqrt(Normsq() * v.Normsq()); }

    bool operator>(float f) { return x>f && y>f && z>f; }
    bool operator>=(float f) { return x>=f && y>=f && z>=f; }
    bool operator<(float f) { return x<f && y<f && z<f; }
    bool operator<=(float f) { return x<=f && y<=f && z<=f; }
};

struct Ray {
    Vec3f origin;
    Vec3f dir;

    Vec3f Reflect(const Vec3f& normal) { return dir + (normal + normal) * dir.Dot(normal); }
};

struct TraceResult {
    Vec3f hitpoint;
    Vec3f normal;
    Vec3f reflection;
};

struct Geometry {
    Color matte;
    Color emission;

    float brightness = 0;
    float opacity = 1;
    float reflection = 0;

    bool doublesided = false;

    /* true if hit */
    virtual bool Trace(const Ray& ray, TraceResult& result) { return false; };
};


struct Plane : public Geometry {
    Vec3f normal;
    float d;

    /* F(x,y,z) = Ax + By + Cz + d */
    /* F(point) = 0 */
    /* normal.Dot(point) + d = 0 */

    Plane(Vec3f normal, Vec3f point) : normal(normal), d(-normal.Dot(point)) {};

    float F(Vec3f p) { return normal.Dot(p) + d; }

    virtual Vec3f Trace(const Ray& ray, TraceResult& result) override {
        /*
        (Aa + Bb + Cc)t + Aa0 + Bb0 + Cc0 + d = 0
        t = -F(p0) / normal.Dot(ray.direction)
        */
        float prod = normal.Dot(ray.dir);
        if (is_smol(prod)) return false;
        float t = -F(ray.origin) / prod;

        if ( t < 0 ) return false;
        if ( prod > 0 && !doublesided ) return false;

        result.hitpoint = ray.origin + ray.dir * t;
        result.normal = normal;

        return true;
    }
};

struct Sphere : public Geometry {
    Vec3f O;
    float R;
private:
    float Rsq;
public:

    Sphere(Vec3f origin, Vec3f radius) : O(origin), R(radius), Rsq(radius*radius) {}

    float F(Vec3f p) { return (p - O).Normsq() - Rsq; }

    virtual Vec3f Trace(const Ray& ray, TraceResult& result) override {
        /* 1. Distance from ray to the origin */
        /* 
            F(p(t)) = (ray.dir * t + ray.origin - O).Normsq() - Rsq;
            F't(t0) = 2(ray.dir * t0 + ray.origin - O).Dot(ray.dir) = 
                    = 2*ray.dir.Normsq*t0 + (ray.origin - O).Dot(ray.dir) = 0
            t0 = (O - ray.origin).Dot(ray.dir) / (2 ray.dir.Normsq)
        */
        
        float t = (O - ray.origin).Dot(ray.dir) / (2 * ray.dir.Normsq());

        return true;
    }
}