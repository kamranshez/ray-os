# Claims all the way down

- URL: https://www.lesswrong.com/posts/ud6wrLLshsG8Jvkec/claims-all-the-way-down
- Author: Jasper Blank
- Date: 2026-06-16
- Karma: 9  Comments: 0  Words: 2802
- Band: C  Tier: 2  Score: 30.5  Density: 7.14
- Anchors: \bcursor\b

---

It can be hard to know where to begin when you do not understand something. A way to try to understand things is to look at what the people who claim to understand something are talking about.  
Sadly this means you have to deal with massive discussions. A big example of this is the Covid [origin debates](https://www.astralcodexten.com/p/practically-a-book-review-rootclaim). During these discussions the disagreement can be about many parts, and it can be hard to know who is even telling the truth and who is lying. This can make it almost impossible to map out what the world is really like and to see why.

  

Almost, but not quite...

If we want to map out these discussions we have to start with the core of what makes an honest argument. At the core there are primary sources. Primary sources can be a specific study, a witness claim or a verified authority to name a few. These primary sources can then be linked to claims. If we find all of the relevant primary sources and all of the claims that are supported by them we can calculate how valid each of these claims is using methods explained later in this article.

Sometimes, however, a claim is so complicated that there are many different primary sources pointing in many different directions. In these cases it can be helpful to break the claim down into subclaims. Each of these subclaims can then in turn be supported by primary sources or subclaims. As long as the logic connecting every claim with subclaims and sources is valid, it will allow you to find the best possible conclusion based on the available evidence.

Finding the strength of any piece of evidence on any claim used to be painstakingly slow and difficult to calibrate. This is where language models come in. They can do the arduous work of scraping for every source and identifying how relevant it is and how strongly it weighs on each specific claim. This can quickly fill out an entire graph of claims. This graph of claims can then be made into a publicly available tool.

These calls will still be subjective which is why it is essential for the tool to be transparent and easy to add your own perspective to. People are going to disagree with the final outcome of this process no matter what claim it ends up supporting. This disagreement is why we wanted this tool in the first place. That is why it is essential to keep every factor accessible and able to be called into question. A proper version of this tool should be able to quickly show the effects of any change to any link on the final claim.

Once this tool is in place you will be able to drill down on any part of the claim tree and find why every part of the argument is as strong as it is. By the end of this article I will present one component I believe any version of this tool would need. This component is called the grouping node and allows a single node to combine the evidence present in multiple sources or subclaims into a single probability a relevant margin for error.

How claims should be combined
=============================

In starting work on this tool I wrote down some core principles to keep this tool accountable to.

*   Every claim should be traceable to primary sources
*   Every number that is not set in stone should be shown as such
*   The system should be clear and understandable
*   The arithmetic should be based on existing literature
*   The system should have consistent reasoning on reruns
*   The system should be able to capture any argument

To show what this system could look like when filled out I wrote an example graph that shows how a claim can be supported by subclaims and how each of these claims can be supported by subclaims and sources in turn.

At the top you see the main claim. This main claim is the one we want to know with appropriate certainty. You can see that this claim has two subclaims, in this case a supporting and a refuting subclaim. The claim takes into account both of these subclaims when coming to a final value. Each of these subclaims have their own inputs in turn. The beauty is that this can extend down as far as needed to represent any argument.

This graph is only illustrative. All of the values in this first widget are there to show how the information propagates. If you want to know how real sources get put in then keep on reading until the second widget.

This graph is fully interactive. I encourage you to try clicking on every part. It can be especially fun to click on a source and change the value and see how every upstream claim adjusts based on it.

```widget[xBBTMJTdhkPYAeT8Q]
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Netherlands flood claim tree</title>
<style>
  :root{
    --bg:#ffffff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0;
    --yes:#0f766e; --no:#b45309;
    --yes-bg:#eef5f5; --no-bg:#faf3ee;
    --mono:"SFMono-Regular",ui-monospace,Menlo,Consolas,monospace;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);padding:18px 16px 30px;}
  .stage{position:relative;max-width:660px;height:350px;margin:0 auto;overflow:hidden;isolation:isolate;}
  .world{position:absolute;left:0;top:0;width:2400px;height:760px;transform-origin:0 0;will-change:transform;z-index:1;pointer-events:none;}
  .world.animating{transition:none;}
  svg#wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;}
  .stage.is-flipping .node.nav{pointer-events:none;}
  .stage.is-flipping .upstub{pointer-events:none;}
  .flip-layer{position:absolute;inset:0;z-index:20;pointer-events:none;}
  .flip-layer .node{position:absolute;margin:0;transform-origin:0 0;will-change:transform,opacity;}
  .flip-layer .pop{display:none!important;}
  .flip-ghost-wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;}
  .node.flip-new{will-change:transform,opacity;}
  #wires.flip-new-wires{will-change:opacity;}

  .tree{position:absolute;inset:0;z-index:1;display:block;}

  .node{background:#fff;border:1px solid var(--line);border-radius:11px;padding:9px 8px;text-align:center;}
  .world .node{position:absolute;width:140px;min-width:0;transform:translate(-50%,-50%) scale(var(--node-scale,1));transform-origin:center;will-change:transform,opacity;pointer-events:auto;}
  .ntype{font-size:9.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);line-height:1.25;margin-bottom:5px;}
  .nnum{font-family:var(--mono);font-size:14px;font-weight:700;}
  .nnum.pos{color:var(--yes);} .nnum.neg{color:var(--no);}
  .node.support{border-color:rgba(15,118,110,.45);background:var(--yes-bg);}
  .node.refute{border-color:rgba(180,83,9,.45);background:var(--no-bg);}
  .node.support .ntype{color:var(--yes);} .node.refute .ntype{color:var(--no);}

  .node.claim{border:2px solid var(--ink);border-radius:13px;padding:12px 12px;justify-self:center;min-width:300px;}
  .node.claim .ntype{font-size:11px;color:var(--ink);font-weight:700;letter-spacing:.08em;}
  .node.claim .nnum{font-size:22px;}
  .node.sub{justify-self:center;min-width:140px;}
  .world .node.claim,.flip-layer .node.claim{width:300px;}
  .world .node.claim,.world .node.sub{min-width:0;}
  .node.focused{border-width:2px;box-shadow:0 8px 24px rgba(15,23,42,.1);}
  .node.focused.support{border-color:rgba(15,118,110,.85);}
  .node.focused.refute{border-color:rgba(180,83,9,.85);}
  .world .node.popover-open{z-index:50;}

  .node.nav{cursor:pointer;transition:box-shadow .12s,border-color .12s;}
  .node.nav:hover{border-color:#6366f1;box-shadow:0 3px 12px rgba(99,102,241,.18);}

  /* source number → popover */
  .node.src .nnum{cursor:pointer;border-bottom:1.5px dotted #94a3b8;display:inline-block;padding:0 2px;border-radius:2px;}
  .node.src .nnum:hover{background:#eef2ff;border-bottom-color:#6366f1;}
  .pop{display:none;position:absolute;z-index:30;top:100%;left:50%;transform:translateX(-50%);margin-top:4px;
       background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 24px rgba(15,23,42,.16);
       padding:10px 12px;width:172px;cursor:default;text-align:left;}
  .pop::before{content:"";position:absolute;top:-18px;left:-16px;right:-16px;bottom:-16px;background:transparent;z-index:-1;}
  .pop.open{display:block;}
  .pop .plab{font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);display:flex;justify-content:space-between;margin-bottom:5px;}
  .pop .plab b{color:var(--ink);font-family:var(--mono);}
  .pop input[type=range]{width:100%;margin:0;accent-color:#64748b;}
  .pop .cbrow{display:flex;align-items:center;gap:6px;margin-top:9px;font-size:10px;color:var(--muted);cursor:pointer;user-select:none;}
  .pop .cbrow input{margin:0;accent-color:#64748b;cursor:pointer;}
  .pop .scale{display:flex;justify-content:space-between;margin-top:4px;font-size:9px;color:var(--muted);}
  .node.comb{cursor:pointer;}
  .node.comb .nnum{border-bottom:1.5px dotted #94a3b8;display:inline-block;padding:0 2px;border-radius:2px;}
  .node.comb .nnum:hover{background:#eef2ff;border-bottom-color:#6366f1;}

  /* up-connection (climb back to the parent) */
  .upstub{position:absolute;z-index:0;display:flex;flex-direction:column;align-items:center;cursor:pointer;will-change:opacity;}
  .upstub .arrow{font-size:11px;color:var(--muted);line-height:1;margin-bottom:1px;}
  .upstub .line{flex:1;border-left:1.6px dashed #94a3b8;}
  .upstub:hover .arrow{color:var(--ink);}
  .upstub:hover .line{border-left-color:#6366f1;}

</style>
</head>
<body>
<div class="stage" id="stage"></div>

<script>
  let focusId='0';      // current view's root ("0" = the original claim)
  let showOdds=false;
  let isFlipping=false;
  let flipToken=0;
  const overrides={};
  const associations={};
  const FLIP_MS=1000;
  const FLIP_EASE='cubic-bezier(.2,.72,.17,1)';
  const WORLD_W=2400, WORLD_H=760;
  const WORLD_ORIGIN={x:1200,y:72};
  const WORLD_STEP={x:150,y:132};
  const WORLD_PARENT_STEP={x:300,y:132};
  const WORLD_RATIO=.9;
  const WORLD_X_RATIO=.5;
  const WORLD_Y_RATIO=.9;
  const VIEW_SIZE={w:712,h:355,top:42,parentTop:50};
  const NODE_SIZE={w:140,h:54};

  // Built procedurally so every branch has structure all the way down (no single long spine).
  // The top three tiers are fixed to keep the default opening view (a pair under the left
  // subclaim, a triple under the right); below that, every subclaim grows bushy children.
  const INITIAL_DATABASE=(function buildDatabase(){
    const nodes={};
    const rnd=s=>{let h=2166136261;for(let i=0;i<s.length;i++){h=((h^s.charCodeAt(i))*16777619)>>>0;}return (h>>>8)/16777216;};
    const roleChar=id=>id[id.length-1]==='R'?'refute':'support';
    const leafVal=id=>{
      let net=0; for(let i=1;i<id.length;i++){const c=id[i];if(c==='L')net++;else if(c==='R')net--;}
      const v=50+net*6+Math.round((rnd(id+'#v')-0.5)*16);  // lean by path (support vs refute) + noise
      const base=Math.max(10,Math.min(90,v));
      return Math.min(98,base+11);
    };
    const associationVal=id=>id.length<=2?0:(rnd(id+'#association')<0.5?0:1);
    const floodLabels={
      '0':'Netherlands will experience a massive flood before 2035',
      '0L':'Flood risk is rising',
      '0LL':'Sea level trend',
      '0LR':'Extreme rain risk',
      '0LRL':'Storm surge risk',
      '0LRR':'River peak risk',
      '0LRLL':'North Sea storms',
      '0LRLR':'Higher tides',
      '0LRRL':'Rhine discharge',
      '0LRRR':'Meuse discharge',
      '0R':'Walls will weaken',
      '0RL':'Dikes may be exceeded',
      '0RM':'Delta Works have limits',
      '0RR':'Maintenance gaps',
      '0RLL':'Inspections may miss risk',
      '0RLR':'Upgrades may lag',
      '0RLLL':'Primary dikes at risk',
      '0RLLR':'Coastal dunes weaken',
      '0RLRL':'Climate budget lags',
      '0RLRR':'Water boards constrained',
      '0LRLLL':'Storm records',
      '0LRLLR':'Tide gauges',
      '0LRLRL':'Sea-level data',
      '0LRLRR':'Subsidence data',
      '0LRRLL':'Rhine models',
      '0LRRLR':'Rainfall trends',
      '0LRRRL':'Meuse models',
      '0LRRRR':'Soil saturation',
      '0RLLLL':'Dike reports flag risk',
      '0RLLLR':'Inspection gaps',
      '0RLLRL':'Sand nourishment gaps',
      '0RLLRR':'Barrier test concerns',
      '0RLRLL':'Budget plans lag',
      '0RLRLR':'Upgrade tenders lag',
      '0RLRRL':'Board minutes show strain',
      '0RLRRR':'Pump capacity limited'
    };
    function grow(id,depth){
      // every node branches into 2 (sometimes 3) children that branch further; only the
      // deepest level (and the occasional early node) becomes a source leaf — never a thin spine.
      if(depth<=0 || (depth<=3 && rnd(id+'#leaf')<0.28)){
        nodes[id]={role:roleChar(id),value:leafVal(id),source:true};
        return;
      }
      const chars=rnd(id+'#t')<0.24?['L','M','R']:['L','R'];
      const kids=chars.map(c=>id+c);
      nodes[id]={role:roleChar(id),children:kids,association:associationVal(id)};
      kids.forEach(k=>grow(k,depth-1));
    }
    function makeSource(id){
      nodes[id]={role:roleChar(id),value:leafVal(id),source:true};
    }
    function pruneCrowdedTriples(){
      let changed=true;
      while(changed){
        changed=false;
        Object.entries(nodes).forEach(([,node])=>{
          const kids=node.children || [];
          if(kids.length<3) return;
          const branchingKids=kids.filter(child=>(nodes[child]?.children || []).length>0);
          if(branchingKids.length<2) return;
          branchingKids.forEach(child=>{
            if((nodes[child]?.children || []).length>=3){
              makeSource(child);
              changed=true;
            }
          });
        });
      }
    }
    nodes['0']={kind:'claim',label:'Claim',children:['0L','0R'],association:0};
    nodes['0L']={role:'support',children:['0LL','0LR'],association:0};
    nodes['0R']={role:'refute',children:['0RL','0RM','0RR'],association:0};
    nodes['0LL']={role:'support',value:67.5,source:true};
    nodes['0RM']={role:'refute',value:53.01,source:true};
    grow('0LR',6);
    grow('0RL',6);
    grow('0RR',6);
    pruneCrowdedTriples();
    nodes['0RR']={role:'refute',value:18.02,source:true};
    Object.entries(floodLabels).forEach(([id,label])=>{
      if(nodes[id]) nodes[id].label=label;
    });
    return {rootId:'0',nodes};
  })();

  const DB_PARENTS={};
  Object.entries(INITIAL_DATABASE.nodes).forEach(([id,node])=>{
    (node.children || []).forEach(child=>{DB_PARENTS[child]=id;});
  });

  function dbNode(id){return INITIAL_DATABASE.nodes[id];}
  function parentId(id){return DB_PARENTS[id] || null;}
  function childrenOf(id){return dbNode(id)?.children || [];}
  function hasChildren(id){return childrenOf(id).length>0;}

  Object.entries(INITIAL_DATABASE.nodes).forEach(([id,node])=>{
    if((node.children || []).length>=2) associations[id]=node.association ?? 0;
  });

  function oddsLabelFromOdds(odds){
    const n=odds>=1?odds:1/odds;
    const text=n>=100?String(Math.round(n)):n>=10?String(Math.round(n)):n.toFixed(1);
    return odds>=1?text+' / 1':'1 / '+text;
  }
  function fmt(f,odds=null){return showOdds?oddsLabelFromOdds(odds ?? percentToOdds(f)):f+'%';}

  function commonPrefixId(a,b){
    let i=0, n=Math.min(a.length,b.length);
    while(i<n && a[i]===b[i]) i++;
    return a.slice(0,Math.max(1,i));
  }

  function branchOffset(step){
    return step==='L'?-1:step==='R'?1:0;
  }

  function associationFor(id){return id in associations?associations[id]:0;}
  const MULTIPLY_SPREAD=1.18;
  function branchSpread(parentId,useAssociation){
    return useAssociation?MULTIPLY_SPREAD-.55*associationFor(parentId):MULTIPLY_SPREAD;
  }
  const TRIPLE_STEP=104;           // horizontal spacing between triple subclaims (was 90)
  const TRIPLE_NODE_SCALE=.84;     // triple subclaims render a bit smaller
  function isTripleMember(id){ const p=parentId(id); return !!p && childrenOf(p).length>=3; }
  function nodeScaleMul(id){ return isTripleMember(id)?TRIPLE_NODE_SCALE:1; }
  function branchStep(parentId,xStep){
    const secondLayerStep=WORLD_STEP.x*WORLD_X_RATIO;
    return childrenOf(parentId).length>=3 && Math.abs(xStep-secondLayerStep)<.001 ? TRIPLE_STEP : xStep;
  }

  function walkDown(pos,startId,path,firstStepX=WORLD_STEP.x){
    let xStep=firstStepX, yStep=WORLD_STEP.y;
    let current=startId;
    for(let i=0;i<path.length;i++){
      const step=path[i];
      pos.x+=branchOffset(step)*branchStep(current,xStep)*branchSpread(current,i===path.length-1);
      pos.y+=yStep;
      pos.scale*=WORLD_RATIO;
      current+=step;
      xStep*=WORLD_X_RATIO;
      yStep*=WORLD_Y_RATIO;
    }
  }

  function walkUp(pos,startId,path){
    let xStep=WORLD_PARENT_STEP.x, yStep=WORLD_PARENT_STEP.y;
    for(let i=path.length-1;i>=0;i--){
      const step=path[i];
      const parent=startId.slice(0,startId.length-path.length+i);
      pos.x-=branchOffset(step)*branchStep(parent,xStep)*branchSpread(parent,i===path.length-1);
      pos.y-=yStep;
      pos.scale/=WORLD_RATIO;
      xStep*=WORLD_X_RATIO;
      yStep*=WORLD_Y_RATIO;
    }
  }

  function worldPx(id,layoutRoot=focusId){
    const common=commonPrefixId(id,layoutRoot);
    const pos={x:WORLD_ORIGIN.x,y:WORLD_ORIGIN.y,scale:1};
    walkUp(pos,layoutRoot,layoutRoot.slice(common.length));
    const firstStepX=common===parentId(layoutRoot)?WORLD_PARENT_STEP.x:WORLD_STEP.x;
    walkDown(pos,common,id.slice(common.length),firstStepX);
    return pos;
  }

  function idsForSubtree(rootId,levels){
    const ids=[rootId];
    let layer=[rootId];
    for(let depth=0;depth<levels;depth++){
      const next=[];
      layer.forEach(id=>{ next.push(...childrenOf(id)); });
      ids.push(...next);
      layer=next;
    }
    return ids;
  }

  function edgeSet(ids){
    const visible=new Set(ids), edges=new Set();
    ids.forEach(id=>{
      const par=parentId(id);
      if(par && visible.has(par)) edges.add(id+'>'+par);
    });
    return edges;
  }

  function markerSet(ids){
    const visible=new Set(ids), markers=new Set();
    ids.forEach(id=>{
      if(dbNode(id)?.source || !hasChildren(id)) return;
      if(childrenOf(id).some(child=>visible.has(child))) return;
      markers.add(id);
    });
    return markers;
  }

  function transitionFade(oldId,newId){
    const oldIds=idsForView([oldId],oldId);
    const newIds=idsForView([newId],newId);
    return {
      oldId,newId,
      oldIds:new Set(oldIds),
      newIds:new Set(newIds),
      oldEdges:edgeSet(oldIds),
      newEdges:edgeSet(newIds),
      oldMarkers:markerSet(oldIds),
      newMarkers:markerSet(newIds),
      oldUp:!!parentId(oldId),
      newUp:!!parentId(newId)
    };
  }

  function fadeAmount(oldSet,newSet,key,t){
    const was=oldSet.has(key), is=newSet.has(key);
    if(was && is) return 1;
    if(was) return 1-t;
    if(is) return t;
    return 1;
  }

  function nodeFade(id,fade,t){
    return fade?fadeAmount(fade.oldIds,fade.newIds,id,t):1;
  }

  function roleFromPercent(f){return f>=50?'support':'refute';}
  function kindFor(id){
    const node=dbNode(id) || {};
    return node.kind==='claim'?'claim':node.source?'source-sub':'sub';
  }
  function roleFor(id){
    const node=dbNode(id);
    if(!node || node.kind==='claim') return node?.role || null;
    return roleFromPercent(forVal(id));
  }
  function labelFor(id,kind,f){
    const meta=dbNode(id) || {};
    if(meta.label) return meta.label;
    if(kind==='claim') return 'Claim';
    return kind==='source-sub'?'Illustrative source':'Illustrative subclaim';
  }

  function cameraFrame(rootId,layoutRoot=rootId){
    const p=worldPx(rootId,layoutRoot), scale=p.scale;
    const top=parentId(rootId)?VIEW_SIZE.parentTop:VIEW_SIZE.top;
    return {
      x:p.x-(VIEW_SIZE.w*scale)/2,
      y:p.y-(top*scale),
      w:VIEW_SIZE.w*scale,
      h:VIEW_SIZE.h*scale
    };
  }

  function cameraForFrame(frame){
    const stage=document.getElementById('stage');
    const fit=Math.min(stage.clientWidth/frame.w,stage.clientHeight/frame.h);
    const tx=(stage.clientWidth-frame.w*fit)/2-frame.x*fit;
    const ty=(stage.clientHeight-frame.h*fit)/2-frame.y*fit;
    return {tx,ty,scale:fit};
  }

  function cameraTransformForFrame(frame){
    const c=cameraForFrame(frame);
    return `translate(${c.tx}px,${c.ty}px) scale(${c.scale})`;
  }

  function cameraTransform(rootId,layoutRoot=rootId){
    return cameraTransformForFrame(cameraFrame(rootId,layoutRoot));
  }

  function lerp(a,b,t){return a+(b-a)*t;}
  function easeCamera(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
  function mixFrame(a,b,t){
    return {
      x:lerp(a.x,b.x,t),
      y:lerp(a.y,b.y,t),
      w:lerp(a.w,b.w,t),
      h:lerp(a.h,b.h,t)
    };
  }

  function mixPose(a,b,t){
    return {
      x:lerp(a.x,b.x,t),
      y:lerp(a.y,b.y,t),
      scale:lerp(a.scale,b.scale,t)
    };
  }

  function layoutForIds(ids,fromRoot,toRoot,t){
    const layout={};
    ids.forEach(id=>{ layout[id]=mixPose(worldPx(id,fromRoot),worldPx(id,toRoot),t); });
    return layout;
  }

  function applyUpstubFade(fade,t){
    document.querySelectorAll('.upstub').forEach(up=>{
      const mode=up.dataset.fadeMode;
      up.style.opacity=!fade || !mode || mode==='stable'?1:mode==='in'?t:1-t;
    });
  }

  function applyLayout(ids,layout,fade=null,fadeT=1){
    ids.forEach(id=>{
      const el=document.querySelector(`.node[data-id="${id}"]`);
      const p=layout[id];
      if(!el || !p) return;
      el.style.left=p.x+'px';
      el.style.top=p.y+'px';
      el.style.setProperty('--node-scale',p.scale*nodeScaleMul(id));
      el.style.opacity=nodeFade(id,fade,fadeT);
    });
    drawWorldWires(ids,layout,fade,fadeT);
    applyUpstubFade(fade,fadeT);
  }

  function animateCamera(world,ids,fromRoot,toRoot,fromFrame,toFrame,token,fade=null){
    world.style.transform=cameraTransformForFrame(fromFrame);
    applyLayout(ids,layoutForIds(ids,fromRoot,toRoot,0),fade,0);
    requestAnimationFrame(()=>{
      const start=performance.now();
      const step=now=>{
        if(!isFlipping || token!==flipToken) return;
        const raw=Math.min(1,(now-start)/FLIP_MS);
        const eased=easeCamera(raw);
        applyLayout(ids,layoutForIds(ids,fromRoot,toRoot,eased),fade,raw);
        world.style.transform=cameraTransformForFrame(mixFrame(fromFrame,toFrame,eased));
        if(raw<1) requestAnimationFrame(step);
        else finishWorldMove(token);
      };
      requestAnimationFrame(step);
    });
  }
  function basePercent(id){return id in overrides?overrides[id]:(dbNode(id)?.value ?? 50);}
  function percentToOdds(percent){
    const p=Math.max(.000001,Math.min(.999999,percent/100));
    return p/(1-p);
  }
  function percentFromOdds(odds){
    if(!Number.isFinite(odds)) return 100;
    return odds/(1+odds)*100;
  }
  function oddsFor(id,memo={}){
    if(id in memo) return memo[id];
    const kids=childrenOf(id);
    let odds;
    if(kids.length>=2){
      const alpha=associationFor(id), W=kids.length;
      const signal=kids.reduce((acc,child)=>acc+Math.log(oddsFor(child,memo)),0);
      odds=Math.exp(signal/(1+alpha*(W-1)));
    }else{
      odds=percentToOdds(basePercent(id));
    }
    memo[id]=odds;
    return odds;
  }
  function forVal(id){return Math.round(percentFromOdds(oddsFor(id)));}
  function closePops(){
    document.querySelectorAll('.pop.open').forEach(p=>p.classList.remove('open'));
    document.querySelectorAll('.node.popover-open').forEach(n=>n.classList.remove('popover-open'));
  }
  document.addEventListener('click',closePops);

  function updateNodeVisual(el,id){
    const kind=kindFor(id), exactOdds=oddsFor(id), f=Math.round(percentFromOdds(exactOdds)), n=el.querySelector('.nnum'), t=el.querySelector('.ntype');
    if(t) t.textContent=labelFor(id,kind,f);
    if(n){
      n.textContent=fmt(f,exactOdds);
      n.classList.toggle('pos',f>=50);
      n.classList.toggle('neg',f<50);
    }
    const role=kind==='claim'?null:roleFromPercent(f);
    el.classList.toggle('support',role==='support');
    el.classList.toggle('refute',role==='refute');
  }

  function makeNode(id,kind,activeFocus){
    const el=document.createElement('div');
    el.className='node '+(kind==='claim'?'claim':kind==='source-sub'?'sub src':'sub');
    el.dataset.id=id;
    el.innerHTML='<div class="ntype"></div><div class="nnum"></div>';
    updateNodeVisual(el,id);
    const focused=id===activeFocus;
    if((kind==='sub' || kind==='source-sub') && hasChildren(id) && !focused){
      el.classList.add('nav');
      el.addEventListener('click',e=>{e.stopPropagation();transitionTo(id);});
    }
    if(focused && hasChildren(id)){
      wireAssociation(el,id);
    }
    if(kind==='source-sub'){
      wireSource(el,id);
    }
    return el;
  }

  function wireAssociation(el,id){
    const num=el.querySelector('.nnum');
    const pop=document.createElement('div'); pop.className='pop';
    pop.innerHTML=`<div class="plab"><span>association</span><b></b></div>
      <input type="range" min="0" max="1" step="0.01">
      <div class="scale"><span>multiply</span><span>log avg</span></div>
      <label class="cbrow"><input type="checkbox"><span>show odds</span></label>`;
    el.appendChild(pop);
    el.classList.add('comb');
    const val=pop.querySelector('b'), sl=pop.querySelector('input[type=range]'), cb=pop.querySelector('input[type=checkbox]');
    const head=()=>{ val.textContent=Math.round(associationFor(id)*100)+'%'; };
    sl.addEventListener('click',e=>e.stopPropagation());
    sl.addEventListener('input',e=>{ associations[id]=Number(e.target.value); head(); refreshNumbers(); refreshWorldLayout(); });
    cb.addEventListener('click',e=>e.stopPropagation());
    cb.addEventListener('change',()=>{ showOdds=cb.checked; refreshNumbers(); });
    const openEditor=e=>{ e.stopPropagation(); if(isFlipping) return; closePops();
      sl.value=associationFor(id); cb.checked=showOdds; head(); el.classList.add('popover-open'); pop.classList.add('open'); };
    num.addEventListener('click',openEditor);
    el.addEventListener('click',openEditor);
    pop.addEventListener('click',e=>e.stopPropagation());
  }

  function wireSource(el,id){
    const num=el.querySelector('.nnum');
    const pop=document.createElement('div'); pop.className='pop';
    pop.innerHTML=`<div class="plab"><span>chance</span><b></b></div>
      <input type="range" min="2" max="98" step="1">
      <label class="cbrow"><input type="checkbox"><span>show odds</span></label>`;
    el.appendChild(pop);
    const val=pop.querySelector('b'), sl=pop.querySelector('input[type=range]'), cb=pop.querySelector('input[type=checkbox]');
    const head=()=>{ pop.querySelector('.plab span').textContent=showOdds?'for : against':'chance'; val.textContent=fmt(forVal(id),oddsFor(id)); };
    sl.addEventListener('click',e=>e.stopPropagation());
    sl.addEventListener('input',e=>{ overrides[id]=parseInt(e.target.value); head(); refreshNumbers(); refreshWorldLayout(); });
    cb.addEventListener('click',e=>e.stopPropagation());
    cb.addEventListener('change',()=>{ showOdds=cb.checked; head(); refreshNumbers(); });
    const openEditor=e=>{ e.stopPropagation(); closePops();
      sl.value=basePercent(id); cb.checked=showOdds; head(); el.classList.add('popover-open'); pop.classList.add('open'); };
    num.addEventListener('click',openEditor);
    el.addEventListener('click',openEditor);
    pop.addEventListener('click',e=>e.stopPropagation());
  }

  function refreshNumbers(){   // re-text all numbers in place (format flip / source edit) without rebuilding
    document.querySelectorAll('#tree .node').forEach(el=>{
      updateNodeVisual(el,el.dataset.id);
    });
  }

  function refreshWorldLayout(){
    if(isFlipping || !document.getElementById('world')) return;
    const ids=idsForView([focusId],focusId);
    applyLayout(ids,layoutForIds(ids,focusId,focusId,1));
    document.getElementById('world').style.transform=cameraTransform(focusId,focusId);
    const up=document.querySelector('.upstub');
    if(up && parentId(focusId)) up.style.height=Math.max(52,nodeTopInStage(focusId,focusId,focusId)-5)+'px';
  }

  function transitionTo(nextId){
    if(isFlipping || nextId===focusId) return;
    closePops();
    const oldId=focusId;
    const token=++flipToken;
    isFlipping=true;
    const ids=idsForView([oldId,nextId],nextId,2);
    const fade=transitionFade(oldId,nextId);
    renderWorld([oldId,nextId],nextId,oldId,2,fade,0);
    document.getElementById('stage').classList.add('is-flipping');
    const world=document.getElementById('world');
    const fromFrame=cameraFrame(oldId,oldId);
    const toFrame=cameraFrame(nextId,nextId);
    focusId=nextId;
    animateCamera(world,ids,oldId,nextId,fromFrame,toFrame,token,fade);
  }

  function finishWorldMove(token){
    if(!isFlipping || token!==flipToken) return;
    isFlipping=false;
    document.getElementById('stage').classList.remove('is-flipping');
    render();
  }

  function render(){
    renderWorld([focusId],focusId);
    document.getElementById('world').style.transform=cameraTransform(focusId,focusId);
  }

  function idsForView(focuses,activeFocus,backDepth=1){
    const ids=new Set();
    focuses.forEach(id=>idsForSubtree(id,3).forEach(child=>ids.add(child)));
    let ctx=activeFocus;
    for(let depth=0;depth<backDepth;depth++){
      const par=parentId(ctx);
      if(!par) break;
      ids.add(par);
      if(depth===0) childrenOf(par).forEach(child=>ids.add(child));
      ctx=par;
    }
    return [...ids].sort((a,b)=>a.length-b.length || a.localeCompare(b));
  }

  function nodeTopInStage(id,layoutRoot,frameRoot){
    const p=worldPx(id,layoutRoot);
    const c=cameraForFrame(cameraFrame(frameRoot,layoutRoot));
    return p.y*c.scale+c.ty-(NODE_SIZE.h*p.scale*c.scale)/2;
  }

  function addUpstub(stage,id,layoutRoot,frameRoot,mode='stable',fadeT=1){
    const par=parentId(id);
    if(!par) return;
    const up=document.createElement('div'); up.className='upstub';
    const h=Math.max(52,nodeTopInStage(id,layoutRoot,frameRoot)-5);
    up.dataset.fadeMode=mode;
    up.style.opacity=mode==='in'?fadeT:mode==='out'?1-fadeT:1;
    up.style.left='calc(50% - 9px)'; up.style.top='0px'; up.style.width='18px'; up.style.height=h+'px';
    up.innerHTML='<div class="arrow">&#9650;</div><div class="line"></div>';
    up.title='back to the parent claim';
    up.addEventListener('click',e=>{ e.stopPropagation(); transitionTo(par); });
    stage.appendChild(up);
  }

  function renderWorld(focuses,activeFocus,layoutRoot=activeFocus,backDepth=1,fade=null,fadeT=1){
    const stage=document.getElementById('stage');
    stage.innerHTML='<div class="world" id="world"><svg id="wires" xmlns="http://www.w3.org/2000/svg"></svg><div class="tree" id="tree"></div></div>';
    const tree=document.getElementById('tree');
    const ids=idsForView(focuses,activeFocus,backDepth);

    ids.forEach(id=>{
      const node=dbNode(id);
      if(!node) return;
      const kind=kindFor(id);
      const n=makeNode(id,kind,activeFocus);
      const p=worldPx(id,layoutRoot);
      n.style.left=p.x+'px';
      n.style.top=p.y+'px';
      n.style.setProperty('--node-scale',p.scale*nodeScaleMul(id));
      if(id===activeFocus) n.classList.add('focused');
      n.style.opacity=nodeFade(id,fade,fadeT);
      tree.appendChild(n);
    });

    drawWorldWires(ids,layoutForIds(ids,layoutRoot,layoutRoot,1),fade,fadeT);

    if(fade){
      if(fade.oldUp) addUpstub(stage,fade.oldId,layoutRoot,fade.oldId,'out',fadeT);
      if(fade.newUp) addUpstub(stage,fade.newId,layoutRoot,fade.newId,'in',fadeT);
    }else{
      addUpstub(stage,activeFocus,layoutRoot,activeFocus);
    }
  }

  function drawWorldWires(ids,layout,fade=null,fadeT=1){
    const svg=document.getElementById('wires');
    svg.setAttribute('viewBox',`0 0 ${WORLD_W} ${WORLD_H}`);
    svg.setAttribute('preserveAspectRatio','none');
    const visible=new Set(ids);
    const C=id=>{
      const p=layout[id], h=NODE_SIZE.h*p.scale*nodeScaleMul(id);
      return {x:p.x,top:p.y-h/2,bot:p.y+h/2,scale:p.scale};
    };
    const teal='#0f766e', amber='#b45309';
    const color={support:teal,refute:amber};
    let s='';
    const curve=(a,b,col,op=1)=>{ if(op<=.01) return; const my=(a.top+b.bot)/2, sw=Math.max(.7,1.6*a.scale), arrow=Math.max(2.4,4*b.scale);
      s+=`<path d="M${a.x},${a.top} C${a.x},${my} ${b.x},${my} ${b.x},${b.bot}" fill="none" stroke="${col}" stroke-width="${sw}" opacity="${.78*op}"/>`;
      s+=`<polygon points="${b.x},${b.bot} ${b.x-arrow},${b.bot+arrow*1.5} ${b.x+arrow},${b.bot+arrow*1.5}" fill="${col}" opacity="${.9*op}"/>`; };
    ids.forEach(id=>{
      const par=parentId(id);
      if(!par || !visible.has(par)) return;
      const op=fade?fadeAmount(fade.oldEdges,fade.newEdges,id+'>'+par,fadeT):1;
      curve(C(id),C(par),color[roleFor(id)],op);
    });
    ids.forEach(id=>{
      if(dbNode(id)?.source || !hasChildren(id)) return;
      if(childrenOf(id).some(child=>visible.has(child))) return;
      const op=fade?fadeAmount(fade.oldMarkers,fade.newMarkers,id,fadeT):1;
      if(op<=.01) return;
      const p=layout[id], col=color[roleFor(id)] || teal, len=34*p.scale;
      [-1,1].forEach(side=>{
        const dx=18*p.scale*side, y0=p.y+NODE_SIZE.h*p.scale*nodeScaleMul(id)/2;
        s+=`<path d="M${p.x+dx*.35},${y0} L${p.x+dx},${y0+len}" stroke="${col}" stroke-width="${Math.max(.6,1.1*p.scale)}" opacity="${.35*op}" fill="none"/>`;
      });
    });
    svg.innerHTML=s;
  }

  function drawWires(view){
    const stage=document.getElementById('stage'), svg=document.getElementById('wires');
    const sr=stage.getBoundingClientRect();
    svg.setAttribute('viewBox',`0 0 ${sr.width} ${sr.height}`); svg.setAttribute('preserveAspectRatio','none');
    const C=id=>{const r=document.querySelector(`.node[data-id="${id}"]`).getBoundingClientRect();
      return {x:r.left+r.width/2-sr.left, top:r.top-sr.top, bot:r.bottom-sr.top};};
    const teal='#0f766e', amber='#b45309';
    const color={support:teal,refute:amber};
    let s='';
    const curve=(a,b,col)=>{ const my=(a.top+b.bot)/2;
      s+=`<path d="M${a.x},${a.top} C${a.x},${my} ${b.x},${my} ${b.x},${b.bot}" fill="none" stroke="${col}" stroke-width="1.6" opacity=".8"/>`;
      s+=`<polygon points="${b.x},${b.bot} ${b.x-4},${b.bot+6} ${b.x+4},${b.bot+6}" fill="${col}"/>`; };
    view.links.forEach(link=>curve(C(link.from),C(link.to),color[link.role]));
    // off-screen branches under the bottom subclaims
    view.offscreen.forEach(spec=>{ const c=C(spec.id), col=color[spec.role];
      [-9,9].forEach(dx=>{ s+=`<path d="M${c.x+dx*0.45},${c.bot} L${c.x+dx},${c.bot+24}" stroke="${col}" stroke-width="1.4" opacity=".5" fill="none"/>`; }); });
    svg.innerHTML=s;

    // up-connection to the parent (HTML overlay so it's clickable)
    const par=parentId(view.rootId);
    if(par){
      const f=C(view.rootId);
      const up=document.createElement('div'); up.className='upstub';
      up.style.left=(f.x-9)+'px'; up.style.top='0px'; up.style.width='18px'; up.style.height=f.top+'px';
      up.innerHTML='<div class="arrow">▲</div><div class="line"></div>';
      up.title='back to the parent claim';
      up.addEventListener('click',e=>{ e.stopPropagation(); transitionTo(par); });
      stage.appendChild(up);
    }
  }

  window.addEventListener('resize',()=>{ if(!isFlipping) render(); });
  render();
</script>
</body>
</html>

```

This graph uses a simple formula, we will walk through this formula in the case of the main claim in its default values. First we need to convert the percentages into odds. We have two subclaims the first subclaim has 86% certainty and the second subclaim has 38%.

$$
86\% \Rightarrow O_1=\frac{86}{14}\approx 6.14 / 1 \qquad;\qquad 38\% \Rightarrow O_2=\frac{38}{62}\approx 1 / 1.63
$$

Then we need to know the association between the two sources. If they are independent we should treat them as separate tests and multiply the odds. If they are not we need to average them by taking the square root after multiplying this property holds in this general formula.

$$
O_{\text{claim}} = \left(O_1 O_2\right)^{\frac{1}{1+a}}
$$

In our top claim case we have two independent claims so a is zero and $\frac{1}{1+a} = \frac{1}{1+0} = 1$  
Then we can feel in our odds into the formula.

$$
O_{\text{claim}} = \left(\frac{6.14}{1}\cdot\frac{1}{1.63}\right)^1 = \left(\frac{6.14}{1.63}\right)^1 = 3.77 / 1 \approx 3.8 / 1
$$

This gives us the final odds of the final claim and we can convert those back into percentages.

$$
P_{\text{claim}} = \frac{O_{\text{claim}}}{1+O_{\text{claim}}} = \frac{3.77}{1+3.77} = \frac{3.77}{4.77} \approx 0.79 = 79\%
$$

This same process gets propagated throughout the entire graph allowing for the claim to be supported by every piece of knowledge below it. If you're interested why this formula was chosen I invite you to follow along with the math on the block below. The article is intended to be possible to follow even if you didn't read that part.

It is important to note that this way of combining odds does assume that each subclaim and source moves their parent claim by exactly the same force as how likely they are to be true. This is a simplification made to allow for this example to be easier to follow along with. In the final version every node will separate the confidence in the claim from the force of each subclaim on their parent.

+++ Following along with the math

In the specific case above we showed how to combine two odds. I will start off with showing how this formula generalizes. First I show the two cases used in the widget for 2 and 3 claims.

$$
O_{\text{claim}} = \left(O_1 O_2\right)^{\frac{1}{1+a}} \qquad;\qquad O_{\text{claim}} = \left(O_1 O_2 O_3\right)^{\frac{1}{1+2a}}
$$

  

If you're observant you might have noticed the pattern already. This pattern can be extend to allow a claim to have any number of subclaims.

$$
O_{\text{claim}} = \left(\prod_{i=1}^{n} O_i\right)^{\frac{1}{1+a(n-1)}}
$$

This formula might feel pulled out of thin air. To show where It comes from I will go back to the beginning.

An introduction to Bayes
------------------------

This article will be using a lot of the terminology of [Bayesian statistics](https://en.wikipedia.org/wiki/Bayes%27_theorem). If you have never seen Bayesian statistics before or want to catch up, I can recommend [this](https://www.youtube.com/watch?v=HZGCoVF3YvM&list=PLiAulSm0XXgvCGe63mrAkda9UQ9478YQv) excellent series from 3Blue1Brown. If instead you want a small reminder I will try to build up to it from fundamentals.

In these equations P(X) is intended to mean the probability of X. So if I toss a coin "P(heads) = 50%"  
translates to "The probability that I toss heads is 50%".

In these equations a | is intended to signal a "given that". So "P(Heads|cheating) = 100%" translates to "The probability that I toss heads given that I am cheating is 100%".

These definitions together allow us to build up to out first equation:

$$
P(B)P(A\mid B)=P(A\text{ and }B)=P(A)P(B\mid A)
$$

This equations shows that the probability of A and B being true can be restated as the probability of B being true multiplied by the probability of A given that B. It can also be restated as the probability of A multiplied by the probability of B given A. Below you can see a visual proof where the green area represents this constant area.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781434001/lexical_client_uploads/dzjgajeyf8ldjqzpypxl.png)

Below instead of A and B we will use H and E. H represents the Hypothesis and E represents the evidence. So in this case P(H|E) represents the probability of the Hypothesis given the evidence. P(E|H) represents the probability of the evidence given the hypothesis.

$$
P(E)P(H\mid E)=P(H)P(E\mid H)
$$

  
Once we have this formula we can construct the core Bayes formula by dividing both sides by P(E).

$$
P(H \mid E) = \frac{P(E \mid H)\,P(H)}{P(E)}
$$

This is the core Bayesian formula. It allows us to calculate what our hypothesis H should be given the evidence E. The only problem with this formula is that it can not easily integrate multiple pieces of evidence. For that we will need to do a slight rewrite.

We can go through the same reasoning for P($\neg$H|E). For this we use $\neg$ symbol to mean not. P($\neg$H) is the probability that H is not true. This gives us an almost identical equation.

$$
P(\lnot H \mid E) = \frac{P(E \mid \lnot H)\,P(\lnot H)}{P(E )}
$$

We can divide the above two formula's. Once we have done this we can simplify away the P(E)

$$
\frac{P(H \mid E)}{P(\lnot H \mid E)} = \frac{\dfrac{P(E \mid H)\,P(H)}{P(E)}}{\dfrac{P(E \mid \lnot H)\,P(\lnot H)}{P(E)}} = \frac{P(E \mid H)\,P(H)}{P(E \mid \lnot H)\,P(\lnot H)}
$$

If this is all going a bit fast I can strongly recommend [this](https://www.youtube.com/watch?v=lG4VkPoG3ko) 3Blue1Brown video. Once we have done this change we can cleanly separate this formula into three parts: The posterior odds, the likelihood ratio and the prior odds.

$$
\underbrace{\frac{P(H \mid E)}{P(\lnot H \mid E)}}_{\text{posterior odds}} \;=\; \underbrace{\frac{P(E \mid H)}{P(E \mid \lnot H)}}_{\text{likelihood ratio } (LR)} \;\times\; \underbrace{\frac{P(H)}{P(\lnot H)}}_{\text{prior odds}}
$$

Finally we can simplify the combination of the percentage of something happening divided by the probability of the opposite as the odds. For example 10% can be expressed as 10 to 90 odds and 50% can be expressed as 1 to 1 odds. For the mathematics of expectations odds can more easily represent changes in belief than probability, shown by the examples below.

$$
\underbrace{O(H \mid E)}_{\text{posterior odds}} \;=\; \underbrace{LR}_{\text{likelihood ratio }} \;\times\; \underbrace{O(H)}_{\text{prior odds}}
$$

Below I will show how to use this with three examples. Every time I will normalize the odds to a total of 100 allowing quick conversion to percentages, in the real program this is calculated in odds allowing for quick and accurate measurement.

1.  Weather forecasting: Tomorrow I am going to go camping, Id live to know if its going to rain. In my country the prior odds of it raining are 20 to 80, or 20%.  
    I look at the weather forecast, their forecasts have a likelihood ratio of 90 to 10, or 90%. That means that the weather forecast is correct 90 times for every 10 times it is wrong.  
    The way to calculate my posterior expectation of having rain tomorrow is to multiply 20/80 with 90/10 or (20/80)*(90/10) = 1800/800 ≈ 69/31 or 69%.  
    This means that after checking my weather app I expect a 69 to 31 odds of rain tomorrow.
2.  Disease detection: I go to the doctor for a regular routine checkup. In my age bracket the prior odds of having heart problems is 1 to 99, or 1%.  
    I undergo a test that has a likelihood ratio of 95 to 5, or 95%. This means that the test is correct 95 times for every 5 times that it is wrong.  
    The way to calculate my posterior expectation of having heart disease after this test is simply to multiply 1/99 with 95/5 or (1/99)*(95/5) = 95/495 ≈ 16/84 or 16%.  
    This means that after this test I expect a 16 to 84 odds of having heart problems. If it surprises you that this test still means I most likely don't have heart problems then please again watch [this video](https://www.youtube.com/watch?v=lG4VkPoG3ko).
3.  Disease detection part 2: I go back to the doctor because a screening test showed that I might have heart problems . My cohort with one positive screening test show an odds of having 16 to 84 odds of having heart problems.  
    Next I undergo a really strong test that has a likelihood of 99 to 1. this means it is correct 99 times for every time it is wrong.  
    Then the posterior expectation is (16/84)*(99/1) = (1584/84) ≈ 95/5 or 95%. This shows that the two tests together are able to be strong enough to overcome the initial low likelihood.  
    

Separating out the prior and the likelihood ratio like this allows us to multiply together many tests. If we take the same 2 hart problem tests of above we could combine them into a single stronger test. We can do this by multiplying the tests giving us a combined likelihood ratio of (95/5) * (99/1) = 9405/5[^37szg3pcd4h].

To show that this gives the same result we can use this test on the original prior of 1/99 again by multiplying (9405/5)*(1/99) = 95/5 or 95%.

With this in our toolbelt we are now able to add together any amount of uncorrelated updates to our hypothesis. However in the real world we find many pieces of evidence that are correlated. We would still like to be able to use these pieces of evidence.

### Opinion pooling

In the extreme fully correlated evidence points at the same claim. One example of this is measuring temperature in the same room multiple times, in this case we just want to average out the measurements.

If we have two experts on Weather forecasting and we ask both of them if next week there will be a hurricane hitting the coast they will most likely give two separate odds. Lets look at one scenario.

The fist expert gives 99:1 odds of there being a hurricane and the other expert gives 50:50 odds of there being a hurricane. We want to add together their claims, but linearly adding the claim together would fail to take into account the extra confidence of the 99:1 odds expert. The middle ground is multiplicative averaging.

$$
O_{\text{pool}} = \sqrt{\frac{99}{1} \cdot \frac{50}{50}} = \sqrt{99 \cdot 1} = \sqrt{99} \approx 9.95
$$

This can be generalized to any combination of two odds.

$$
O_{\text{pool}} = \sqrt{O_1 \cdot O_2} = O_1^{1/2}\, O_2^{1/2}
$$

Here we can also give every expert a different weight the important part is that the total weight adds to 1. So if we give expert 1 a weight of 0.1 we need to give expert 2 a weight of 0.9.

$$
O_{\text{pool}} = O_1^{\,w_1}\, O_2^{\,w_2}, \qquad w_1 + w_2 = 1
$$

We can generalize this to any amount of experts. If you're not familiair with Π and Σ. I will explain one by one first Σ essentially says sum up, so we sum up every weight $w$ unil the final weight $i$ and we want it to sum to 1. This sum of 1 is to make sure that the percentage is bounded by the claims of the experts. We do not want to claim a higher certainty than the most certain expert. The second symbol Π says to take the product. So we multiply together every odds ratio O to the power of that experts weight, just like we have done above.

$$
O_{\text{pool}} = \prod_i O_i^{\,w_i}, \qquad \sum_i w_i = 1
$$

If in a specific case we take all weights to be the same we can conclude that this average weight must be 1/n to add up to 1 in total. This gives us.

$$
O_{\text{pool}} = \prod_{i=1}^{n} O_i^{\,1/n} = \left(\prod_{i=1}^{n} O_i\right)^{\,1/n}
$$

Combining both methods
----------------------

To combine both methods we will start by picking back up the Bayesian update

$$
\underbrace{O(H \mid E)}_{\text{posterior odds}} \;=\; \underbrace{LR}_{\text{likelihood ratio }} \;\times\; \underbrace{O(H)}_{\text{prior odds}}
$$

We can see that we can add many experiments by multiplying by the likelihood of each experiment. This gives us.  

$$
O(H \mid E_1,\dots,E_k) = O(H) \times \prod_i LR_i
$$

The final change that we need is that we can use all previous claims as experiments[^pc3ify5yixe]. This way we can see both the original odds and the likelihood ratios all as multiplied odds.

$$
O_{posterior} = \prod_i O_i = \prod_{i=1}^{n} O_i
$$

When we combine this with the opinion pool we will start to see the formula that we used. When the correlation is 0 every claim is evaluated separately and we are doing a Bayesian update and when correlation is 1 we are opinion pooling the subclaims.

$$
O_{\text{claim}} = \left(\prod_{i=1}^{n} O_i\right)^{\frac{1}{1+a(n-1)}}
$$

This odds accumulator allows for adding together many different sources and subclaims. These calculated odds can then be the input odds of a new claim.

+++

Grouping node with real world data
==================================

The core of my system I would like to call the grouping node. This grouping node is a slightly more complicated version of the subclaims above because it is also able to account for the strength of different sources on this claim. This grouping node will be shown in a bit in the form of a widget. First I will go over every part you can find in it.

The node below aims to answer the question: "What is the likelihood that the associated claim is true?". In this case the claim is: "A credible lab pathway exists for Covid". This is the value you see in the green field, by default 80%. It comes to this value by combining every piece of evidence connected to the claim.  
  
At the top you could put in a prior, or knowledge before specific sources. This prior can represent previous knowledge you believe is not represented within any sources, If you're making claims about a coin toss this prior can represent that almost all coins are fair 50/50 coins. This prior can have a strength and a specific percentage. By default it is put to 0 to say that all knowledge this node has comes form its sources.  
  
Below the prior you can see the sources. In this case S1-S7 each of these sources show the odds of the claim being true based on this specific source. These sources get multiplied like in the example above. These sources show one representational quote from the source and are a link to the source. This means that everybody who uses this tool can analyse every part of every claim and see what the result would be if one or more sources were interpreted differently.

The way to interpret the odds ratio next to each source is like an answer to the question "How often would we see this source in a world where the claim is true compared to a world where the claim is false". To give an example lets look into the claim "My coin has heads on both sides" and then we have the primary source "The coin landed heads after a toss". If the coin was fair we would expect 50% of the time heads, but if it had heads on both sides we would expect it 100%. We take the ratio between these two probabilities. This gives us 2/1 odds. So in this case It would be a supporting source with 2.0/1 odds.

To use the S5 WHO-China example. We are effectively saying "WHO-China is 1.6 times less likely to release this statement in a world with a credible lab pathway compared to a world without it". It can sometimes be impossible to know this likelihood ratio with absolute certainty. That is why this tool also gives a 90% certainty range that gets properly propagated into the output estimate.

In order for a tool like this to be at its most relevant we do need to calibrate the langage models. Here we can dig into the structured expert judgement literature Cooke, Hanea and Burgman have all spent decades calibrating different judgements. With calibration this kind of tool can go way further.

You can also change every relevant value simply by clicking and sliding the value. This is one additional way to make this knowledge tree accessible and approachable to everybody who uses it. I do not intend to have it feel like the computer just tells you the way something is. Instead I aim to show where different parts of the argument come from and how each part impacts the final claim.

Below you can see the grouping node visualized as a ledger. Every value is editable and I encourage you to try:  

```widget[8rMGD4GC368jFmDk5]
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Inside a Subclaim node — interactive</title>
<style>
  :root{
    --bg:#ffffff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0;
    --pos:#0f766e; --neg:#b45309; --prior:#334155; --track:#f1f5f9;
    --band:rgba(99,102,241,.22);
    --mono:"SFMono-Regular",ui-monospace,Menlo,Consolas,monospace;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  }
  *{box-sizing:border-box;}
  html{scrollbar-gutter:stable;overflow-x:hidden;}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);padding:32px 32px 48px;overflow-x:hidden;}
  .wrap{width:100%;max-width:820px;margin:0 auto;}
  h1{font-size:16px;font-weight:650;margin:0 0 2px;}
  .sub{font-size:18px;font-weight:400;color:var(--ink);margin:2px 0 14px;}
  .hint{font-size:11px;color:var(--muted);margin:0 0 20px;font-style:italic;}
  code{font-family:var(--mono);font-size:11px;background:var(--track);padding:1px 5px;border-radius:4px;}

  .left{width:100%;}

  /* prior card */
  .priorcard{display:inline-flex;align-items:baseline;gap:11px;background:var(--track);border:1px solid var(--line);border-radius:8px;padding:5px 11px;margin-bottom:6px;}
  .priorcard .lab{font-size:9px;color:var(--muted);letter-spacing:.06em;}
  .priorcard .pfield{font-size:11px;color:var(--muted);}           /* "strength"/"value" labels muted */
  .priorcard .pfield .ed{font-size:12.5px;font-weight:700;}
  #nCard .ed{color:var(--ink);}                                    /* strength: always ink */
  #priorCard .ed{color:var(--ink);}                                /* value: ink by default… */
  .priorcard.nzero #priorCard .ed{color:var(--muted);}             /* …muted while strength is 0 */
  .baseline{font-size:10px;color:var(--muted);margin:0 0 14px;}

  /* axis header */
  .axis{display:grid;grid-template-columns:40px minmax(0,1fr) 220px 96px;gap:8px 10px;font-size:9px;color:var(--muted);margin-bottom:6px;}
  .axis .a-zone{position:relative;text-align:center;height:12px;}
  .axis .a-srclabel{letter-spacing:.06em;text-transform:uppercase;color:var(--ink);font-weight:600;align-self:end;}
  .axis .a-srclabel span{text-transform:none;letter-spacing:0;font-weight:400;font-style:italic;}
  .axis .a-shiftlabel{font-size:7.5px;letter-spacing:.02em;text-transform:uppercase;color:var(--muted);font-weight:600;text-align:right;align-self:end;}
  .axis .a-zone .lo{position:absolute;left:0;color:var(--pos);}
  .axis .a-zone .hi{position:absolute;right:0;color:var(--neg);}
  .axis .a-zone .z{position:absolute;left:50%;transform:translateX(-50%);}

  /* rows */
  .row{display:grid;grid-template-columns:40px minmax(0,1fr) 220px 96px;gap:8px 10px;align-items:center;font-size:11.5px;padding:3px 0;}
  .chip{font-size:9.5px;font-weight:700;text-align:center;border-radius:4px;padding:3px 0;}
  .chip.pos{color:var(--pos);background:rgba(15,118,110,.12);}
  .chip.neg{color:var(--neg);background:rgba(180,83,9,.12);}
  a.srclink{color:var(--ink);text-decoration:none;overflow-wrap:anywhere;}
  a.srclink:hover{text-decoration:underline;}
  .barzone{position:relative;height:13px;}
  .barzone .axline{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:rgba(15,23,42,.35);z-index:2;}
  .bar{position:absolute;top:1px;height:11px;border-radius:3px;z-index:1;}
  .val{text-align:right;font-family:var(--mono);font-size:11px;font-weight:600;line-height:1.2;}
  .sourceci{font-size:9px;font-weight:500;color:var(--muted);margin-top:2px;white-space:normal;}
  .productrow{display:grid;grid-template-columns:40px minmax(0,1fr) 220px 96px;gap:8px 10px;align-items:center;padding:4px 0 2px;}
  .productrow .label{grid-column:2;text-align:left;font-size:10px;color:var(--muted);}
  .productrow .expr{grid-column:3 / 5;text-align:right;font-family:var(--mono);font-size:11px;font-weight:600;color:var(--ink);white-space:nowrap;}
  .productrow .pos{color:var(--pos);}
  .productrow .neg{color:var(--neg);}

  /* editable number */
  .ed{position:relative;cursor:pointer;border-bottom:1px dotted #94a3b8;padding:0 1px;border-radius:2px;}
  .ed:hover{background:#eef2ff;border-bottom-color:#6366f1;}
  .ed.pos{color:var(--pos);} .ed.neg{color:var(--neg);}
  .pop{display:none;position:absolute;z-index:30;top:108%;left:50%;transform:translateX(-50%);
       background:#fff;border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 24px rgba(15,23,42,.13);
       padding:10px 12px;width:200px;cursor:default;}
  /* invisible halo: keeps the popover open while crossing the gap or grazing past its edges.
     z-index:-1 keeps it behind the card content so it never intercepts the sliders' clicks. */
  .pop::before{content:"";position:absolute;top:-20px;left:-14px;right:-14px;bottom:-14px;background:transparent;z-index:-1;}
  .ed.editR .pop{left:auto;right:0;transform:none;}
  .ed.open .pop{display:block;}
  .pop .plab{font-size:9.5px;color:var(--muted);letter-spacing:.04em;display:flex;justify-content:space-between;margin-bottom:3px;}
  .pop .plab b{color:var(--ink);font-family:var(--mono);font-weight:600;}
  .pop input[type=range]{width:100%;margin:0 0 8px;}
  .pop input[type=range]:last-child{margin-bottom:0;}
  .pop .pnote{font-size:9px;color:var(--muted);margin-top:2px;line-height:1.35;}

  /* sigma row */
  .sigma{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);margin-top:8px;padding-top:8px;font-size:11px;color:var(--muted);}
  .sigma .net{font-family:var(--mono);color:var(--ink);font-weight:600;}

  /* posterior strip */
  .postcard{display:flex;align-items:center;gap:22px;background:rgba(15,118,110,.06);border:1px solid rgba(15,118,110,.4);border-radius:14px;padding:14px 18px;margin-top:16px;}
  .postcard .headline{flex:none;}
  .postcard .gaugewrap{flex:1;min-width:0;}
  .postcard .lab{font-size:9.5px;color:var(--muted);letter-spacing:.05em;}
  .postcard .big{font-size:42px;font-weight:800;color:var(--pos);line-height:1.05;font-variant-numeric:tabular-nums;}
  .gtrack{position:relative;height:12px;border-radius:6px;background:var(--track);overflow:hidden;margin:6px 0 4px;}
  .gband{position:absolute;top:0;bottom:0;background:var(--band);}
  .gmark{position:absolute;top:-3px;bottom:-3px;width:3px;background:var(--pos);border-radius:2px;}
  .gscale{display:flex;justify-content:space-between;font-size:9px;color:var(--muted);}
  .gpctrow{position:relative;height:14px;margin-bottom:1px;}
  .gpct{position:absolute;transform:translateX(-50%);font-size:11px;font-weight:700;color:var(--pos);font-variant-numeric:tabular-nums;white-space:nowrap;}
  .ci{font-size:10px;color:var(--muted);margin-top:8px;}
  .pq{font-size:10px;color:var(--muted);margin-top:3px;}
  .reset{font-size:10.5px;border:1px solid var(--line);background:#fff;border-radius:7px;padding:5px 10px;cursor:pointer;color:var(--muted);}
  .reset:hover{border-color:var(--muted);color:var(--ink);}
  .sigplot{flex:1;min-width:200px;max-width:300px;height:auto;}
  .sidecol{flex:none;width:118px;display:flex;flex-direction:column;gap:7px;align-items:flex-start;}
  .cihint{font-size:9px;color:var(--muted);line-height:1.35;}

  .formula{font-family:var(--mono);font-size:10px;color:var(--muted);margin-top:18px;}
  .conclusion{font-size:18px;font-weight:400;color:var(--ink);margin:16px 0 0;}
  .cap{font-size:11.5px;color:var(--muted);line-height:1.5;margin-top:8px;border-top:1px solid var(--line);padding-top:14px;}
  .cap b{color:var(--ink);}

  @media (max-width:760px){
    body{padding:24px 20px 48px;}
    .axis,.row,.productrow{grid-template-columns:36px minmax(0,1fr) minmax(135px,24vw) 88px;gap:7px 8px;}
    .axis .a-srclabel span{display:none;}
    .sigma{flex-direction:column;align-items:flex-start;gap:4px;}
    .sigma .net{text-align:left;}
    .postcard{flex-wrap:wrap;align-items:flex-start;gap:12px 16px;padding:13px 15px;}
    .postcard .headline{flex:0 0 116px;}
    .postcard .big{font-size:36px;}
    .postcard .gaugewrap{flex:1 1 230px;}
    .sidecol{width:auto;flex-direction:row;align-items:center;}
    .cihint{max-width:260px;}
  }

  @media (max-width:560px){
    body{padding:20px 14px 48px;}
    .priorcard{display:flex;flex-wrap:wrap;gap:5px 10px;}
    .axis,.row,.productrow{grid-template-columns:34px minmax(0,1fr) 100px 78px;gap:6px;}
    .axis .a-shiftlabel{font-size:7px;}
    .postcard{display:block;}
    .postcard .headline{width:auto;margin-bottom:9px;}
    .sidecol{margin-top:10px;}
    .cihint{max-width:none;}
  }
</style>
</head>
<body>
<div class="wrap">
  <p class="sub">Does a credible lab pathway exist for covid?</p>

  <div class="left">
      <div class="priorcard" id="priorBox">
        <span class="lab">BEFORE · PRIOR</span>
        <span class="pfield">strength <span id="nCard"></span></span>
        <span class="pfield">value <span id="priorCard"></span></span>
      </div>
      <div class="baseline">outside-view base rate, before the case-specific evidence</div>

      <div class="axis">
        <div></div>
        <div class="a-srclabel">SOURCES <span>· click a quote to open its primary source</span></div>
        <div class="a-zone"><span class="lo">for</span><span class="z">1 / 1</span><span class="hi">against</span></div>
        <div class="a-shiftlabel">odds + 90%</div>
      </div>

      <div id="rows"></div>
      <div class="productrow"><div class="label">Odds multiplied together corrected for association</div><div class="expr" id="oddsProduct"></div></div>

      <div class="sigma">
        <span>power = 1 / (1 + association(W - 1)) · association <span style="color:var(--ink)">(<span id="alphaInline"></span>)</span></span>
        <span class="net" id="net"></span>
      </div>
      <div class="formula" id="intervalFormula"></div>

      <div class="postcard">
        <div class="headline">
          <div class="lab">AFTER · POSTERIOR</div>
          <div class="big"><span id="post"></span></div>
          <div class="pq">P(credible lab pathway)</div>
        </div>
        <div class="gaugewrap">
          <div class="gpctrow"><span class="gpct" id="postpct"></span></div>
          <div class="gtrack"><div class="gband" id="band"></div><div class="gmark" id="mark"></div></div>
          <div class="gscale"><span>0%</span><span>50%</span><span>100%</span></div>
          <div class="ci" id="ci"></div>
        </div>
        <div class="sidecol">
          <div class="cihint">shaded = posterior 90% certainty interval from source uncertainty.</div>
          <button class="reset" id="reset">reset</button>
        </div>
      </div>
      <p class="conclusion" id="conclusion"></p>
  </div>

</div>

<script>
const DEFAULT_PRIOR=50, DEFAULT_N=0, DEFAULT_ALPHA=0.3;
const Z90 = 1.6448536269514722;
const SOURCES = [
  {id:"S1", side:"pos", shift:1.90, conf:0.25, q:"DEFUSE: “introduce…human-specific cleavage sites”", url:"https://www.documentcloud.org/documents/21066966-defuse-proposal"},
  {id:"S2", side:"pos", shift:1.70, conf:0.25, q:"Andersen, privately: lab escape “so friggin' likely”", url:"https://biosafetynow.org/wp-content/uploads/2023/07/Proximal_Origin_Slack_OCRd.pdf"},
  {id:"S3", side:"pos", shift:1.30, conf:0.22, q:"DOE: lab origin “most likely”; FBI: lab incident", url:"https://www.dni.gov/index.php/newsroom/reports-publications/reports-publications-2021/3583-declassified-assessment-on-covid-19-origins"},
  {id:"S4", side:"pos", shift:1.20, conf:0.22, q:"“…more likely a product of synthetic genome assembly”", url:"https://www.biorxiv.org/content/10.1101/2022.10.18.512756v1"},
  {id:"S5", side:"neg", shift:-0.45, conf:0.20, q:"WHO-China: a lab incident is “extremely unlikely”", url:"https://www.who.int/docs/default-source/coronaviruse/who-convened-global-study-of-origins-of-sars-cov-2-china-part-joint-report.pdf"},
  {id:"S6", side:"neg", shift:-0.80, conf:0.20, q:"furin sites “naturally occur”; “no smoking gun”", url:"https://www.sciencedirect.com/science/article/pii/S1873506120304165"},
  {id:"S7", side:"neg", shift:-1.00, conf:0.22, q:"Proximal Origin: “not a laboratory construct”", url:"https://www.nature.com/articles/s41591-020-0820-9"},
];
const DEF = SOURCES.map(s=>({shift:s.shift,conf:s.conf}));
let state = {prior:DEFAULT_PRIOR, n:DEFAULT_N, alpha:DEFAULT_ALPHA};

const logit=p=>Math.log(p/(1-p));
const sigmoid=x=>1/(1+Math.exp(-x));
const pairFor=s=>Math.round(sigmoid(s)*100);                         // "for" value out of 100 from a shift
const pctToShift=p=>logit(Math.min(Math.max(p/100,0.02),0.98));
function oddsLabelFromOdds(odds){
  const n=odds>=1?odds:1/odds;
  const text=n>=100?String(Math.round(n)):n>=10?String(Math.round(n)):n.toFixed(1);
  return odds>=1?text+' / 1':'1 / '+text;
}
function oddsLabelFromPercent(percent){
  const p=Math.min(Math.max(percent/100,0.000001),0.999999);
  return oddsLabelFromOdds(p/(1-p));
}
function oddsLabelFromProbability(p){
  const clipped=Math.min(Math.max(p,0.000001),0.999999);
  return oddsLabelFromOdds(clipped/(1-clipped));
}
function oddsLabelFromLogOdds(x){
  return oddsLabelFromProbability(sigmoid(x));
}
function sourceIntervalLabel(s){
  return `90% ${oddsLabelFromLogOdds(s.shift-Z90*s.conf)} - ${oddsLabelFromLogOdds(s.shift+Z90*s.conf)}`;
}
function oddsFactorFromPercent(percent){
  const p=Math.min(Math.max(percent/100,0.000001),0.999999);
  const odds=p/(1-p);
  return odds>=1?odds:1/odds;
}
function compactOddsNumber(n){
  return n>=100?String(Math.round(n)):n>=10?String(Math.round(n)):n.toFixed(1);
}
function displayedOddsFactorFromPercent(percent){
  return Number(compactOddsNumber(oddsFactorFromPercent(percent)));
}
function uncertaintyFactorFromConf(conf){ return Math.exp(conf); }
function confFromUncertaintyFactor(f){ return Math.log(Math.max(1.01, f)); }
function uncertaintyLabelFromConf(conf){ return "×/÷ " + compactOddsNumber(uncertaintyFactorFromConf(conf)); }
function uncertaintyLabelFromFactor(f){ return "×/÷ " + compactOddsNumber(f); }
function uncertainty90LabelFromFactor(f){ return "90% ×/÷ " + compactOddsNumber(Math.pow(f,Z90)); }
// designEffect: W correlated sources count as W/deff effective independent observations (Kish
// effective sample size). α=0 ⇒ deff=1 (accumulate); α=1 ⇒ deff=W (pool/average).
function designEffect(W,alpha){ return 1 + alpha*Math.max(0, W-1); }   // W redundant sources count as W/deff

// Combine prior and evidence in log-odds.
//   evidenceLog = Σshift / deff  — the pooled evidence; this alone is the result when there is no prior.
//   m           = W / deff       — the evidence's effective independent-observation count.
// "prior strength n" = how many observations the prior is worth. The posterior is the count-weighted
// average of the prior (weight n) and the evidence (weight m): n=0 ⇒ evidence alone (default unchanged),
// larger n pulls the posterior toward the prior, n→∞ ⇒ posterior → prior.
function combine(priorLog,shifts,n,alpha){
  const W=shifts.length;
  const Sg=shifts.reduce((sum,shift)=>sum+shift,0);
  const deff=designEffect(W,alpha);
  const evidenceLog=Sg/deff;
  if(n<=0) return evidenceLog;                          // n=0 sentinel: no prior, evidence decides
  const m=W/deff;                                       // effective independent-source count
  return (n*priorLog + m*evidenceLog)/(n+m);            // count-weighted average in log-odds
}

// ---- editable-number helper -------------------------------------------------
// makes a <span class="ed"> whose click reveals a popover of sliders; closes on mouseleave
const ALL_EDS=[];                      // registry so reset can re-sync every slider thumb
function makeEd({text, cls='', right=false, sliders, fmt}){
  const ed=document.createElement('span');
  ed.className='ed '+cls+(right?' editR':'');
  const label=document.createElement('span'); label.className='edtxt'; label.textContent=text; ed.appendChild(label);
  const pop=document.createElement('div'); pop.className='pop'; ed.appendChild(pop);
  const parts=[];
  sliders.forEach(sl=>{
    const head=document.createElement('div'); head.className='plab';
    const name=document.createElement('span'); name.textContent=sl.name;
    const valb=document.createElement('b'); valb.textContent=sl.fmt(sl.get());
    head.append(name,valb);
    const inp=document.createElement('input'); inp.type='range'; inp.min=sl.min; inp.max=sl.max; inp.step=sl.step; inp.value=sl.get();
    inp.addEventListener('input',e=>{ sl.set(parseFloat(e.target.value)); valb.textContent=sl.fmt(sl.get()); recompute(); });
    inp.addEventListener('click',e=>e.stopPropagation());
    pop.append(head,inp);
    parts.push({inp,valb,sl});
    if(sl.note){const nt=document.createElement('div');nt.className='pnote';nt.textContent=sl.note;pop.appendChild(nt);}
  });
  ed.addEventListener('click',e=>{
    e.stopPropagation();
    document.querySelectorAll('.ed.open').forEach(o=>{if(o!==ed)o.classList.remove('open');});
    ed.classList.toggle('open');
  });
  ed.addEventListener('mouseleave',()=>ed.classList.remove('open'));
  ed._setText=t=>{label.textContent=t;};
  ed._sync=()=>parts.forEach(p=>{ p.inp.value=p.sl.get(); p.valb.textContent=p.sl.fmt(p.sl.get()); });
  ALL_EDS.push(ed);
  return ed;
}
document.addEventListener('click',()=>document.querySelectorAll('.ed.open').forEach(o=>o.classList.remove('open')));

// ---- build static structure -------------------------------------------------
const edPrior=makeEd({
  text:oddsLabelFromPercent(state.prior), cls:'',
  sliders:[{name:'prior odds', min:1, max:99, step:1, get:()=>state.prior, set:v=>state.prior=v, fmt:oddsLabelFromPercent,
            note:'the base rate before case evidence.'}]
});
const edN=makeEd({
  text:state.n.toFixed(0), cls:'',
  sliders:[{name:'prior strength n', min:0, max:30, step:0.5, get:()=>state.n, set:v=>state.n=v, fmt:v=>v.toFixed(1),
            note:'how many observations the prior is worth. 0 = let the evidence decide; higher n holds the prior more firmly (and tightens the interval).'}]
});
const edAlpha=makeEd({
  text:state.alpha.toFixed(2), cls:'',
  sliders:[{name:'association', min:0, max:1, step:0.05, get:()=>state.alpha, set:v=>state.alpha=v, fmt:v=>v.toFixed(2),
            note:'0 = accumulate (independent) · 1 = pool (redundant).'}]
});
document.getElementById('priorCard').appendChild(edPrior);
document.getElementById('nCard').appendChild(edN);
document.getElementById('alphaInline').appendChild(document.createTextNode('association '));
document.getElementById('alphaInline').appendChild(edAlpha);

const rowsEl=document.getElementById('rows');
const rowRefs=[];
SOURCES.forEach((s,i)=>{
  const row=document.createElement('div'); row.className='row';
  const chip=document.createElement('div'); chip.className='chip '+s.side; chip.textContent=s.id;
  const q=document.createElement('div');
  q.innerHTML=`<a class="srclink" href="${s.url}" target="_blank" rel="noopener">${s.q}</a>`;
  const bz=document.createElement('div'); bz.className='barzone';
  bz.innerHTML='<div class="axline"></div>';
  const bar=document.createElement('div'); bar.className='bar'; bz.appendChild(bar);
  const valWrap=document.createElement('div'); valWrap.className='val';
  const ed=makeEd({
    text:'', right:true,
    sliders:[
      {name:'source odds', min:2, max:98, step:1, get:()=>pairFor(SOURCES[i].shift), set:v=>SOURCES[i].shift=pctToShift(v), fmt:oddsLabelFromPercent},
      {name:'90% uncertainty', min:1.02, max:3, step:0.01, get:()=>uncertaintyFactorFromConf(SOURCES[i].conf), set:v=>SOURCES[i].conf=confFromUncertaintyFactor(v), fmt:uncertainty90LabelFromFactor,
       note:'source uncertainty. The row shows the corresponding 90% certainty interval.'}
    ]
  });
  const ci=document.createElement('div'); ci.className='sourceci';
  valWrap.appendChild(ed);
  valWrap.appendChild(ci);
  row.append(chip,q,bz,valWrap);
  rowsEl.appendChild(row);
  rowRefs.push({bar,ed,ci});
});

const aOrAn=n=>{const s=String(n);return (s[0]==='8'||s==='11'||s==='18')?'an':'a';};

// ---- compute + paint --------------------------------------------------------
function recompute(){
  edPrior._setText(oddsLabelFromPercent(state.prior));
  edN._setText(state.n.toFixed(0));
  edAlpha._setText(state.alpha.toFixed(2));
  document.getElementById('priorBox').classList.toggle('nzero', !(state.n>0)); // grey the value while the prior is inert

  // bars + per-row value text — each source as a for:against split summing to 100
  SOURCES.forEach((s,i)=>{
    const f=pairFor(s.shift);                               // "for" portion, 0..100
    const bar=rowRefs[i].bar;
    bar.style.left='0'; bar.style.width='100%';
    bar.style.background=`linear-gradient(90deg, var(--pos) ${f}%, var(--neg) ${f}%)`;
    const ed=rowRefs[i].ed;
    ed._setText(oddsLabelFromPercent(f));
    ed.classList.toggle('pos',f>=50); ed.classList.toggle('neg',f<50);
    rowRefs[i].ci.textContent='';
  });
  const posProduct=compactOddsNumber(SOURCES.slice(0,4).reduce((prod,s)=>prod*displayedOddsFactorFromPercent(pairFor(s.shift)),1));
  const negProduct=compactOddsNumber(SOURCES.slice(4,7).reduce((prod,s)=>prod*displayedOddsFactorFromPercent(pairFor(s.shift)),1));
  const evidenceMass=SOURCES.length;
  const exponent=(1/designEffect(evidenceMass,state.alpha)).toFixed(2);
  document.getElementById('oddsProduct').innerHTML=`(<span class="pos">${posProduct}</span> / <span class="neg">${negProduct}</span>)<sup>${exponent}</sup>`;
  document.getElementById('net').innerHTML=
    `1 / (1 + ${state.alpha.toFixed(2)}(${evidenceMass.toFixed(1)} - 1)) = <b>${exponent}</b>`;

  const p0=state.prior/100, priorLog=logit(p0);
  const shifts=SOURCES.map(s=>s.shift);
  const postLog=combine(priorLog,shifts,state.n,state.alpha);
  const post=sigmoid(postLog);

  // Analytic 90% interval. A source uncertainty of ×/÷m means log-odds SD = ln(m); the model is
  // linear in log-odds, so the association correction divides source variance by deff².
  const deff=designEffect(shifts.length,state.alpha);
  const sourceVar = SOURCES.reduce((sum,s)=>sum+s.conf*s.conf,0)/(deff*deff);  // Var(evidence log-odds)
  // Match combine(): for n>0 the mean is a count-weighted average of prior and evidence, so their
  // variances combine with the same (squared) weights — and a stronger prior tightens the interval.
  let intervalSd;
  if(state.n>0){
    const m=shifts.length/deff;                    // effective source count (same m as combine)
    const wP=state.n/(state.n+m), wE=m/(state.n+m);
    intervalSd=Math.sqrt(wP*wP*(1/state.n) + wE*wE*sourceVar);
  } else {
    intervalSd=Math.sqrt(sourceVar);               // no prior → evidence uncertainty only
  }
  const lo=sigmoid(postLog-Z90*intervalSd), hi=sigmoid(postLog+Z90*intervalSd);
  const sourceLogRss = Math.sqrt(SOURCES.reduce((sum,s)=>sum+s.conf*s.conf,0));
  const sourceMultiplier = Math.exp(sourceLogRss/deff);
  const intervalMultiplier = Math.exp(Z90*intervalSd);
  const priorTerm = state.n>0 ? `1/${state.n.toFixed(1)}` : "0";
  document.getElementById('intervalFormula').innerHTML='';

  const fp=Math.round(post*100);
  document.getElementById('post').textContent=oddsLabelFromProbability(post);
  const pctEl=document.getElementById('postpct');
  pctEl.textContent=fp+'%';
  pctEl.style.left=(post*100)+'%';
  document.getElementById('mark').style.left=(post*100)+'%';
  document.getElementById('conclusion').textContent='There is '+aOrAn(fp)+' '+fp+'% chance that a credible pathway exists for COVID.';
  const band=document.getElementById('band');
  band.style.left=(lo*100)+'%'; band.style.width=Math.max(0,(hi-lo)*100)+'%';
  document.getElementById('ci').textContent='';
}

document.getElementById('reset').addEventListener('click',e=>{
  e.stopPropagation();
  state={prior:DEFAULT_PRIOR,n:DEFAULT_N,alpha:DEFAULT_ALPHA};
  SOURCES.forEach((s,i)=>{s.shift=DEF[i].shift;s.conf=DEF[i].conf;});
  ALL_EDS.forEach(e=>e._sync());        // restore every slider thumb + readout, not just the data
  recompute();
});

recompute();
</script>
</body>
</html>
```

  

Attempting to graph the structure of arguments has been done before [Squiggle](https://www.squiggle-language.com/), [Kialo](https://www.kialo-edu.com/), and [Argdown](https://argdown.org/) are a few examples. These services, however, have always had a hard time taking off, for what I believe is a simple reason: mapping out arguments is boring and hard work. People who want to map out entire arguments are few and far between, and those who do can already gather quite an audience from putting in this work.  
  
Here is where I believe we have the new opportunity. Language models have now become capable enough to fill out these full graphs with only light handholding. And if the graphs are made to be inherently transparent any mistake will also quickly be transparent.

The fractal upside
==================

The upside of this grouping node structure is that every node could have not only primary sources as input but also other grouping nodes allowing for building claims out of other sources. This allows us to argue for subclaims, as you can see the example claim is a subclaim of the Covid origins argument. This also allows us to chain together all claims into a big graph allowing for even more complicated representations and more accurate conclusions. If you're curious as to one implementation of is idea you can check it out on [my website](https://jasperblank.com/epistack/).

What is still needed for the [magic encyclopedia](https://www.lesswrong.com/posts/RyeRYm4FrpqP32a2v/citations-needed-magic-encyclopedias-to-save-the-world)
-----------------------------------------------------------------------------------------------------------------------------------------------------------

The method presented in this post is far from enough to map out every claim. This is only a starting point to apply some relevant mathematics to this subject. In order to show what I believe is still needed to use this as a building block I will use the 3 layers suggested by the [Epistemic Case Study Competition](https://www.lesswrong.com/posts/frizRHnA6AZpJSDqw/lab-leaks-black-holes-and-eggs-epistemic-case-study). In this structure the three layers are ingestion, structure and assessment. This tool lives in Layer 2, where we try to structure every relevant part of a claim. This structure should be objective and be shared between everyone.  

### Layer 3: Assessment

Assessment is the most abstract layer. From this layer we need consistent testing to see if the tool is really useful and if people would really need it. The current implementation of this tool is transparent to help with this.

### Layer 2: Structure

This current grouping node is still limited in many ways. This tool only combines odds of different claims. While this allows some level of clustering this cannot represent all claims. Some simple arguments such as "If you're outside and it's raining, you will be wet" cannot be contained in the grouping node. That is why I intend to add Boolean logic nodes and arithmetic nodes. Both of these together will allow every claim or combination of claims to be represented in this system. I plan on having my claim analysis system have these seven nodes.  

*   Noisy AND node:  
    The noisy AND node allow for a group of blockers to be taken into account. In this formula $p_i$ is the probability that a subclaim holds $b_i$  is the blockers strength if the subclaim fails and $s_0$ is the base rate chance of success.

$$
P(Y)=s_0\prod_i \left(1-b_i(1-p_i)\right)
$$

*   Noisy OR node:  
    The noisy OR node allows for a group of unlocks to be taken into account. In this formula $p_i$ is the probability that a subclaim holds $u_i$  is the unlocks strength if the subclaim holds and $s_0$ is the base rate chance of success even if all claims fail.

$$
P(Y)=1-(1-s_0)\prod_i(1-u_i p_i)
$$

*   Possibility node:  
    The possibility node allows the hypothesis space to be split up into different hypotheses one of which has to happen. In this formula $P(H_i)$ is the unnormalized probability of a claim $\sum_i P(H_i$) is the normalization factor and $P_{norm}(H_i)$ is the normalized probability guaranteeing that all hypotheses add up to 100%.

$$
P_{norm}(H_i)=\frac{P(H_i)}{\sum_i P(H_i)}
$$

*   Distribution node:  
    The distribution node allows for uncertain values to be represented and reasoned about. Each distribution node has a domain such as all positive rational numbers. In this formula $X$ is the uncertain value that is represented and $P_X$ describes the probability distribution of what X can be.

$$
X \sim P_X
$$

*   Estimate node:  
    The estimate node allows for a fermi estimate to be made using different distributions. A difficult to estimate distribution can be turned into many easy to estimate distributions. In this formula $X_n$ represent different distributions $f(...)$ represents a formula using these distributions and $Y$ represents the output distribution.

$$
Y = f(X_1, X_2, \ldots, X_n)
$$

*   Predicate node:  
    A predicate node allows for probability claims to be extracted from distribution nodes. It does this by calculating the probability that a claim lies above a given threshold value. In this formula $k$ is the given threshold value $X$ is an uncertain value from a Distribution node and $P(C)$ is the output probability of this node.

$$
P(C)=P(X>k)
$$

*   Grouping node:  
    The grouping node as shown in this article can be used to combine multiple sources into a single probability. This is needed because in the real world most claim will not have single conclusive sources and as such sources need to be grouped together. In this formula $n$ is the number of input ratio's $a$ is the correlation over all input nodes and sources $O_i$ is the every odds input and $O_{claim}$ is the posterior.

$$
O_{\text{claim}} = \left(\prod_{i=1}^{n} O_i\right)^{\frac{1}{1+a(n-1)}}
$$

With these 7 nodes in place all non causal claims can be fully represented and reasoned about. In further articles I will get into more detail regarding the other 6 nodes.

### Layer 1: Ingestion

Ingestion is the combined process of finding primary sources and checking their validity. My structural tool needs this ingestion to connect the primary sources with claims. The most important component this structure still needs from layer 1 is a process that can answer any version of "What is the likelihood ratio of this primary source saying what it says depending on whether the claim is true or false". It also needs to find a reliable answer to the question "How strongly correlated are these two sources"[^c1v76m7a6i8].

[^37szg3pcd4h]: To break this odds ratio down into something like a percentage requires us to go all the way to 9995/5 or 99.95% 

[^pc3ify5yixe]: This is also done in Pearl Probabilistic Reasoning in Intelligent Systems on chapter 2.2.2 page 45 

[^c1v76m7a6i8]: This is my first-ever Lesswrong post. I would like to thank Tom, Glenn, Mark, and Elisabetta for helping me by proofreading and sharing their thoughts on the article.