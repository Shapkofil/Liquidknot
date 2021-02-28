//Copyright (c) 2020 BlenderNPR and contributors. MIT license.

#include "Pipelines/NPR_Pipeline.glsl"

uniform sampler2D color_texture;

void LIGHT_SHADER(LightShaderInput I, inout LightShaderOutput O)
{
    O.color = texture(color_texture, I.light_uv.xy) * I.LS.P;
}

