# Slide Layouts

Five layout types cover all presentation needs. Each slide is a full-viewport `<div class="slide">`.

## Layout 1: Title + Terminal (Default)

Left 32% has badge + title. Right 68% has the terminal filling full height. This is the primary layout — use it for any slide that benefits from showing code, CLI output, or a simulated session.

```html
<div class="slide" data-n="1">
    <div class="slide-body">
        <div class="slide-left">
            <div class="badge">DEEP DIVE</div>
            <div class="slide-title">Title Here</div>
            <div class="slide-desc">Optional subtitle text.</div>
        </div>
        <div class="slide-right">
            <div class="terminal"><!-- ... --></div>
        </div>
    </div>
    <div class="slide-footer">
        <span>&larr; &rarr; to navigate</span>
        <span>1 / N</span>
    </div>
</div>
```

```css
.slide-body {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 56px;
    min-height: 0;
}
.slide-left {
    flex: 0 0 32%;
    max-width: 32%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.slide-right {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    max-height: 100%;
}
```

## Layout 2: Title + Terminal + Analogy

Same as Layout 1 but with an analogy callout box below the description on the left.

```html
<div class="slide-left">
    <div class="badge">DEEP DIVE</div>
    <div class="slide-title">Rate Limiter</div>
    <div class="slide-desc">Prevents noisy scripts from flooding.</div>
    <div class="analogy">
        Like a <strong>nightclub bouncer</strong>. Capacity: 10...
    </div>
</div>
```

```css
.analogy {
    margin-top: 20px;
    padding: 14px 18px;
    background: var(--badge-bg);
    border: 1px solid var(--badge-border);
    border-radius: 6px;
    font-size: 0.9rem;
    color: var(--page-dim);
    line-height: 1.7;
}
.analogy strong { color: var(--badge-color); }
```

## Layout 3: Stacked (Full-Width Content)

Title at top, content spans full width below. Use for comparison cards, tables, or content that needs horizontal space.

```html
<div class="slide-body stacked">
    <div class="slide-left">
        <div class="badge">DEEP DIVE</div>
        <div class="slide-title">Safety Rails</div>
    </div>
    <div class="slide-right">
        <table class="dt"><!-- ... --></table>
    </div>
</div>
```

```css
.slide-body.stacked {
    flex-direction: column;
    align-items: stretch;
    gap: 28px;
}
.slide-body.stacked .slide-left {
    flex: none; max-width: 100%;
}
```

## Layout 4: Stats + Terminal

Stats row above the terminal on the right side. Use for data-heavy slides.

```html
<div class="slide-right">
    <div class="stats">
        <div class="stat-box"><div class="stat-v">10</div><div class="stat-l">Burst</div></div>
        <div class="stat-box"><div class="stat-v">2s</div><div class="stat-l">Refill</div></div>
    </div>
    <div class="terminal"><!-- ... --></div>
</div>
```

```css
.stats { display: flex; gap: 12px; margin-bottom: 16px; }
.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--term-border);
    border-radius: 8px;
    padding: 16px; text-align: center;
}
.stat-v {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem; font-weight: 700;
    color: var(--badge-color);
}
.stat-l { font-size: 0.75rem; color: var(--page-dim); margin-top: 2px; }
```

## Layout 5: Comparison Cards

Three side-by-side cards with an analogy box below. Use for "vs" slides or option comparisons.

```html
<div class="slide-body stacked">
    <div class="slide-left">
        <div class="badge">DEEP DIVE</div>
        <div class="slide-title">Three Options</div>
    </div>
    <div class="slide-right">
        <div class="cards-row">
            <div class="mini-card"><h4>Option A</h4><p>Description</p><span class="cl">LABEL</span></div>
            <div class="mini-card"><h4>Option B</h4><p>Description</p><span class="cl">LABEL</span></div>
            <div class="mini-card hl"><h4>Option C</h4><p>Highlighted</p><span class="cl">WINNER</span></div>
        </div>
        <div class="analogy">Analogy text here with <strong>emphasis</strong>.</div>
    </div>
</div>
```

```css
.cards-row { display: flex; gap: 14px; }
.mini-card {
    flex: 1;
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--term-border);
    border-radius: 8px;
    padding: 24px 20px;
    text-align: center;
}
.mini-card.hl {
    border-color: var(--badge-color);
    background: var(--badge-bg);
}
.mini-card h4 { font-size: 0.95rem; font-weight: 600; margin-bottom: 6px; }
.mini-card p { font-size: 0.82rem; color: var(--page-dim); line-height: 1.5; }
.mini-card .cl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    color: var(--badge-color); letter-spacing: 0.1em;
    margin-top: 10px; display: block;
}
```

## Common Elements

### Callout Box
A green-tinted callout for key insights or takeaways. Use below comparison cards or at the bottom of a slide's right column.
```html
<div class="callout">
    <strong>Key insight:</strong> Explanation text here with <strong>emphasis</strong>.
</div>
```
```css
.callout {
    margin-top: 20px;
    padding: 14px 18px;
    background: rgba(126, 200, 126, 0.06);
    border: 1px solid rgba(126, 200, 126, 0.15);
    border-radius: 6px;
    font-size: 0.9rem;
    color: var(--page-dim);
    line-height: 1.7;
}
.callout strong { color: var(--tool-green); }
```

### Use-Case Labels
Small category tags placed above the slide title to classify use-case slides (e.g. Stream vs Poll pattern).
```html
<span class="uc-label uc-stream">STREAM</span>
<span class="uc-label uc-poll">POLL</span>
```
```css
.uc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 600;
    letter-spacing: 0.1em;
    padding: 3px 10px; border-radius: 3px;
    display: inline-block; margin-bottom: 14px;
    width: fit-content;
}
.uc-stream {
    color: var(--tool-cyan);
    border: 1px solid rgba(107, 200, 200, 0.3);
    background: rgba(107, 200, 200, 0.08);
}
.uc-poll {
    color: var(--tool-orange);
    border: 1px solid rgba(212, 160, 107, 0.3);
    background: rgba(212, 160, 107, 0.08);
}
```

Place between the badge and the slide title in `.slide-left`. Create custom variants by copying the pattern with different color variables.

### Badge
```css
.badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.14em;
    color: var(--badge-color);
    border: 1.5px solid var(--badge-border);
    background: var(--badge-bg);
    padding: 5px 16px;
    border-radius: 3px;
    margin-bottom: 24px;
    width: fit-content;
}
```

### Slide Title
```css
.slide-title {
    font-size: 2.6rem; font-weight: 800;
    letter-spacing: -0.035em; line-height: 1.12;
    color: var(--page-text);
}
.slide-title.xl { font-size: 3.2rem; }
```

### Slide Footer
```css
.slide-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--page-muted);
}
```

### Data Table
```css
.dt { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.dt th {
    text-align: left; padding: 10px 14px;
    border-bottom: 1px solid var(--term-border);
    color: var(--page-dim); font-weight: 600;
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.06em;
}
.dt td {
    padding: 9px 14px;
    border-bottom: 1px solid rgba(58,58,66,0.4);
    vertical-align: top;
}
.dt code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; color: var(--tool-blue);
}
```
