// ============================================================================
//  Loom "Enhance" — exact port of Loom's camera-kit WebGL shader
//  Reverse-engineered from Loom.app v0.355.2
//    @loomhq-desktop/camera-kit  ->  src/gl/shaders.ts + src/gl/materials.ts
//
//  For the OBS plugin "obs-shaderfilter" (Exeldro).
//  Add it to your camera source:  Filters -> + -> "User-defined shader"
//  -> "Load shader text from file" -> pick this file.
//
//  KEY FINDING: Loom's plain-webcam "Enhance" (no virtual background,
//  blemish-smoothing off) is ONLY a gamma curve:  pow(color, 1.0/gamma).
//  Brightness / Contrast / Saturation / Hue are applied ONLY when you pick a
//  named Filter (Lark, Burst, ...). So to match Loom, tune ONE knob: Gamma.
//  Loom applies them in this exact order, gamma last — replicated below.
// ============================================================================

// ---- Gamma : the whole "Enhance" look. Loom: pow(color, 1.0/gamma) ----------
uniform float gamma <
    string label = "Gamma (the Enhance look)";
    string widget_type = "slider";
    float minimum = 0.50;
    float maximum = 2.50;
    float step    = 0.01;
> = 1.40;

// ---- Optional: only needed to reproduce a named Loom Filter preset ----------
// Defaults below are 1.0 / 0.0 = no change (matches plain Enhance).
//   Lark : brightness 1.10, contrast 0.90, saturation 1.20
//   Burst: contrast 1.20, saturation 1.35
//   Aden : brightness 1.20, contrast 0.90, saturation 0.85, hue -20
uniform float brightness <
    string label = "Brightness (x, Loom multiply)";
    string widget_type = "slider";
    float minimum = 0.50; float maximum = 2.00; float step = 0.01;
> = 1.00;

uniform float contrast <
    string label = "Contrast (x)";
    string widget_type = "slider";
    float minimum = 0.50; float maximum = 2.00; float step = 0.01;
> = 1.00;

uniform float saturation <
    string label = "Saturation (x)";
    string widget_type = "slider";
    float minimum = 0.00; float maximum = 2.00; float step = 0.01;
> = 1.00;

uniform float hue_shift_deg <
    string label = "Hue shift (degrees)";
    string widget_type = "slider";
    float minimum = -180.0; float maximum = 180.0; float step = 1.0;
> = 0.0;

float4 mainImage(VertData v_in) : TARGET
{
    float4 color = image.Sample(textureSampler, v_in.uv);

    // (1) Brightness  -- Loom: vec4(color.rgb * brightness, color.a)
    color.rgb = color.rgb * brightness;

    // (2) Contrast    -- Loom: ((rgb - 0.5) * contrast) + 0.5
    color.rgb = ((color.rgb - 0.5) * contrast) + 0.5;

    // (3) Saturation  -- Loom: mix(luma, rgb, sat), Rec.601 weights
    float gray = dot(color.rgb, float3(0.299, 0.587, 0.114));
    color.rgb = lerp(float3(gray, gray, gray), color.rgb, saturation);

    // (4) Hue shift   -- Loom: YIQ rotation. Faithful to Loom's GLSL
    //     column-major mat3*vec3 (replicated here with explicit dots).
    //     hue = 0 -> identity, so this is a no-op for the plain Enhance look.
    if (abs(hue_shift_deg) > 0.0001)
    {
        float y = dot(color.rgb, float3(0.299,  0.595716,  0.211456));
        float i = dot(color.rgb, float3(0.587, -0.274453, -0.522591));
        float q = dot(color.rgb, float3(0.114, -0.321263,  0.311135));
        float ang    = atan2(q, i) + radians(hue_shift_deg);
        float chroma = sqrt(i * i + q * q);
        float ni = chroma * cos(ang);
        float nq = chroma * sin(ang);
        color.r = dot(float3(y, ni, nq), float3(1.0,  1.0,     1.0));
        color.g = dot(float3(y, ni, nq), float3(0.9563, -0.2721, -1.1070));
        color.b = dot(float3(y, ni, nq), float3(0.6210, -0.6474,  1.7046));
    }

    // (5) Gamma -- Loom's final step in EVERY shader: pow(color, 1.0/gamma)
    float inv_g = 1.0 / gamma;
    color.rgb = pow(max(color.rgb, 0.0), float3(inv_g, inv_g, inv_g));

    return float4(saturate(color.rgb), color.a);
}
