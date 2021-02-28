//Copyright (c) 2020 BlenderNPR and contributors. MIT license.

#include "Pipelines/NPR_Pipeline.glsl"

uniform int ao_samples = 16;
uniform float ao_radius = 0.75;

void COMMON_PIXEL_SHADER(Surface S, inout PixelOutput PO)
{
    float ao = get_ao(ao_samples, ao_radius);
    
    PO.color.rgb = vec3(ao);
}

