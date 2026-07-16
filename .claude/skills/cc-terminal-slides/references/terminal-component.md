# Terminal Component

The terminal window is the primary visual element in slides. It mimics the Claude Code CLI appearance.

## HTML Structure

```html
<div class="terminal">
    <div class="term-header">
        <div class="term-dots">
            <div class="term-dot dot-r"></div>
            <div class="term-dot dot-y"></div>
            <div class="term-dot dot-g"></div>
        </div>
        <span class="term-path">claude &middot; ~/project</span>
    </div>
    <div class="term-body">
        <div class="term-content">
            <!-- Slide content goes here -->
        </div>
        <div class="term-footer">
            <span class="prompt-bottom"><span class="cursor"></span></span>
            <span class="shortcuts">? for shortcuts</span>
        </div>
    </div>
</div>
```

## CSS

```css
.terminal {
    background: var(--term-bg);
    border: 1px solid var(--term-border);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
}
.term-header {
    display: flex;
    align-items: center;
    padding: 14px 20px;
    background: var(--term-header-bg);
    border-bottom: 1px solid var(--term-border);
    flex-shrink: 0;
}
.term-dots { display: flex; gap: 8px; }
.term-dot { width: 12px; height: 12px; border-radius: 50%; }
.dot-r { background: var(--dot-red); }
.dot-y { background: var(--dot-yellow); }
.dot-g { background: var(--dot-green); }
.term-path {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--term-dim);
}
.term-body {
    padding: 28px 32px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.9;
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.term-content { flex: 1; }
.term-footer { margin-top: auto; padding-top: 16px; }
```

## Terminal Text Elements

These classes style text inside `.term-body` to look like real Claude Code output.

### Prompt Line
```html
<span class="p">monitor the deploy and tell me when ready</span>
```
```css
.p {
    display: block;
    background: var(--prompt-bg);
    padding: 7px 14px;
    border-radius: 5px;
    margin-bottom: 18px;
    color: var(--term-text);
}
.p::before {
    content: '\276F  '; /* ❯ followed by two spaces */
    color: var(--term-dim);
}
```

### Bullet Lines (Tool Calls)
```html
<span class="ln"><span class="b c-tool">Monitor</span><span class="c-dim">("deploy status")</span></span>
```
```css
.b::before { content: '\23FA  '; font-size: 0.65em; vertical-align: middle; }
.b { color: var(--term-text); }
```

### Sub-Results (Tree Connector)
```html
<span class="sub c-dim">Monitor started · task brovgltib · timeout 300s</span>
```
```css
.sub { padding-left: 24px; display: block; }
.sub::before { content: '\2514\2500 '; color: var(--term-muted); }
```

### Lines and Spacing
```html
<span class="ln">regular line of text</span>
<span class="gap"></span>    <!-- 12px gap -->
<span class="sgap"></span>   <!-- 22px section gap -->
```
```css
.ln { display: block; }
.gap { display: block; height: 12px; }
.sgap { display: block; height: 22px; }
```

### Color Classes
```css
.c-tool { color: var(--tool-blue); }
.c-green { color: var(--tool-green); }
.c-orange { color: var(--tool-orange); }
.c-red { color: var(--tool-red); }
.c-pink { color: var(--tool-pink); }
.c-purple { color: var(--tool-purple); }
.c-cyan { color: var(--tool-cyan); }
.c-yellow { color: var(--tool-yellow); }
.c-dim { color: var(--term-dim); }
.c-muted { color: var(--term-muted); }
.c-text { color: var(--term-text); }
```

### Response Block (Assistant Message)
```html
<span class="resp">The deploy is ready. All systems go.</span>
```
```css
.resp {
    display: block;
    background: rgba(126, 200, 126, 0.06);
    border-left: 2px solid rgba(126, 200, 126, 0.2);
    padding: 10px 16px;
    border-radius: 0 4px 4px 0;
    margin: 12px 0;
    color: var(--term-text);
    font-size: 0.76rem;
    line-height: 1.8;
}
```

### Cursor and Bottom Prompt
```html
<span class="prompt-bottom"><span class="cursor"></span></span>
<span class="shortcuts">? for shortcuts</span>
```
```css
.cursor {
    display: inline-block;
    width: 8px; height: 15px;
    background: var(--term-dim);
    vertical-align: text-bottom;
    animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
.prompt-bottom { display: block; margin-top: 12px; }
.prompt-bottom::before { content: '\276F  '; color: var(--term-dim); }
.shortcuts { display: block; color: var(--term-muted); font-size: 0.7rem; margin-top: 12px; }
```

### Two-Column Layout
```html
<div class="term-cols">
    <div class="term-col">
        <span class="term-col-label c-cyan">LEFT LABEL</span>
        <span class="ln">Left column content</span>
    </div>
    <div class="term-col" style="border-left:1px solid var(--term-border); padding-left:32px;">
        <span class="term-col-label c-orange">RIGHT LABEL</span>
        <span class="ln">Right column content</span>
    </div>
</div>
```
```css
.term-cols { display: flex; gap: 32px; }
.term-col { flex: 1; }
.term-col-label {
    font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.1em; margin-bottom: 12px;
    display: block;
}
```

Use for side-by-side comparisons inside the terminal (e.g. Stream vs Poll, With vs Without). The right column gets a left border as a visual divider.

## Tabbed Terminal

When comparing 2-4 approaches to the same task (e.g. "three ways to run a command"), use tabs above a single terminal instead of side-by-side cards or multiple terminals. Tabs keep the terminal full-width and readable while letting the viewer click between options.

**Why tabs over cards:** Cards force content into narrow columns that are unreadable at presentation/video distance. A tabbed terminal gives each option the full terminal width and makes the comparison interactive — the viewer clicks to see each approach using the same scenario, making the difference visceral.

**Critical: use the same example across all tabs.** If you're comparing approaches A, B, and C, show them all doing the exact same task. Different examples per tab obscure the comparison — viewers can't tell if the difference is the approach or the task.

### HTML Structure
```html
<div class="mode-tabs">
    <div class="mode-tab active" data-tab="a">Option A</div>
    <div class="mode-tab" data-tab="b">Option B</div>
    <div class="mode-tab" data-tab="c">Option C</div>
</div>
<div class="terminal">
    <div class="term-header"><!-- dots + path --></div>
    <div class="term-body">
        <div class="tab-panel active" data-panel="a">
            <div class="term-content">
                <!-- Option A terminal content -->
            </div>
        </div>
        <div class="tab-panel" data-panel="b">
            <div class="term-content">
                <!-- Option B terminal content -->
            </div>
        </div>
        <div class="tab-panel" data-panel="c">
            <div class="term-content">
                <!-- Option C terminal content -->
            </div>
        </div>
        <div class="term-footer"><!-- cursor + shortcuts --></div>
    </div>
</div>
```

### CSS
```css
.mode-tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.mode-tab {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.06em;
    padding: 8px 20px; border-radius: 6px;
    border: 1px solid var(--term-border);
    background: rgba(255,255,255,0.025);
    color: var(--page-dim); cursor: pointer;
    transition: all 0.2s;
}
.mode-tab:hover { border-color: var(--page-dim); color: var(--page-text); }
.mode-tab.active {
    border-color: var(--badge-color);
    background: var(--badge-bg);
    color: var(--badge-color);
}
.tab-panel { display: none; }
.tab-panel.active { display: block; }
```

### JavaScript
Add this to the navigation script. The `stopPropagation()` is critical — without it, tab clicks trigger slide navigation.
```javascript
document.querySelectorAll('.mode-tab').forEach(tab => {
    tab.addEventListener('click', e => {
        e.stopPropagation();
        const t = tab.dataset.tab;
        document.querySelectorAll('.mode-tab').forEach(x => x.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(x => x.classList.remove('active'));
        tab.classList.add('active');
        document.querySelector(`.tab-panel[data-panel="${t}"]`).classList.add('active');
    });
});
```

### When to Use Tabs vs Other Layouts

| Scenario | Use |
|----------|-----|
| Comparing 2-4 approaches to the **same task** | Tabbed terminal |
| Comparing 2 things side-by-side in one view | Two-column terminal (`.term-cols`) |
| Comparing 3+ options with short descriptions | Comparison cards (Layout 5) |
| Showing before/after or with/without | Two-column terminal (`.term-cols`) |

## Usage Notes

- The terminal flexes to fill available height — it should dominate the slide's right side.
- The `term-path` in the header should reflect the context: `claude · ~/project` for user-facing demos, `internals · pipeline` for technical deep dives, `binary · extracted` for reverse-engineering content.
- Include `term-footer` with cursor + shortcuts on slides that represent interactive sessions. Omit cursor on slides showing static code/data.
- The `⏺` bullet (U+23FA) matches the macOS Claude Code UI. It renders smaller via `font-size: 0.65em`.
