#!/usr/bin/env python3
"""Render the outlier-mining workflow result into a navigable HTML artifact.

Usage:
    python3 build_outlier_html.py --result <workflow-result.json> --out <outlier-report.html>

The HTML has pin buttons on every insight, a sidebar pin tray with persistence
in localStorage, and two export actions (Markdown download + copy to clipboard).
"""
import argparse
import html
import json
from pathlib import Path


def esc(s):
    return html.escape(s or "", quote=True)


def build_html(data):
    report = data["report"]
    stats = data["stats"]
    topic = data.get("topic", "Topic")
    consensus = data.get("consensus_thesis", "")

    def headline_html():
        out = []
        for i, h in enumerate(report["headline"], 1):
            pin_payload = json.dumps({
                "type": "headline", "idea": h["idea"], "author": h["author"],
                "quote": h["quote"], "why": h["why_it_matters"],
            })
            out.append(f"""
            <article class="card hero" data-pin='{esc(pin_payload)}'>
              <div class="num">{i}</div>
              <h3>{esc(h['idea'])}</h3>
              <div class="who">@{esc(h['author'])}</div>
              <blockquote>{esc(h['quote'])}</blockquote>
              <div class="why">{esc(h['why_it_matters'])}</div>
              <button class="pin-btn">☆ Pin</button>
            </article>
            """)
        return "\n".join(out)

    def themes_html():
        out = []
        for i, t in enumerate(report["themes"], 1):
            supports = []
            for s in t["supports"]:
                pin_payload = json.dumps({
                    "type": "support", "theme": t["name"], "author": s["author"],
                    "idea": s["idea"], "quote": s["quote"],
                })
                supports.append(f"""
                <li class="support" data-pin='{esc(pin_payload)}'>
                  <div class="row">
                    <span class="who">@{esc(s['author'])}</span>
                    <button class="pin-btn small">☆</button>
                  </div>
                  <div class="idea">{esc(s['idea'])}</div>
                  <blockquote>{esc(s['quote'])}</blockquote>
                </li>
                """)
            out.append(f"""
            <article class="card theme">
              <h3><span class="theme-n">{i}</span> {esc(t['name'])}</h3>
              <p class="oneliner">{esc(t['one_liner'])}</p>
              <ul class="supports">{''.join(supports)}</ul>
            </article>
            """)
        return "\n".join(out)

    def models_html():
        out = []
        for m in report["mental_models"]:
            pin_payload = json.dumps({
                "type": "model", "framing": m["framing"], "author": m["author"],
            })
            out.append(f"""
            <li class="card model" data-pin='{esc(pin_payload)}'>
              <blockquote>{esc(m['framing'])}</blockquote>
              <div class="who">@{esc(m['author'])}</div>
              <button class="pin-btn micro">☆</button>
            </li>
            """)
        return "\n".join(out)

    def objections_html():
        out = []
        for o in report["sharpest_objections"]:
            pin_payload = json.dumps({
                "type": "objection", "objection": o["objection"],
                "author": o["author"], "quote": o["quote"],
            })
            out.append(f"""
            <article class="card objection" data-pin='{esc(pin_payload)}'>
              <h3>{esc(o['objection'])}</h3>
              <div class="who">@{esc(o['author'])}</div>
              <blockquote>{esc(o['quote'])}</blockquote>
              <button class="pin-btn">☆ Pin</button>
            </article>
            """)
        return "\n".join(out)

    def tooling_html():
        out = []
        for t in report["specific_tooling"]:
            pin_payload = json.dumps({
                "type": "tooling", "tool": t["name"],
                "what_it_is": t["what_it_is"], "author": t["author"],
            })
            out.append(f"""
            <li class="card tool" data-pin='{esc(pin_payload)}'>
              <div class="tool-name">{esc(t['name'])}</div>
              <div class="tool-desc">{esc(t['what_it_is'])}</div>
              <div class="who">via @{esc(t['author'])}</div>
              <button class="pin-btn micro">☆</button>
            </li>
            """)
        return "\n".join(out)

    return TEMPLATE.format(
        topic=esc(topic),
        consensus=esc(consensus),
        anchors=stats.get("anchors", 0),
        extracted=stats.get("candidates_extracted", 0),
        verified=stats.get("candidates_verified", 0),
        rejected=stats.get("candidates_rejected", 0),
        n_themes=len(report.get("themes", [])),
        n_models=len(report.get("mental_models", [])),
        n_objections=len(report.get("sharpest_objections", [])),
        n_tooling=len(report.get("specific_tooling", [])),
        headline=headline_html(),
        themes=themes_html(),
        models=models_html(),
        objections=objections_html(),
        tooling=tooling_html(),
    )


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Outlier Insights — {topic}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root {{
    --bg: #0d1117;
    --panel: #161b22;
    --panel-2: #1c2128;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --muted-2: #b1bac4;
    --accent: #f0a020;
    --accent-2: #ffd166;
    --pinned-bg: rgba(240,160,32,0.08);
    --pinned-bd: #f0a020;
    --danger: #f04545;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, "Inter", "Segoe UI", sans-serif; font-size: 15px; line-height: 1.55; }}
  body {{ display: grid; grid-template-columns: 1fr 320px; min-height: 100vh; }}
  main {{ padding: 40px 48px 120px; max-width: 980px; }}
  @media (max-width: 1000px) {{
    body {{ grid-template-columns: 1fr; }}
    main {{ padding: 24px 20px; }}
    aside {{ position: relative !important; height: auto !important; border-left: none !important; border-top: 1px solid var(--border); }}
  }}

  header.page {{ margin-bottom: 40px; }}
  h1 {{ font-size: 36px; line-height: 1.1; margin: 0 0 8px; letter-spacing: -0.02em; font-weight: 700; }}
  .subtitle {{ color: var(--muted-2); margin: 0 0 20px; max-width: 640px; }}
  .consensus {{
    background: var(--panel); border: 1px solid var(--border);
    border-left: 3px solid var(--accent); padding: 12px 16px;
    border-radius: 6px; margin: 16px 0 20px; font-size: 14px; color: var(--muted-2);
  }}
  .consensus strong {{ color: var(--accent-2); display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }}

  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; margin-bottom: 16px; }}
  .stat {{ background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; }}
  .stat .n {{ font-size: 22px; font-weight: 700; color: var(--accent-2); }}
  .stat .l {{ color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }}

  nav.section-nav {{ display: flex; gap: 6px; flex-wrap: wrap; padding: 10px; background: var(--panel); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 40px; }}
  nav.section-nav a {{ color: var(--muted-2); text-decoration: none; padding: 4px 12px; border-radius: 12px; font-size: 13px; border: 1px solid transparent; }}
  nav.section-nav a:hover {{ color: var(--accent); border-color: var(--accent); }}

  section {{ margin-bottom: 64px; scroll-margin-top: 16px; }}
  section h2 {{ font-size: 24px; margin: 0 0 8px; font-weight: 700; letter-spacing: -0.01em; }}
  section .section-blurb {{ color: var(--muted); margin: 0 0 24px; font-size: 14px; max-width: 640px; }}

  /* Cards (shared) */
  .card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 18px 22px; position: relative; margin-bottom: 12px;
  }}
  .card.pinned {{ background: var(--pinned-bg); border-color: var(--pinned-bd); }}
  .card .who {{ color: var(--accent-2); font-size: 12px; font-weight: 600; }}
  .card blockquote {{ margin: 8px 0; padding: 8px 12px; background: rgba(0,0,0,0.2); border-left: 2px solid var(--border); border-radius: 4px; font-style: italic; color: var(--muted-2); font-size: 13px; }}

  /* Hero (top 5) */
  .hero {{ padding: 24px 28px; border-left: 4px solid var(--accent); }}
  .hero .num {{ position: absolute; top: 14px; right: 20px; font-size: 48px; font-weight: 900; color: rgba(240,160,32,0.18); line-height: 1; }}
  .hero h3 {{ font-size: 19px; margin: 0 0 8px; line-height: 1.35; padding-right: 56px; font-weight: 700; }}
  .hero blockquote {{ font-size: 14px; margin-top: 12px; }}
  .hero .why {{ font-size: 13px; color: var(--muted-2); margin-top: 10px; }}

  /* Themes */
  .theme h3 {{ font-size: 18px; margin: 0 0 4px; display: flex; gap: 10px; align-items: baseline; }}
  .theme .theme-n {{ font-size: 13px; color: var(--accent); font-weight: 700; }}
  .theme .oneliner {{ color: var(--muted-2); margin: 0 0 16px; font-size: 13px; }}
  .theme .supports {{ list-style: none; margin: 0; padding: 0; }}
  .support {{ background: var(--panel-2); border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; position: relative; }}
  .support.pinned {{ background: var(--pinned-bg); border-color: var(--pinned-bd); }}
  .support .row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .support .idea {{ font-size: 13px; font-weight: 500; margin-bottom: 4px; }}
  .support blockquote {{ margin: 4px 0 0; padding: 0 0 0 10px; background: none; font-size: 12px; }}

  /* Models */
  .models-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 10px; list-style: none; padding: 0; margin: 0; }}
  .model {{ padding: 14px 16px; margin: 0; }}
  .model blockquote {{ margin: 0 0 6px; padding: 0; background: none; border: none; font-size: 13px; }}
  .model .who {{ font-size: 11px; }}

  /* Objections */
  .objection {{ border-left: 3px solid #d04848; }}
  .objection h3 {{ font-size: 15px; margin: 0 0 4px; line-height: 1.4; }}

  /* Tooling */
  .tools-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px; list-style: none; padding: 0; margin: 0; }}
  .tool {{ padding: 12px 14px; margin: 0; }}
  .tool-name {{ font-weight: 700; color: var(--accent); font-size: 14px; }}
  .tool-desc {{ color: var(--muted-2); font-size: 12px; margin: 4px 0; }}
  .tool .who {{ font-size: 11px; color: var(--muted); }}

  /* Pin buttons */
  .pin-btn {{
    background: var(--panel-2); border: 1px solid var(--border); color: var(--muted);
    padding: 5px 12px; border-radius: 5px; cursor: pointer; font-size: 11px;
    margin-top: 8px; transition: all 0.12s;
  }}
  .pin-btn.small {{ padding: 2px 8px; font-size: 11px; margin: 0; }}
  .pin-btn.micro {{ position: absolute; top: 8px; right: 8px; padding: 2px 6px; font-size: 10px; margin: 0; background: transparent; border-color: transparent; }}
  .pin-btn:hover {{ color: var(--accent); border-color: var(--accent); }}
  .pinned .pin-btn {{ color: var(--accent); border-color: var(--accent); background: rgba(240,160,32,0.1); }}

  /* Sidebar */
  aside {{ position: sticky; top: 0; height: 100vh; background: var(--panel); border-left: 1px solid var(--border); padding: 20px; overflow-y: auto; }}
  aside h2 {{ margin: 0 0 4px; font-size: 16px; }}
  aside .sub {{ color: var(--muted); font-size: 12px; margin-bottom: 14px; }}
  .pin-item {{
    background: var(--panel-2); border: 1px solid var(--border); border-left: 3px solid var(--accent);
    border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 12px; position: relative;
  }}
  .pin-item .x-btn {{ position: absolute; top: 4px; right: 6px; background: none; border: none; color: var(--muted); cursor: pointer; font-size: 14px; line-height: 1; }}
  .pin-item .x-btn:hover {{ color: var(--danger); }}
  .pin-item .tag {{ display: inline-block; font-size: 9px; background: rgba(0,0,0,0.3); padding: 1px 6px; border-radius: 3px; color: var(--accent-2); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.06em; }}
  .pin-item .author {{ color: var(--accent-2); font-size: 11px; font-weight: 600; }}
  .pin-item .q {{ color: var(--muted-2); font-style: italic; font-size: 11px; margin-top: 4px; }}
  .empty {{ color: var(--muted); font-style: italic; font-size: 12px; }}
  .sb-actions {{ display: grid; gap: 6px; margin-top: 12px; }}
  .sb-btn {{ padding: 9px; border-radius: 6px; cursor: pointer; font-weight: 600; border: 1px solid var(--border); background: var(--panel-2); color: var(--text); font-size: 13px; }}
  .sb-btn.primary {{ background: var(--accent); color: #0d1117; border-color: var(--accent); }}
  .sb-btn.primary:hover {{ background: var(--accent-2); }}
  .sb-btn:not(.primary):hover {{ border-color: var(--accent); color: var(--accent); }}
  .sb-btn.danger:hover {{ color: var(--danger); border-color: var(--danger); }}
  .toast {{
    position: fixed; bottom: 20px; right: 20px; background: var(--accent); color: #0d1117;
    padding: 10px 16px; border-radius: 6px; font-weight: 600; font-size: 13px;
    opacity: 0; transform: translateY(10px); transition: all 0.2s; pointer-events: none;
    z-index: 1000;
  }}
  .toast.show {{ opacity: 1; transform: translateY(0); }}

  ::selection {{ background: var(--accent); color: #0d1117; }}
</style>
</head>
<body>

<main>
  <header class="page">
    <h1>Outlier insights — {topic}</h1>
    <p class="subtitle">Non-obvious takes mined from the engagement and adversarially verified. The consensus thesis was deliberately filtered out — these are the takes the consensus doesn't tell you.</p>

    <div class="consensus">
      <strong>Consensus thesis (filtered out)</strong>
      {consensus}
    </div>

    <div class="stats">
      <div class="stat"><div class="n">{anchors}</div><div class="l">Anchors</div></div>
      <div class="stat"><div class="n">{extracted}</div><div class="l">Candidates</div></div>
      <div class="stat"><div class="n">{verified}</div><div class="l">Verified</div></div>
      <div class="stat"><div class="n">{rejected}</div><div class="l">Rejected</div></div>
      <div class="stat"><div class="n">{n_themes}</div><div class="l">Themes</div></div>
    </div>
  </header>

  <nav class="section-nav">
    <a href="#headline">★ The 5</a>
    <a href="#themes">{n_themes} themes</a>
    <a href="#models">Mental models ({n_models})</a>
    <a href="#objections">Objections ({n_objections})</a>
    <a href="#tooling">Tooling ({n_tooling})</a>
  </nav>

  <section id="headline">
    <h2>The 5 outliers most worth anchoring around</h2>
    <p class="section-blurb">The takes a thoughtful reader would say "huh, I hadn't thought of that" about.</p>
    {headline}
  </section>

  <section id="themes">
    <h2>Themes</h2>
    <p class="section-blurb">Clusters of related outliers. Use as section structures.</p>
    {themes}
  </section>

  <section id="models">
    <h2>Mental models worth stealing verbatim</h2>
    <p class="section-blurb">One-line framings to drop in as-is.</p>
    <ul class="models-grid">{models}</ul>
  </section>

  <section id="objections">
    <h2>Sharpest objections (steelmanned)</h2>
    <p class="section-blurb">What pushes back on the consensus thesis. Address these or read as naive.</p>
    {objections}
  </section>

  <section id="tooling">
    <h2>Specific tooling & patterns named</h2>
    <p class="section-blurb">Concrete things — drop these for credibility.</p>
    <ul class="tools-grid">{tooling}</ul>
  </section>
</main>

<aside>
  <h2>Pins <span id="pin-count">(0)</span></h2>
  <div class="sub">Click ☆ to pin. Persists in this browser.</div>
  <div id="pins"><div class="empty">No pins yet.</div></div>
  <div class="sb-actions">
    <button class="sb-btn primary" id="copy">📋 Copy Markdown</button>
    <button class="sb-btn" id="export">⬇ Download .md</button>
    <button class="sb-btn danger" id="clear">Clear all</button>
  </div>
</aside>

<div class="toast" id="toast">Copied!</div>

<script>
const STORAGE_KEY = "x-thread-outlier-pins-v1";
let pins = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");

function save() {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(pins)); }}
function escHtml(s) {{ return (s||'').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c])); }}
function keyOf(p) {{ return [p.type, p.author||'', p.idea||p.framing||p.objection||p.tool||'', (p.quote||'').slice(0,40)].join('|'); }}

function renderPins() {{
  document.getElementById('pin-count').textContent = `(${{pins.length}})`;
  const el = document.getElementById('pins');
  if (!pins.length) {{ el.innerHTML = '<div class="empty">No pins yet.</div>'; }} else {{
    el.innerHTML = pins.map((p, i) => {{
      const main = p.idea || p.framing || p.objection || p.tool || '';
      const q = p.quote ? `<div class="q">"${{escHtml(p.quote.slice(0,140))}}${{p.quote.length>140?'…':''}}"</div>` : '';
      return `<div class="pin-item">
        <button class="x-btn" data-i="${{i}}">×</button>
        <div class="tag">${{p.type}}</div>
        <div class="author">@${{escHtml(p.author||'?')}}</div>
        <div>${{escHtml(main)}}</div>
        ${{q}}
      </div>`;
    }}).join('');
  }}
  // Sync card pinned-state
  document.querySelectorAll('[data-pin]').forEach(card => {{
    const p = JSON.parse(card.dataset.pin);
    const isPinned = pins.some(x => keyOf(x) === keyOf(p));
    card.classList.toggle('pinned', isPinned);
    const btn = card.querySelector('.pin-btn');
    if (btn) {{
      const isSmall = btn.classList.contains('small') || btn.classList.contains('micro');
      btn.textContent = isPinned ? (isSmall ? '★' : '★ Pinned') : (isSmall ? '☆' : '☆ Pin');
    }}
  }});
}}

function buildMarkdown() {{
  const lines = ['# Pinned outlier insights', '', `Captured ${{pins.length}} pins.`, ''];
  pins.forEach((p, i) => {{
    lines.push(`## ${{i+1}}. [${{p.type}}] @${{p.author||'?'}}`);
    lines.push('');
    const main = p.idea || p.framing || p.objection || p.tool || '';
    if (main) lines.push(`**${{main}}**`);
    if (p.what_it_is) {{ lines.push(''); lines.push(p.what_it_is); }}
    if (p.quote) {{ lines.push(''); lines.push(`> ${{p.quote}}`); }}
    if (p.why) {{ lines.push(''); lines.push(`_${{p.why}}_`); }}
    if (p.theme) {{ lines.push(''); lines.push(`Theme: _${{p.theme}}_`); }}
    lines.push(''); lines.push('---'); lines.push('');
  }});
  return lines.join('\n');
}}

function toast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1600);
}}

document.addEventListener('click', e => {{
  // Pin/unpin
  const card = e.target.closest('[data-pin]');
  if (card && (e.target.closest('.pin-btn') || e.target === card)) {{
    if (e.target.closest('.x-btn')) return; // sidebar X handles itself
    const p = JSON.parse(card.dataset.pin);
    const k = keyOf(p);
    const idx = pins.findIndex(x => keyOf(x) === k);
    if (idx >= 0) pins.splice(idx, 1); else pins.push(p);
    save(); renderPins();
    return;
  }}
  // Sidebar remove
  const x = e.target.closest('.x-btn[data-i]');
  if (x) {{
    pins.splice(+x.dataset.i, 1);
    save(); renderPins();
  }}
}});

document.getElementById('clear').addEventListener('click', () => {{
  if (!pins.length) return;
  if (!confirm(`Clear all ${{pins.length}} pins?`)) return;
  pins = []; save(); renderPins();
}});

document.getElementById('export').addEventListener('click', () => {{
  if (!pins.length) {{ toast('No pins yet'); return; }}
  const blob = new Blob([buildMarkdown()], {{ type: 'text/markdown' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'outlier-pins.md';
  a.click();
  URL.revokeObjectURL(a.href);
  toast('Downloaded outlier-pins.md');
}});

document.getElementById('copy').addEventListener('click', async () => {{
  if (!pins.length) {{ toast('No pins yet'); return; }}
  const md = buildMarkdown();
  try {{
    await navigator.clipboard.writeText(md);
    toast(`Copied ${{pins.length}} pin${{pins.length===1?'':'s'}}`);
  }} catch (err) {{
    // fallback
    const ta = document.createElement('textarea');
    ta.value = md;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    toast('Copied (fallback)');
  }}
}});

renderPins();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Render outlier workflow result to HTML.")
    ap.add_argument("--result", required=True, help="Path to workflow-result.json")
    ap.add_argument("--out", required=True, help="Path to write the HTML file")
    a = ap.parse_args()

    data = json.loads(Path(a.result).read_text(encoding="utf-8"))
    out_html = build_html(data)
    Path(a.out).write_text(out_html, encoding="utf-8")
    print(f"Wrote {a.out} ({Path(a.out).stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
