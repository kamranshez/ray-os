#!/usr/bin/env python3
"""Lane 1 scorer: density-normalised agentic-coding relevance over FULL post bodies."""
import json, re, math, sys

# ---- ANCHORS: terms that are essentially never in a non-agentic-coding post. High precision.
ANCHOR = {
 r"claude code":4.0, r"claude-code":4.0, r"\bcodex\b":3.0, r"claude agent sdk":4.0, r"\bagent sdk\b":3.0,
 r"\baider\b":3.0, r"\bdevin\b":2.5, r"windsurf":3.0, r"github copilot":2.5, r"\bcopilot\b":1.5,
 r"\bcursor\b":2.0, r"claude\.md":4.5, r"agents\.md":4.5, r"cursorrules":4.0, r"\.cursor/":4.0,
 r"sub-?agents?":3.5, r"slash command":3.5, r"\bmcp\b":2.5, r"model context protocol":3.0,
 r"agentic (coding|engineering|software|development|programming)":4.0,
 r"coding agents?":3.0, r"vibe cod":2.5, r"ai[- ]assisted (coding|programming|development|software)":4.0,
 r"agent(ic)? harness":3.5, r"\bharness(es)?\b":1.5, r"scaffold(ing|s|ed)?":1.5,
 r"agent(ic)? loop":3.0, r"context engineering":4.0, r"context rot":3.0, r"context window":1.2,
 r"plan mode":3.5, r"git worktree":4.0, r"\btmux\b":1.5, r"token budget":2.0, r"\bcompaction\b":2.5,
 r"tool calls?":1.5, r"tool[- ]use":1.5, r"system prompt":1.8, r"prompt engineering":2.0,
 r"parallel agents?":3.0, r"agent orchestrat":3.0, r"multi-?agent":1.2,
 r"\bskills?\b(?=[^.]{0,70}(claude|agent|\.md|folder|directory|invoke))":2.5,
 r"\bhooks?\b(?=[^.]{0,80}(agent|claude|tool|command|pretool|posttool))":2.5,
 r"pair program":2.0, r"llm (writes|wrote|generates?|generated) (the )?code":2.5,
 r"code review(ing)? agent":3.5, r"\bautonomous(ly)? (cod|writ|implement|refactor)":3.0,
}
# ---- SUBSTRATE: proves it's about shipping real software, not pure theory
SUBSTRATE = [r"\bcodebase\b", r"pull request", r"code review", r"refactor", r"unit test", r"\btdd\b",
  r"\bci\b", r"\blinter?\b", r"type error", r"\bcompiles?\b", r"\bdebugg?", r"\brepo(sitory)?\b",
  r"\bcommits?\b", r"pytest", r"test suite", r"stack trace", r"\bgit\b", r"\bmerge conflict",
  r"\bpython\b", r"typescript", r"\brust\b", r"\bbash\b", r"\bterminal\b", r"\bIDE\b"]
# ---- PRACTITIONER voice: they actually ran it
VOICE = [r"\bi (asked|told|ran|tried|used|gave|had|built|wrote|set up|noticed|found|spent)\b",
  r"i've been (using|running|doing|trying)", r"my (workflow|setup|experience|process|agents?|repo)",
  r"in (my|our) experience", r"worked (well )?for me", r"\bwe (ran|tried|built|used)\b",
  r"here's (what|how) i", r"turns out", r"my current", r"i now "]
TITLE_RX = re.compile(r"claude code|codex|agentic|coding agent|sub-?agent|cursor|copilot|aider|vibe cod"
  r"|ai.assisted|harness|scaffold|context engineering|prompt|\bagents?\b|automat|\bllm\b|software|workflow|tool", re.I)

AC = [(re.compile(p, re.I), w) for p, w in ANCHOR.items()]
SC = [re.compile(p, re.I) for p in SUBSTRATE]
VC = [re.compile(p, re.I) for p in VOICE]
LINK_RX = re.compile(r"\]\(https?://")

def analyse(p):
    md = (p.get("contents") or {}).get("markdown") or ""
    words = (p.get("contents") or {}).get("wordCount") or max(len(md.split()), 1)
    title = p.get("title") or ""
    hits, wsum, distinct = {}, 0.0, 0
    for rx, w in AC:
        n = len(rx.findall(md))
        if n:
            distinct += 1; wsum += w * n; hits[rx.pattern] = n
    sub = sum(1 for rx in SC if rx.search(md))
    voice = sum(1 for rx in VC if rx.search(md))
    # DENSITY: anchor weight per 1k words. floor at 300 words so tiny posts don't explode.
    dens = wsum / max(words, 300) * 1000
    tboost = 8.0 if TITLE_RX.search(title) else 0.0
    # breadth is log-damped so a 15k-word roundup can't win on breadth alone
    score = 3.2*dens + 2.5*math.log1p(distinct)*2 + 1.0*sub + 1.6*voice + tboost
    nlinks = len(LINK_RX.findall(md))
    lu = p.get("linkUrl") or ""
    return dict(
        id=p["_id"], slug=p["slug"], title=title,
        url=f"https://www.lesswrong.com/posts/{p['_id']}/{p['slug']}",
        karma=p.get("baseScore"), comments=p.get("commentCount"), date=p["postedAt"][:10],
        author=(p.get("user") or {}).get("displayName"), af=bool(p.get("af")),
        tags=[t["slug"] for t in (p.get("tags") or [])], words=words,
        score=round(score,1), density=round(dens,2), distinct=distinct, sub=sub, voice=voice,
        nlinks=nlinks, ext_link=lu if lu and "lesswrong.com" not in lu else None,
        # a link-aggregator/newsletter: very long + very link-dense
        aggregator=bool(words > 5000 and nlinks > 40),
        top_hits=sorted(hits.items(), key=lambda x: -x[1])[:10])

if __name__ == "__main__":
    rows = [analyse(json.loads(l)) for l in open(sys.argv[1])]
    rows.sort(key=lambda r: -r["score"])
    json.dump(rows, open("scored2.json","w"), indent=1)
    agg=[r for r in rows if r["aggregator"]]
    print(f"scored {len(rows)}; aggregators flagged: {len(agg)} -> {[r['title'][:30] for r in agg[:14]]}")
