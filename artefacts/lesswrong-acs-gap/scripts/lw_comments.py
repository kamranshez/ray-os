#!/usr/bin/env python3
"""Comment lane: pull anchor-matching LW comments (incl. Shortform) via /api/search,
then rescore locally. Shortform is where practitioners post quick technique notes and is
invisible to any post-level scan."""
import json, sys, time, datetime, urllib.request, re
sys.path.insert(0, ".")
from lw_pipeline import HC, SC, VO

URL="https://www.lesswrong.com/api/search"
# Query with the hard tool names directly — full-text, so we cast wide then rescore locally.
QUERIES=["claude code","codex cli","cursor agent","AGENTS.md","CLAUDE.md","subagent",
 "coding agent","agentic coding","vibe coding","MCP server","slash command","git worktree",
 "agent harness","scaffold agent","context engineering","aider copilot devin windsurf",
 "claude code workflow tips","how I use claude code","prompt for coding agent",
 "agent skills hooks","parallel agents tmux","plan mode","agent sdk","token budget compaction"]

def search(q, page, after_ms, hpp=500):
    body=json.dumps([{"indexName":"comments","params":{"query":q,"hitsPerPage":hpp,"page":page,
        "numericFilters":[f"publicDateMs>{after_ms}"]}}]).encode()
    r=urllib.request.Request(URL,data=body,headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
    for i in range(3):
        try:
            with urllib.request.urlopen(r,timeout=90) as f: return json.loads(f.read())[0]
        except Exception:
            if i==2: raise
            time.sleep(2)

after=sys.argv[1] if len(sys.argv)>1 else "2026-05-20"
after_ms=int(datetime.datetime.fromisoformat(after).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)
raw={}
for q in QUERIES:
    for pg in (0,1):
        r=search(q,pg,after_ms)
        for h in r["hits"]: raw[h["objectID"]]=h
        if pg+1>=r["nbPages"]: break
    time.sleep(0.2)
print(f"pulled {len(raw)} unique comments in window")

out=[]
for h in raw.values():
    b=h.get("body") or ""
    hn=sum(1 for rx,_ in HC if rx.search(b)); hw=sum(w*len(rx.findall(b)) for rx,w in HC)
    sn=sum(1 for rx,_ in SC if rx.search(b)); sw=sum(w*len(rx.findall(b)) for rx,w in SC)
    v=sum(1 for rx in VO if rx.search(b)); words=max(len(b.split()),1)
    # gate: needs substance, not just a passing mention
    if words<50: continue
    if hn<2 and not (hn>=1 and words>=150): continue
    dens=(hw+0.6*sw)/max(words,200)*1000        # 200-word floor: short comments can't spike
    substance=min(words/150.0,4.0)              # reward actual writeups over one-liners
    out.append(dict(id=h["objectID"], postId=h["postId"], postTitle=h.get("postTitle"),
        url=f"https://www.lesswrong.com/posts/{h['postId']}/{h.get('postSlug')}?commentId={h['objectID']}",
        karma=h["baseScore"], date=h["postedAt"][:10], author=h.get("authorDisplayName"),
        words=words, hard_n=hn, voice=v, density=round(dens,1),
        shortform=bool(re.search(r"shortform",(h.get("postTitle") or ""),re.I)),
        score=round(1.2*dens+6*hn+3*v+0.4*min(h["baseScore"],60)+8*substance,1), body=b))
out.sort(key=lambda x:-x["score"])
json.dump(out,open("comment_shortlist.json","w"),indent=1)
print(f"comment shortlist: {len(out)} (shortform: {sum(1 for x in out if x['shortform'])})")
