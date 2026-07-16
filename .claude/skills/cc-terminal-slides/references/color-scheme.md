# Color Scheme

Extracted from Claude Code dark mode UI via color-picking reference screenshots and CC source code analysis.

## CSS Variables

```css
:root {
    /* Page background and text */
    --page-bg: #1c1c20;
    --page-text: #e2e2e6;
    --page-dim: #6a6a74;
    --page-muted: #44444e;

    /* Badge — terracotta/burnt orange accent */
    --badge-color: #c08060;
    --badge-border: rgba(192, 128, 96, 0.45);
    --badge-bg: rgba(192, 128, 96, 0.08);

    /* Terminal window */
    --term-bg: #282830;
    --term-header-bg: #2e2e36;
    --term-border: #3a3a42;
    --term-text: #d4d4dc;
    --term-dim: #6e6e78;
    --term-muted: #4a4a54;
    --prompt-bg: #333340;

    /* Traffic light dots */
    --dot-red: #ff5f57;
    --dot-yellow: #febc2e;
    --dot-green: #28c840;

    /* Semantic tool colors (from CC source + ref images) */
    --tool-blue: #7eb8d4;      /* Read, Write, Bash — permission blue */
    --tool-green: #7ec87e;     /* success, confirmed */
    --tool-orange: #d4a06b;    /* warnings, Recalling, numbers */
    --tool-red: #d46b6b;       /* errors, critical */
    --tool-pink: #d46ba8;
    --tool-purple: #9b7ed4;    /* keywords, flow control */
    --tool-cyan: #6bc8c8;      /* tags, labels, parameters */
    --tool-yellow: #d4c86b;    /* highlights, emphasis */
}
```

## Text Selection Highlight

Always include this so user text-selection matches the deck's palette instead of the browser's default blue (which clashes with the dark background and makes selected text hard to read):

```css
::selection { background: rgba(192, 128, 96, 0.45); color: #fff; text-shadow: none; }
::-moz-selection { background: rgba(192, 128, 96, 0.45); color: #fff; text-shadow: none; }
```

The `rgba(192, 128, 96, 0.45)` matches the badge's terracotta accent so highlights feel native to the deck.

## Color Provenance

| Color | Source | Used For |
|-------|--------|----------|
| `#1c1c20` | Color-picked from dark mode slide ref | Page background |
| `#282830` | Color-picked from terminal body | Terminal body |
| `#2e2e36` | Color-picked from terminal header | Terminal header bar |
| `#c08060` | Color-picked from "DEEP DIVE" badge | Accent / badge text |
| `#D77757` | CC source `rgb(215,119,87)` | Claude orange (brand) |
| `#5769F7` | CC source `rgb(87,105,247)` | Permission/tool blue |
| `#ff5f57` | Standard macOS traffic light | Close dot |
| `#febc2e` | Standard macOS traffic light | Minimize dot |
| `#28c840` | Standard macOS traffic light | Maximize dot |

## CC Source Findings

- **Font**: System default monospace (no explicit config). Use `'JetBrains Mono', monospace` as closest web substitute.
- **Titles**: Use `'Inter', -apple-system, sans-serif`.
- **Bullet character**: `⏺` (U+23FA) on macOS (`figures.ts`), `●` on other platforms.
- **Prompt character**: `❯` (U+276F) from `figures.pointer`.
- **Horizontal dividers**: `─` (U+2500, box-drawing light horizontal).
- **Border radius**: 8px (SVG), 16px (PNG) from CC source.
