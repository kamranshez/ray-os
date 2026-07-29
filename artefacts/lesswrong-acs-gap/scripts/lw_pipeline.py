#!/usr/bin/env python3
"""
LessWrong agentic-coding retrieval pipeline.
  python3 lw_pipeline.py fetch  2026-05-20 corpus.jsonl     # ~90s, ~22MB for 1190 posts
  python3 lw_pipeline.py rank   corpus.jsonl                # instant, local
Emits shortlist.json (candidates) + aggregator_links.json (link-mining lane).
"""
import json, math, re, sys, time, urllib.request, urllib.parse

GQL = "https://www.lesswrong.com/graphql"
UA  = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# ───────────────────────────── FETCH ─────────────────────────────
POST_Q = """{ posts(input:{terms:{view:"new", limit:%d, offset:%d, after:"%s"}}) { results {
  _id title slug postedAt baseScore commentCount question af url
  user { displayName slug } tags { name slug } contents { wordCount markdown }
} } }"""

def gql(q, tries=4):
    req = urllib.request.Request(GQL, data=json.dumps({"query": q}).encode(), headers=UA)
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=180) as r: return json.loads(r.read())
        except Exception:
            if i == tries - 1: raise
            time.sleep(2 * (i + 1))

def fetch(after, out, page=100):
    n, off = 0, 0
    with open(out, "w") as f:
        while True:
            d = gql(POST_Q % (page, off, after))
            if "errors" in d: sys.exit("GQL: " + json.dumps(d["errors"])[:400])
            res = d["data"]["posts"]["results"]
            if not res: break
            for p in res: f.write(json.dumps(p) + "\n")
            n += len(res); off += page
            print(f"  {n} posts…", flush=True)
            if len(res) < page: break
            time.sleep(0.4)
    print(f"fetched {n} -> {out}")

# ───────────────────────── ANCHOR VOCABULARY ─────────────────────────
# HARD anchors: near-zero false-positive rate for "this post is about agentic coding".
HARD = {
 r"claude code":4.0, r"\bcodex\b":3.0, r"\bcursor\b":2.0, r"\baider\b":3.0, r"\bcopilot\b":1.8,
 r"\bdevin\b":2.5, r"windsurf":3.0, r"claude\.md":4.5, r"agents\.md":4.5, r"cursorrules":4.0,
 r"sub-?agents?":3.5, r"vibe cod":2.5, r"\bmcp\b":2.5, r"model context protocol":3.0,
 r"agentic (coding|engineering|software|development|programming)":4.0, r"coding agents?":3.0,
 r"slash command":3.5, r"\bworktree":4.0, r"claude agent sdk":4.0, r"\bagent sdk\b":3.0,
 r"ai[- ]assisted (coding|programming|development|software)":4.0, r"context engineering":4.0,
 r"plan mode":3.5, r"\bharness(es|ing)?\b":1.6, r"scaffold(ing|s|ed)?":1.6,
 r"agent(ic)? loop":3.0, r"llm (writes|wrote|generates?|generated)":2.0,
}
# SOFT anchors: supporting technique vocabulary (counted, but can't alone qualify a post).
SOFT = {
 r"context window":1.2, r"context rot":3.0, r"token budget":2.0, r"\bcompaction\b":2.5,
 r"tool calls?":1.5, r"tool[- ]use":1.5, r"system prompt":1.8, r"prompt engineering":2.0,
 r"parallel agents?":3.0, r"agent orchestrat":3.0, r"multi-?agent":1.2, r"\btmux\b":1.5,
 r"pair program":2.0, r"code review(ing)? agent":3.5, r"\bautonomous(ly)? (cod|writ|implement|refactor)":3.0,
 r"\bskills?\b(?=[^.]{0,70}(claude|agent|\.md|folder|directory|invoke))":2.5,
 r"\bhooks?\b(?=[^.]{0,80}(agent|claude|tool|command|pretool|posttool))":2.5,
}
SUBSTRATE = [r"\bcodebase\b", r"pull request", r"code review", r"refactor", r"unit test", r"\btdd\b",
 r"\bci\b", r"\blinter?\b", r"type error", r"\bcompiles?\b", r"\bdebugg?", r"\brepo(sitory)?\b",
 r"\bcommits?\b", r"pytest", r"test suite", r"stack trace", r"\bgit\b", r"merge conflict",
 r"\bpython\b", r"typescript", r"\brust\b", r"\bbash\b", r"\bterminal\b"]
VOICE = [r"\bi (asked|told|ran|tried|used|gave|had|built|wrote|set up|noticed|found|spent)\b",
 r"i've been (using|running|doing|trying)", r"my (workflow|setup|experience|process|agents?|repo)",
 r"in (my|our) experience", r"worked (well )?for me", r"\bwe (ran|tried|built|used)\b",
 r"here's (what|how) i", r"my current", r"\bi now \b"]
TITLE_RX = re.compile(r"claude code|codex|agentic|coding agent|sub-?agent|cursor|copilot|aider|vibe cod"
 r"|ai.assisted|harness|scaffold|context engineering|prompt|\bagents?\b|automat|\bllm\b|software"
 r"|workflow|\btool|program|engineer|\bcode\b|productiv", re.I)

HC = [(re.compile(p, re.I), w) for p, w in HARD.items()]
SC = [(re.compile(p, re.I), w) for p, w in SOFT.items()]
SUB = [re.compile(p, re.I) for p in SUBSTRATE]
VO  = [re.compile(p, re.I) for p in VOICE]
MDLINK = re.compile(r"\[([^\]]{0,120})\]\((https?://[^)]+)\)")

def analyse(p):
    c  = p.get("contents") or {}
    md = c.get("markdown") or ""
    words = c.get("wordCount") or max(len(md.split()), 1)
    title = p.get("title") or ""
    hard, hw, hn = {}, 0.0, 0
    for rx, w in HC:
        k = len(rx.findall(md))
        if k: hard[rx.pattern] = k; hw += w * k; hn += 1
    soft, sw, sn = {}, 0.0, 0
    for rx, w in SC:
        k = len(rx.findall(md))
        if k: soft[rx.pattern] = k; sw += w * k; sn += 1
    sub   = sum(1 for rx in SUB if rx.search(md))
    voice = sum(1 for rx in VO if rx.search(md))
    dens  = (hw + 0.6 * sw) / max(words, 300) * 1000        # per-1k-words, floored at 300w
    tb    = 8.0 if TITLE_RX.search(title) else 0.0
    score = 3.2 * dens + 5.0 * math.log1p(hn) + 1.0 * sub + 1.6 * voice + tb
    links = MDLINK.findall(md)
    return dict(id=p["_id"], slug=p["slug"], title=title,
        url=f"https://www.lesswrong.com/posts/{p['_id']}/{p['slug']}",
        ext_url=p.get("url"), karma=p.get("baseScore") or 0, ncomments=p.get("commentCount") or 0,
        date=p["postedAt"][:10], author=(p.get("user") or {}).get("displayName"),
        af=bool(p.get("af")), tags=[t["slug"] for t in (p.get("tags") or [])], words=words,
        score=round(score, 1), density=round(dens, 2), hard_n=hn, soft_n=sn, sub=sub, voice=voice,
        hard=sorted(hard.items(), key=lambda x: -x[1]), soft=sorted(soft.items(), key=lambda x: -x[1]),
        nlinks=len(links), body_blind=len(md) < 200,
        aggregator=bool(words > 5000 and len(links) > 40),
        _links=links)

def rank(path):
    rows = [analyse(json.loads(l)) for l in open(path)]
    aggs = [r for r in rows if r["aggregator"]]
    cands = [r for r in rows if not r["aggregator"]]

    # ── TWO-TIER GATE ──
    for r in cands:
        # Operating point chosen by measured recall: catches 10/10 known-good posts.
        t1 = r["hard_n"] >= 2 and r["density"] >= 3
        t2 = (r["hard_n"] >= 1 and (r["density"] >= 6 or r["voice"] >= 4)) or \
             (r["hard_n"] >= 1 and bool(TITLE_RX.search(r["title"])) and r["karma"] >= 10) or \
             (r["body_blind"] and bool(TITLE_RX.search(r["title"])))
        r["tier"] = 1 if t1 else (2 if t2 else 0)
    short = sorted([r for r in cands if r["tier"]], key=lambda r: (-r["score"]))
    # BAND for downstream triage: precision falls off sharply down the tail, so tell the
    # next stage how much effort each band deserves.
    for i, r in enumerate(short, 1):
        r["band"] = "A" if i <= 25 else ("B" if i <= 50 else "C")
        r.pop("_links", None)
    json.dump(short, open("shortlist.json", "w"), indent=1)

    # ── AGGREGATOR LINK-MINING LANE ──
    anchor_rx = re.compile(r"claude code|\bcodex\b|cursor|copilot|aider|agentic|sub-?agent|coding agent"
                           r"|vibe cod|agents?\.md|worktree|agent harness|agent scaffold"
                           r"|context engineering|\bmcp\b|slash command", re.I)
    mined = []
    for a in aggs:
        for text, u in a["_links"]:
            if anchor_rx.search(text) or anchor_rx.search(u):
                mined.append(dict(anchor=text[:120], url=u, from_post=a["title"], date=a["date"]))
    seen, dedup = set(), []
    for m in mined:
        if m["url"] not in seen: seen.add(m["url"]); dedup.append(m)
    json.dump(dedup, open("aggregator_links.json", "w"), indent=1)

    print(f"corpus={len(rows)}  aggregators={len(aggs)}  shortlist={len(short)} "
          f"(tier1={sum(1 for r in short if r['tier']==1)}, tier2={sum(1 for r in short if r['tier']==2)})")
    print(f"  bands: A(deep-read)={sum(1 for r in short if r['band']=='A')} "
          f"B(triage)={sum(1 for r in short if r['band']=='B')} "
          f"C(skim)={sum(1 for r in short if r['band']=='C')}")
    print(f"aggregator outbound links w/ agentic anchor text: {len(dedup)}")
    return short

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch": fetch(sys.argv[2], sys.argv[3])
    elif cmd == "rank": rank(sys.argv[2])
