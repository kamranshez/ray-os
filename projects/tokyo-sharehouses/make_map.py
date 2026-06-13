#!/usr/bin/env python3
"""Render listings.json into a self-contained Leaflet map with rich filters."""
import json, re

BASE = "/Users/ray/Desktop/ray-os/projects/tokyo-sharehouses"
listings = json.load(open(f"{BASE}/listings.json"))
pts = [l for l in listings if "lat" in l]

def color(r):
    if r is None: return "#888"
    if r < 50000:  return "#2ecc71"
    if r < 70000:  return "#3498db"
    if r < 90000:  return "#f39c12"
    return "#e74c3c"

def min_walk(stations):
    mins = [int(m) for s in stations for m in re.findall(r'(\d+)\s*minutes? walk', s)]
    return min(mins) if mins else None

def campaign_flags(c):
    j = " ".join(c).lower()
    return {
        "no_deposit": "security deposit" in j,
        "no_key": "key money" in j,
        "no_agency": "agency fee" in j,
    }

data = []
for l in pts:
    cf = campaign_flags(l.get("campaigns", []))
    data.append({
        "id": l["id"], "name": l["name"], "url": l["url"],
        "rent": l.get("rent"), "rent_max": l.get("rent_max"),
        "lat": l["lat"], "lng": l["lng"],
        "stations": l.get("stations", []), "campaigns": l.get("campaigns", []),
        "available": l.get("available"), "address": l.get("address", ""),
        "area_min": l.get("area_min"), "area_max": l.get("area_max"),
        "room_types": l.get("room_types", []), "capacity": l.get("capacity"),
        "gender": l.get("gender", "Mixed"), "structure": l.get("structure", ""),
        "age_limit": l.get("age_limit", ""), "walk": min_walk(l.get("stations", [])),
        "color": color(l.get("rent")), **cf,
    })

rents = [l["rent"] for l in pts if l.get("rent")]
areas = [d["area_max"] for d in data if d.get("area_max")]
rmin, rmax = min(rents), max(rents)
amax = max(areas) if areas else 30
stats = {"total": len(listings), "mapped": len(pts),
         "min": rmin, "max": rmax, "med": sorted(rents)[len(rents)//2]}

HTML = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>X-House Tokyo Sharehouses</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
<style>
 *{box-sizing:border-box} body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif}
 #map{position:absolute;top:0;bottom:0;left:360px;right:0}
 #side{position:absolute;top:0;bottom:0;left:0;width:360px;overflow-y:auto;
   background:#1a1d24;color:#e8eaed;padding:16px}
 h1{font-size:17px;margin:0 0 4px} .sub{color:#9aa0a6;font-size:12px;margin-bottom:12px}
 .stat{display:flex;gap:8px;margin-bottom:8px}
 .stat div{background:#262a33;border-radius:8px;padding:7px 8px;flex:1;text-align:center}
 .stat b{display:block;font-size:16px} .stat span{font-size:10px;color:#9aa0a6}
 .fbox{background:#21252e;border-radius:8px;padding:10px 12px;margin-bottom:8px}
 label{font-size:12px;color:#cbd1d8;display:block;margin:2px 0 4px}
 .val{color:#4da3ff;font-weight:600} input[type=range]{width:100%;margin:2px 0}
 .row{display:flex;gap:8px} .row>div{flex:1}
 .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
 .chip{font-size:11px;padding:4px 9px;border-radius:14px;background:#2c313b;
   color:#cbd1d8;cursor:pointer;border:1px solid transparent;user-select:none}
 .chip.on{background:#1d4e8a;border-color:#4da3ff;color:#fff}
 select{width:100%;background:#2c313b;color:#e8eaed;border:1px solid #3a414d;border-radius:6px;padding:5px}
 .legend span{display:inline-flex;align-items:center;gap:4px;font-size:10px;margin-right:8px}
 .dot{width:10px;height:10px;border-radius:50%;display:inline-block}
 #count{font-size:12px;color:#9aa0a6;margin:8px 0 6px;font-weight:600}
 .card{background:#262a33;border-radius:8px;padding:9px;margin-bottom:7px;cursor:pointer;border:1px solid transparent}
 .card:hover{border-color:#4da3ff} .card .nm{font-size:13px;font-weight:600}
 .card .rt{color:#4da3ff;font-size:13px;float:right}
 .card .st{font-size:11px;color:#9aa0a6;margin-top:3px}
 .card .mt{font-size:10px;color:#7d8590;margin-top:2px}
 a{color:#4da3ff} .pop b{font-size:13px} .pop .r{color:#e74c3c;font-weight:600}
 .pop a{display:inline-block;margin-top:6px} .reset{font-size:11px;color:#9aa0a6;cursor:pointer;float:right}
</style></head><body>
<div id="side">
 <h1>X-House Tokyo Sharehouses <span class="reset" onclick="resetAll()">reset</span></h1>
 <div class="sub">__MAPPED__ vacant listings · 38 wards · live data</div>
 <div class="stat">
   <div><b id="shown">__MAPPED__</b><span>showing</span></div>
   <div><b>¥__MED__</b><span>median</span></div>
   <div><b>¥__MINS__</b><span>cheapest</span></div>
 </div>

 <div class="fbox">
   <label>Rent: <span class="val" id="rlbl"></span></label>
   <div class="row">
     <div><input type="range" id="rmin" min="__MIN__" max="__MAX__" value="__MIN__" step="1000"></div>
     <div><input type="range" id="rmax" min="__MIN__" max="__MAX__" value="__MAX__" step="1000"></div>
   </div>
 </div>

 <div class="fbox">
   <label>Min room size: <span class="val" id="albl">any</span></label>
   <input type="range" id="amin" min="0" max="__AMAX__" value="0" step="0.5">
 </div>

 <div class="fbox">
   <label>Max walk to station: <span class="val" id="wlbl">any</span></label>
   <input type="range" id="wmax" min="1" max="30" value="30" step="1">
 </div>

 <div class="fbox">
   <label>Room type</label>
   <div class="chips" id="rtchips">
     <span class="chip" data-rt="Dormitory">Dormitory</span>
     <span class="chip" data-rt="Private room">Private room</span>
     <span class="chip" data-rt="Apartment">Apartment</span>
   </div>
 </div>

 <div class="fbox">
   <div class="row">
     <div>
       <label>Gender</label>
       <select id="gender">
         <option value="">Any</option><option>Mixed</option>
         <option>Women only</option><option>Men only</option>
       </select>
     </div>
   </div>
   <label style="margin-top:8px">Cost savers</label>
   <div class="chips" id="cchips">
     <span class="chip" data-c="no_deposit">No deposit</span>
     <span class="chip" data-c="no_key">No key money</span>
     <span class="chip" data-c="no_agency">No agency fee</span>
   </div>
 </div>

 <div class="legend">
   <span><i class="dot" style="background:#2ecc71"></i>&lt;50k</span>
   <span><i class="dot" style="background:#3498db"></i>50-70k</span>
   <span><i class="dot" style="background:#f39c12"></i>70-90k</span>
   <span><i class="dot" style="background:#e74c3c"></i>90k+</span>
 </div>
 <div id="count"></div>
 <div id="list"></div>
</div>
<div id="map"></div>
<script>
const DATA = __DATA__;
const map = L.map('map').setView([35.69, 139.70], 12);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
  {attribution:'&copy; OSM &copy; CARTO', maxZoom:19}).addTo(map);
const cluster = L.markerClusterGroup({maxClusterRadius:45});
let markers={};
const yen=n=>'¥'+n.toLocaleString();
function popup(d){
  let s='<div class="pop"><b>'+d.name+'</b><br>';
  if(d.rent) s+='<span class="r">'+yen(d.rent)+(d.rent_max&&d.rent_max!=d.rent?'–'+yen(d.rent_max):'')+'/mo</span><br>';
  if(d.area_max) s+='<small>Size: '+(d.area_min||d.area_max)+'–'+d.area_max+'㎡ · '+(d.room_types.join(', ')||'')+'</small><br>';
  if(d.gender&&d.gender!='Mixed') s+='<small>'+d.gender+'</small><br>';
  if(d.stations.length) s+='<small>'+d.stations.slice(0,3).join('<br>')+'</small><br>';
  if(d.available) s+='<small>Available: '+d.available+'</small><br>';
  if(d.address) s+='<small>'+d.address+'</small><br>';
  s+='<a href="'+d.url+'" target="_blank">View listing &raquo;</a></div>';
  return s;
}
DATA.forEach(d=>{
  const m=L.circleMarker([d.lat,d.lng],{radius:7,color:'#fff',weight:1,fillColor:d.color,fillOpacity:.9});
  m.bindPopup(popup(d)); markers[d.id]=m; cluster.addLayer(m);
});
map.addLayer(cluster);

const $=id=>document.getElementById(id);
const rmin=$('rmin'),rmax=$('rmax'),amin=$('amin'),wmax=$('wmax'),gender=$('gender');
const rtSel=new Set(), cSel=new Set();
document.querySelectorAll('#rtchips .chip').forEach(c=>c.onclick=()=>{
  c.classList.toggle('on'); c.classList.contains('on')?rtSel.add(c.dataset.rt):rtSel.delete(c.dataset.rt); render();});
document.querySelectorAll('#cchips .chip').forEach(c=>c.onclick=()=>{
  c.classList.toggle('on'); c.classList.contains('on')?cSel.add(c.dataset.c):cSel.delete(c.dataset.c); render();});
[rmin,rmax,amin,wmax].forEach(e=>e.oninput=render); gender.onchange=render;

function resetAll(){
  rmin.value=rmin.min; rmax.value=rmax.max; amin.value=0; wmax.value=30; gender.value='';
  rtSel.clear(); cSel.clear();
  document.querySelectorAll('.chip.on').forEach(c=>c.classList.remove('on')); render();
}
function pass(d){
  let lo=+rmin.value, hi=+rmax.value; if(lo>hi){[lo,hi]=[hi,lo];}
  if(d.rent!==null && (d.rent<lo || d.rent>hi)) return false;
  if(+amin.value>0 && !(d.area_max>=+amin.value)) return false;
  if(+wmax.value<30 && !(d.walk!==null && d.walk<=+wmax.value)) return false;
  if(rtSel.size && !d.room_types.some(t=>rtSel.has(t))) return false;
  if(gender.value && d.gender!==gender.value) return false;
  for(const c of cSel) if(!d[c]) return false;
  return true;
}
function render(){
  let lo=+rmin.value, hi=+rmax.value; if(lo>hi){[lo,hi]=[hi,lo];}
  $('rlbl').textContent=yen(lo)+' – '+yen(hi);
  $('albl').textContent=+amin.value>0?(+amin.value)+'㎡+':'any';
  $('wlbl').textContent=+wmax.value<30?(+wmax.value)+' min':'any';
  cluster.clearLayers(); let shown=[];
  DATA.forEach(d=>{ if(pass(d)){cluster.addLayer(markers[d.id]); shown.push(d);} });
  shown.sort((a,b)=>(a.rent||1e9)-(b.rent||1e9));
  $('shown').textContent=shown.length; $('count').textContent=shown.length+' listings';
  $('list').innerHTML=shown.slice(0,200).map(d=>
    '<div class="card" data-id="'+d.id+'"><span class="rt">'+(d.rent?yen(d.rent):'—')+
    '</span><div class="nm">'+d.name+'</div><div class="st">'+(d.stations[0]||'')+
    '</div><div class="mt">'+[d.area_max?d.area_max+'㎡':'',d.room_types.join('/'),
      d.walk!=null?d.walk+'min walk':''].filter(Boolean).join(' · ')+'</div></div>').join('');
  $('list').querySelectorAll('.card').forEach(c=>c.onclick=()=>{
    const m=markers[c.dataset.id]; map.setView(m.getLatLng(),16); m.openPopup();});
}
render();
</script></body></html>"""

repl = {"__DATA__": json.dumps(data, ensure_ascii=False),
        "__MAPPED__": stats["mapped"], "__MIN__": rmin, "__MAX__": rmax,
        "__AMAX__": amax, "__MED__": f'{stats["med"]:,}', "__MINS__": f'{rmin:,}'}
out = HTML
for k, v in repl.items():
    out = out.replace(k, str(v))
path = f"{BASE}/tokyo-sharehouses-map.html"
open(path, "w").write(out)
print("Wrote", path)
print(f"Stats: {stats} | area_max range up to {amax}㎡")
