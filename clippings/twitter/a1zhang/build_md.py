#!/usr/bin/env python3
"""Build a readable markdown digest from raw.json."""
import json, os
from datetime import datetime

OUTDIR = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(OUTDIR, "raw.json")))

def fmt_dt(s):
    try:
        dt = datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return s

def stats(t):
    bits = []
    for k, label in [("favorites","❤"),("retweets","🔁"),("replies","💬"),("bookmarks","🔖"),("views","👁")]:
        v = t.get(k)
        if v not in (None, "", 0, "0"):
            bits.append(f"{label}{v}")
    return "  ".join(bits)

def tweet_url(handle, tid):
    return f"https://x.com/{handle}/status/{tid}"

def media_lines(t):
    out = []
    for m in (t.get("media") or []):
        if isinstance(m, dict):
            url = m.get("media_url_https") or m.get("url")
            if url:
                out.append(f"  - {m.get('type','media')}: {url}")
        # nested structure (photo/video arrays)
    md = t.get("media")
    if isinstance(md, dict):
        for p in md.get("photo", []) or []:
            out.append(f"  - photo: {p.get('media_url_https')}")
        for v in md.get("video", []) or []:
            if v.get("media_url_https"):
                out.append(f"  - video thumb: {v.get('media_url_https')}")
    return out

def quoted_block(t):
    q = t.get("quoted")
    if not q or not isinstance(q, dict):
        return []
    qa = (q.get("author") or {}).get("screen_name", "?")
    qt = q.get("text", "").replace("\n", " ")
    return [f"  > 🔗 **Quoting @{qa}:** {qt}"]

u = raw.get("user", {})
lines = []
lines.append("---")
lines.append("tags: [twitter, research, monitoring]")
lines.append(f"aliases: [a1zhang twitter digest]")
lines.append(f"date: {raw['fetched_at'][:10]}")
lines.append("---")
lines.append("")
desc = (u.get('desc','') or '').replace("\n", " ").strip()
lines.append(f"> **@{raw['target']}** — {u.get('name','')}  ")
lines.append(f"> {desc}  ")
lines.append(f"> Followers: {u.get('followers_count','?')} · Following: {u.get('friends_count','?')}  ")
lines.append(f"> **Fetched:** {raw['fetched_at']}  ")
lines.append(f"> **Window:** tweets since {raw['cutoff'][:16]} UTC (last 24h)")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append(f"- **{len(raw['own_tweets_recent'])}** original tweets in the last day")
lines.append(f"- **{len(raw['own_replies_recent'])}** replies in the last day")
lines.append(f"- **{len(raw['parents'])}** parent tweets resolved (the posts they replied to)")
lines.append(f"- **{len(raw['context_items'])}** surrounding context tweets from other people in those threads")
lines.append("")

# Own tweets
lines.append("---")
lines.append("")
lines.append("## Original tweets (last 24h)")
lines.append("")
if not raw["own_tweets_recent"]:
    lines.append("_None in window._")
for t in raw["own_tweets_recent"]:
    tid = t.get("tweet_id") or t.get("id")
    lines.append(f"### {fmt_dt(t.get('created_at',''))}")
    lines.append("")
    lines.append(t.get("text","").strip())
    lines.append("")
    ql = quoted_block(t)
    if ql: lines += ql + [""]
    ml = media_lines(t)
    if ml:
        lines.append("Media:")
        lines += ml
        lines.append("")
    meta = stats(t)
    lines.append(f"{meta}  ·  [link]({tweet_url(raw['target'], tid)})" if meta else f"[link]({tweet_url(raw['target'], tid)})")
    lines.append("")

# Replies with parent context
lines.append("---")
lines.append("")
lines.append("## Replies (last 24h) — with the tweet they replied to")
lines.append("")
if not raw["own_replies_recent"]:
    lines.append("_None in window._")
for t in sorted(raw["own_replies_recent"], key=lambda x: x.get("created_at",""), reverse=True):
    tid = t.get("tweet_id") or t.get("id")
    pid = t.get("in_reply_to_status_id_str")
    parent = raw["parents"].get(pid or "")
    lines.append(f"### {fmt_dt(t.get('created_at',''))}")
    lines.append("")
    if parent:
        pa = (parent.get("author") or {})
        ph = pa.get("screen_name","?")
        lines.append(f"**↪ In reply to @{ph}** ({pa.get('name','')}):")
        lines.append("")
        lines.append("> " + parent.get("text","").strip().replace("\n", "\n> "))
        lines.append("")
        pmeta = stats(parent)
        if pmeta:
            lines.append(f"> {pmeta}  ·  [parent link]({tweet_url(ph, pid)})")
            lines.append("")
    elif pid:
        lines.append(f"**↪ In reply to** tweet `{pid}` (could not resolve)")
        lines.append("")
    lines.append("**@a1zhang replied:**")
    lines.append("")
    lines.append(t.get("text","").strip())
    lines.append("")
    ql = quoted_block(t)
    if ql: lines += ql + [""]
    meta = stats(t)
    lines.append(f"{meta}  ·  [link]({tweet_url(raw['target'], tid)})" if meta else f"[link]({tweet_url(raw['target'], tid)})")
    lines.append("")

# Context from others
lines.append("---")
lines.append("")
lines.append("## Conversation context (other people in those threads)")
lines.append("")
lines.append("_People who appeared in the same reply threads as @a1zhang._")
lines.append("")
for t in raw["context_items"]:
    a = (t.get("author") or {})
    h = a.get("screen_name","?")
    tid = t.get("tweet_id") or t.get("id")
    txt = t.get("text","").strip().replace("\n"," ")
    lines.append(f"- **@{h}** ({fmt_dt(t.get('created_at',''))}): {txt}  ·  [link]({tweet_url(h, tid)})")
lines.append("")

out_path = os.path.join(OUTDIR, f"a1zhang-digest-{raw['fetched_at'][:10]}.md")
with open(out_path, "w") as f:
    f.write("\n".join(lines))
print("Wrote", out_path)
print(len(lines), "lines")
