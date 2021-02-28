#include "Pipelines/NPR_Pipeline.glsl"

uniform int iters = 256;
uniform float clipping =  20.0;
uniform float plank = 0.001;
uniform float light_plank = 0.01;
uniform vec3 sun_pos = vec3(3,2,1);
uniform vec3 sun_color = vec3(.5, .8, .1);
uniform vec3 sky_color = vec3(.001, .08, .3);
uniform vec3 mate = vec3(.2);


float map( in vec3 pos )
{
    float d = length(pos) - 0.8;
    d = min(d, pos.z+.8);

    return d;
}

vec3 calc_normal( in vec3 p ){
   vec2 e = vec2 (light_plank, 0.0);
   return normalize(vec3(
                        map(p + e.xyy) - map(p - e.xyy),
                        map(p + e.yxy) - map(p - e.yxy),
                        map(p + e.yyx) - map(p - e.yyx)
    ));
}


float castRay(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i=0; i<iters; i++)
    {
        vec3 pos = ro + rd * t;
        float d = map ( pos );
        t +=  d;

        if ( d < plank )
            break;

    }
    return t;
}

void COMMON_PIXEL_SHADER(Surface S, inout PixelOutput PO)
{
    vec3 col = vec3(0.0);
    float alpha = 0.0;

    vec3 ro = S.position;
    vec3 rd = -view_direction();

    float t = castRay(ro, rd);


    if ( t < clipping)
    {
        vec3 pos = ro + rd * t;

        vec3 sun_dir = normalize(vec3(sun_pos));
        vec3 nor = calc_normal(pos);
        float sun_diff = clamp(dot(nor, sun_dir), 0.0, 1.0);
        float sun_sha = step(clipping, castRay(pos + nor * plank, sun_dir));
        float sky_diff = .5 + .5*clamp(dot(nor, vec3(0,0,1)), 0.0, 1.0);

        col = mate * sun_diff * sun_sha * sun_color;
        col += mate * sky_diff * sky_color;

        alpha = 1.0;
    }

    col = pow(col, vec3(.4545));
    PO.color = vec4(col, alpha);
}
