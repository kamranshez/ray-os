#!/usr/bin/env python3
"""Build an interactive HTML "idea picker" from a JSON of ideas.

Usage:
    python3 build_picker.py ideas.json out.html

The JSON shape (see references/report-format.md):
    {
      "title": "...", "subtitle": "...",
      "sections": [
        {"name": "...", "items": [
          {"label": "#1", "title": "...", "desc": "...",
           "tags": [{"text": "top", "kind": "hot"}],
           "links": [{"text": "Source", "url": "https://...", "kind": "src"},
                     {"text": "Video", "url": "https://...", "kind": "yt"}]}
        ]}
      ]
    }

Produces a self-contained dark-mode page where:
  - clicking a card toggles selection,
  - clicking a link chip opens it WITHOUT toggling the card,
  - "Copy selection" auto-fills a textarea the user pastes back.

The tool emits no em/en dashes (a firm style rule for Ray's content): any in the
input are converted to plain hyphens.
"""
import json
import sys
import html


def clean(s):
    if s is None:
        return ""
    return str(s).replace(" — ", " - ").replace("—", "-").replace("–", "-")


CSS = """
:root{--bg:#0e1116;--panel:#161b22;--panel2:#1c232d;--line:#2a323d;--txt:#e6edf3;--mut:#9aa7b4;--acc:#6ee7b7;--acc2:#7aa2f7;--sel:#13351f;--selln:#2f7d52;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding-bottom:130px}
header{position:sticky;top:0;z-index:5;background:linear-gradient(180deg,#0e1116 70%,rgba(14,17,22,0));padding:22px 24px 12px}
h1{margin:0 0 4px;font-size:20px}.sub{color:var(--mut);font-size:13px}
.wrap{max-width:920px;margin:0 auto;padding:0 24px}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.btn{background:var(--panel2);border:1px solid var(--line);color:var(--txt);padding:7px 12px;border-radius:8px;cursor:pointer;font-size:13px}.btn:hover{border-color:var(--acc2)}
.secttl{margin:26px 0 8px;font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--acc)}
.card{display:flex;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0;cursor:pointer;transition:.12s}
.card:hover{border-color:#3b475a}.card.sel{background:var(--sel);border-color:var(--selln)}
.card input{margin-top:3px;width:18px;height:18px;accent-color:var(--acc);flex:0 0 auto;pointer-events:none}
.body{flex:1;min-width:0}.ttl{font-weight:650;font-size:15px}.num{color:var(--mut);font-weight:600;margin-right:6px}
.desc{color:var(--mut);font-size:13.5px;margin-top:4px}
.links{margin-top:9px;display:flex;flex-wrap:wrap;gap:6px}
.lnk{display:inline-flex;align-items:center;gap:4px;background:#11202e;border:1px solid #244055;color:#9cc4f7;border-radius:7px;padding:3px 9px;font-size:12px;text-decoration:none;cursor:pointer}
.lnk:hover{background:#16293a;border-color:#3a6fa0}
.lnk.src{background:#11261c;border-color:#2c5a3f;color:#8fe0b4}.lnk.src:hover{background:#163524;border-color:#3f8059}
.lnk.yt{background:#2a1416;border-color:#5e2a2e;color:#f2a8ad}.lnk.yt:hover{background:#371a1d;border-color:#84393f}
.tag{display:inline-block;background:#1f2630;border:1px solid var(--line);color:#a9b6c4;border-radius:999px;padding:1px 8px;font-size:11px;margin-right:6px}
.tag.hot{background:#36240f;border-color:#7d5a2f;color:#f0c089}.tag.seq{background:#16263a;border-color:#2f5b8d;color:#9cc4f7}
footer{position:fixed;bottom:0;left:0;right:0;background:#0b0e12;border-top:1px solid var(--line);padding:12px 24px}
.footin{max-width:920px;margin:0 auto;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.count{font-weight:700}.count b{color:var(--acc)}
textarea{flex:1;min-width:240px;height:64px;background:#11161d;color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:8px;font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;resize:vertical}
.go{background:var(--acc);color:#06231a;font-weight:700;border:none}.go:hover{filter:brightness(1.08)}
.hint{color:var(--mut);font-size:12px;flex-basis:100%}
"""

JS = r"""
const DATA = __DATA__;
const list = document.getElementById('list');
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function section(name){const h=document.createElement('div');h.className='secttl';h.textContent=name;list.appendChild(h);}
function card(it){
  const d=document.createElement('div');d.className='card';
  d.dataset.label=it.label||'';d.dataset.title=it.title||'';
  const tags=(it.tags||[]).map(t=>'<span class="tag '+(t.kind||'')+'">'+esc(t.text)+'</span>').join('');
  const links=(it.links||[]).map(l=>'<a class="lnk '+(l.kind||'src')+'" href="'+l.url+'" target="_blank" rel="noopener">'+((l.kind==='yt')?'▶ ':'')+esc(l.text)+'</a>').join('');
  d.innerHTML='<input type="checkbox"><div class="body"><div class="ttl"><span class="num">'+esc(it.label||'')+'</span>'+esc(it.title)+'</div>'+
    tags+'<div class="desc">'+esc(it.desc)+'</div>'+(links?'<div class="links">'+links+'</div>':'')+'</div>';
  const cb=d.querySelector('input');
  d.addEventListener('click',e=>{if(e.target.closest('a'))return;cb.checked=!cb.checked;d.classList.toggle('sel',cb.checked);update();});
  list.appendChild(d);
}
(DATA.sections||[]).forEach(s=>{section(s.name);(s.items||[]).forEach(card);});
function update(){
  const sel=[...document.querySelectorAll('.card')].filter(c=>c.querySelector('input').checked);
  document.getElementById('c').textContent=sel.length;
  document.getElementById('out').value=sel.length?('Ideas I want to pursue ('+sel.length+'):\n'+sel.map(c=>'- '+c.dataset.label+' '+c.dataset.title).join('\n')):'';
}
function all(v){document.querySelectorAll('.card').forEach(c=>{c.querySelector('input').checked=v;c.classList.toggle('sel',v);});update();}
function copy(ev){update();const t=document.getElementById('out');if(!t.value){t.value='(nothing selected yet)';return;}t.select();try{document.execCommand('copy');}catch(e){}const b=ev.target,o=b.textContent;b.textContent='Copied! Paste it back to me';setTimeout(()=>b.textContent=o,1800);}
window._all=all;window._copy=copy;update();
"""


def build(data):
    title = clean(data.get("title", "Idea Picker"))
    sub = clean(data.get("subtitle", ""))
    # clean every text field in the data before embedding
    for sec in data.get("sections", []):
        sec["name"] = clean(sec.get("name"))
        for it in sec.get("items", []):
            it["title"] = clean(it.get("title"))
            it["desc"] = clean(it.get("desc"))
            for t in it.get("tags", []):
                t["text"] = clean(t.get("text"))
            for l in it.get("links", []):
                l["text"] = clean(l.get("text"))
    js = JS.replace("__DATA__", json.dumps(data))
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body>
<header><div class="wrap"><h1>{html.escape(title)}</h1><div class="sub">{html.escape(sub)}</div>
<div class="toolbar"><button class="btn" onclick="_all(true)">Select all</button>
<button class="btn" onclick="_all(false)">Clear</button></div></div></header>
<div class="wrap" id="list"></div>
<footer><div class="footin"><div class="count"><b id="c">0</b> selected</div>
<button class="btn go" onclick="_copy(event)">Copy selection</button>
<textarea id="out" placeholder="Your selection appears here..." readonly></textarea>
<div class="hint">Click a card to toggle it. Clicking a link chip opens it and will not toggle the card. The box auto-fills - paste it back into the chat.</div>
</div></footer><script>{js}</script></body></html>"""


def main():
    if len(sys.argv) < 3:
        print("usage: build_picker.py <ideas.json> <out.html>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    out = build(data)
    with open(sys.argv[2], "w") as f:
        f.write(out)
    n = sum(len(s.get("items", [])) for s in data.get("sections", []))
    print(f"wrote {sys.argv[2]} ({n} items)")


if __name__ == "__main__":
    main()
