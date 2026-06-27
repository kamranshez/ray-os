---
tags: [youtube, recording, obs, loom, reverse-engineering]
aliases: [loom-obs-color-match]
date: 2026-06-24
---

Goal: get the OBS webcam feed to look like Loom's "auto lighting" / Enhance, exactly, instead of eyeballing OBS Color Correction sliders forever.

## The big finding

Loom has no "auto" anything. There is no histogram, no auto-exposure, no adaptive relight in the client. What reads as auto lighting is really three things stacked: the webcam's own hardware auto-exposure, a fixed enhancement curve, and (optionally) a named filter preset.

The enhancement is a Three.js WebGL shader (`@loomhq-desktop/camera-kit`, `src/gl/shaders.ts`), not AI. It is pure arithmetic, no LUT.

**The plain-webcam path (no virtual background, blemish-smoothing off, which is Ray's setup) is ONLY a gamma curve:**

```glsl
gl_FragColor = gammaCorrect(foreground, uGamma);   // pow(color, 1.0/gamma)
```

A single gamma boost brightens midtones, lifts shadows (the flat look), and slightly desaturates warm shadows all at once. That is why chasing it with separate brightness, contrast, and saturation sliders never lined up. It is one operation, not five.

Brightness, contrast, saturation, and hue only run when a named Filter is selected. Order in Loom's shader is: brightness, contrast, saturation, hue, sepia, grayscale, gradient, then gamma last.

## The decision

Stop hand-tuning OBS's built-in Color Correction filter. Its math differs from Loom's (additive brightness, a different contrast curve), so a perfect match was impossible. Instead, port Loom's exact GLSL into OBS via the `obs-shaderfilter` plugin. Same constants, same operations, same order. See [[loom-enhance.shader]] in this folder.

For the Enhance look, only the Gamma slider matters. The other sliders default to no-op and exist only to reproduce a named Loom Filter exactly.

## Setup

1. Plugin: `obs-shaderfilter` by Exeldro, release 2.6.0, asset `obs-shaderfilter-2.6.0-macos-arm64.pkg` (Apple Silicon). Install, fully restart OBS.
2. Camera source, Filters, +, User-defined shader, tick "Load shader text from file", point it at this folder's `loom-enhance.shader`.
3. Tune the Gamma slider from a 1.40 starting point until it matches Loom.

Note: if the shader is loaded from this repo path, re-point OBS's "Shader text file" field here (it was previously on the Desktop).

## Known caveats (why it may still differ slightly)

1. The exact gamma value Loom's Enhance uses is set by Loom's UI code, which loads remotely and was not in the extracted binary. So the operation is identical but the value is matched by eye. Once matched, it stays identical.
2. Input frame parity: Loom applies the shader to its own capture of the camera (its exposure and white balance), OBS to its own. Same shader, different input, slightly different output. Fix exposure and white balance at the camera source for a true match.
3. Possible Three.js output color-space encoding after the shader. Checked and likely not active on a raw video shader, but if a uniform consistent tint remains after matching gamma, that is the suspect.

## Reference: Loom filter presets (from `FILTER_MAP`)

Exact multipliers if reproducing a named look via the optional sliders:

- Lark: brightness 1.10, contrast 0.90, saturation 1.20
- Burst: contrast 1.20, saturation 1.35
- Aden: brightness 1.20, contrast 0.90, saturation 0.85, hue -20 deg
- Reyes: brightness 1.10, contrast 0.85, saturation 0.75, sepia 0.22
- Bold: contrast 1.50, saturation 1.10

## Not ported (yet)

Blemish smoothing: a masked bilateral blur (`uIsBlemishSmoothingEnabled`). Ray had it off in Loom, so it was left out. The exact GLSL exists if it is ever wanted. Stock OBS cannot do selective skin smoothing without a plugin.

Source app: Loom.app v0.355.2, Electron, package `@loomhq-desktop/camera-kit`.
