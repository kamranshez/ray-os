#!/usr/bin/env python3
"""Write each shortlisted post's FULL body to its own file for the downstream stage."""
import json, os, re, sys
short=json.load(open('shortlist.json'))
bodies={}
for l in open(sys.argv[1] if len(sys.argv)>1 else 'corpus2.jsonl'):
    p=json.loads(l); bodies[p['_id']]=(p.get('contents') or {}).get('markdown') or ''
os.makedirs('bodies',exist_ok=True)
idx=[]
for i,r in enumerate(short,1):
    slug=re.sub(r'[^a-z0-9]+','-',r['title'].lower()).strip('-')[:60]
    fn=f"bodies/{i:02d}-{slug}.md"
    with open(fn,'w') as f:
        f.write(f"# {r['title']}\n\n")
        f.write(f"- URL: {r['url']}\n- Author: {r['author']}\n- Date: {r['date']}\n"
                f"- Karma: {r['karma']}  Comments: {r['ncomments']}  Words: {r['words']}\n"
                f"- Band: {r['band']}  Tier: {r['tier']}  Score: {r['score']}  Density: {r['density']}\n"
                f"- Anchors: {', '.join(k for k,_ in r['hard'])}\n\n---\n\n")
        f.write(bodies[r['id']])
    r['body_path']=os.path.abspath(fn); idx.append(r)
json.dump(idx,open('shortlist.json','w'),indent=1)
print(f"wrote {len(idx)} body files to {os.path.abspath('bodies')}")
