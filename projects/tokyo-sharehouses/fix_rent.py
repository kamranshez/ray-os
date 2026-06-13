import json, re, time, urllib.parse, urllib.request, http.cookiejar, html as H
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
CITY=("68,70,72,67,60,77,69,79,83,62,66,59,63,71,75,85,74,78,84,65,64,76,88,90,98,96,93,80,100,122,124,125,129,130,133,134,136,139")
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def get(u,h=None):
    r=urllib.request.Request(u,headers={"User-Agent":UA,**(h or {})}); return op.open(r,timeout=30).read().decode("utf-8","replace")
def post(u,d,h=None):
    r=urllib.request.Request(u,data=urllib.parse.urlencode(d).encode(),headers={"User-Agent":UA,"X-Requested-With":"XMLHttpRequest",**(h or {})}); return op.open(r,timeout=60).read().decode("utf-8","replace")
page=get("https://x-house.co.jp/en/tokyo/city/?vacant_room_flg=1")
csrf=re.search(r'name="csrf-token" content="([^"]+)"',page).group(1)
def fp(skip,first):
    d={"take":30,"skip":skip,"is_first_load":"true" if first else "false","language":"en","url_language":"en","form_datas[vacant_room_flg]":"1","form_datas[sort]":"recommend","form_datas[city]":CITY}
    return json.loads(post("https://x-house.co.jp/api/cn-h/ajax/load_more_properties",d,{"X-CSRF-TOKEN":csrf}))
first=fp(0,True); total=int(first["property_count"]); allh=[first["html"]]
for s in range(30,total+30,30):
    try: allh.append(fp(s,False)["html"])
    except Exception as e: print("err",s,e)
    time.sleep(0.25)
big="\n".join(allh)
cards=re.split(r'<article class="c-property-card">',big)[1:]
rentmap={}
for c in cards:
    m=re.search(r'<a href="(https://x-house\.co\.jp/en/[^"]+/)"',c)
    if not m: continue
    url=m.group(1)
    pid_m=re.search(r'property_id=(\d+)',c) or re.search(r'xross-(\d+)',url)
    pid=pid_m.group(1) if pid_m else url.rstrip("/").split("/")[-1]
    rents=[int(x.replace(",","")) for x in re.findall(r'<span class="num">\s*([\d,]+)\s*<span class="unit">',c)]
    if rents: rentmap[pid]={"rent":min(rents),"rent_max":max(rents),"room_count":len(rents)}
# merge into listings.json
L=json.load(open("listings.json"))
patched=0
for l in L:
    r=rentmap.get(l["id"])
    if r: l.update(r); patched+=1
json.dump(L,open("listings.json","w"),ensure_ascii=False,indent=2)
rv=[l["rent"] for l in L if l.get("rent")]
print(f"patched {patched}/{len(L)} | rent min {min(rv)} med {sorted(rv)[len(rv)//2]} max {max(rv)}")
