#!/usr/bin/env python3
"""Lanes 2 & 4: LessWrong /api/search (posts + comments indices), unauthenticated."""
import json, sys, time, urllib.request, datetime

URL = "https://www.lesswrong.com/api/search"
QUERIES = [
 "claude code workflow", "codex cli agentic coding", "cursor ide agent rules",
 "CLAUDE.md AGENTS.md instructions file", "subagent delegation parallel agents",
 "coding agent harness scaffold", "context engineering context window management",
 "AI assisted software engineering productivity", "vibe coding experience report",
 "prompt techniques for coding agents", "agent tool use loop verifier tests",
 "MCP server model context protocol tools", "LLM writes my code review",
 "how I use AI to program", "git worktree parallel claude sessions",
 "agent skills slash commands hooks", "автоматизация",  # noise control probe
 "long horizon autonomous coding task", "LLM refactor large codebase",
 "spec driven development with AI agent", "evaluating coding agents benchmark",
 "AI pair programming tips tricks", "token budget compaction long context agent",
 "test driven development with LLM agent", "debugging with an AI agent",
]

def search(index, query, after_ms, hits=40):
    body = json.dumps([{"indexName": index, "params": {
        "query": query, "hitsPerPage": hits,
        "numericFilters": [f"publicDateMs>{after_ms}"]}}]).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())[0]

after = sys.argv[1] if len(sys.argv) > 1 else "2026-05-20"
after_ms = int(datetime.datetime.fromisoformat(after).replace(
    tzinfo=datetime.timezone.utc).timestamp() * 1000)

posts, comments = {}, {}
for q in QUERIES:
    r = search("posts", q, after_ms)
    for rank, h in enumerate(r["hits"]):
        e = posts.setdefault(h["objectID"], dict(
            id=h["objectID"], title=h["title"], slug=h["slug"], karma=h["baseScore"],
            date=h["postedAt"][:10], author=h.get("authorDisplayName"),
            tags=[t["slug"] for t in (h.get("tags") or [])], queries=[], best_rank=99))
        e["queries"].append(q); e["best_rank"] = min(e["best_rank"], rank)
    c = search("comments", q, after_ms, hits=30)
    for rank, h in enumerate(c["hits"]):
        e = comments.setdefault(h["objectID"], dict(
            id=h["objectID"], postId=h["postId"], postTitle=h.get("postTitle"),
            postSlug=h.get("postSlug"), karma=h["baseScore"], date=h["postedAt"][:10],
            author=h.get("authorDisplayName"), body=(h.get("body") or "")[:600],
            queries=[]))
        e["queries"].append(q)
    time.sleep(0.25)

json.dump(list(posts.values()), open("search_posts.json","w"), indent=1)
json.dump(list(comments.values()), open("search_comments.json","w"), indent=1)
print(f"search lane: {len(posts)} unique posts, {len(comments)} unique comments "
      f"across {len(QUERIES)} queries")
