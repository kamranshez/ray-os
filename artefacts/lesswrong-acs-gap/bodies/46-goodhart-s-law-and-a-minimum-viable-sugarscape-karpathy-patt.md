# Goodhart's Law and a Minimum Viable Sugarscape: Karpathy Pattern ABM Autoresearch

- URL: https://www.lesswrong.com/posts/GiMvJcAkfhwWHLbsX/goodhart-s-law-and-a-minimum-viable-sugarscape-karpathy
- Author: Raven Of Empire
- Date: 2026-05-23
- Karma: 2  Comments: 0  Words: 1665
- Band: B  Tier: 1  Score: 35.6  Density: 7.51
- Anchors: \bharness(es|ing)?\b, vibe cod, llm (writes|wrote|generates?|generated)

---

Intro
=====

Agent based models (ABMs) are notorious for being over-parameterized. Researchers can get caught in loops effectively doing manual p-hacking adding more and more rules and variables to their funny world of little guys in a grid. My problem is that ABMs can be far too complex, to truly understand the emergent phenomena (in my opinion) we must find the simplest structure that results in their emergence.

  
With this in mind, I vibe coded and iterated on a small experiment: a harness to allow for a karpathy style ABM ablation research loop. It's made up of the following ideas:

*   **prepare.py + other stuff:** The script retrieves baseline benchmark data from the canonical Mesa Sugarscape implementation, establishing ground-truth. It serves as the test harness that evaluates every proposed iteration to check that emergent behaviors remain within proposed error bounds.
*   **strategy.py:** An agent controlled git repo with a single file. To start it's a pre-flattened and shrunken version of the mesa libraries sugarscape implementation. This is in order to allow the model to see the whole implementation at once, as Karpathy did with his train.py.
*   **program.md:** The human research agenda, steers the LLM (I used gemma) based on overarching goals of the experiment.
*   **sugarscape_autoresearch.py:** Main orchestrator that queries the LLM to propose structural simplifications to the strategy file. The LLM writes a new file based on the old one, if the variant passes the tests and has a smaller complexity measure, the change is committed to the git.

How did I determine that a strategy kept the emergent features of the orignal mesa? Using some key characteristics of sugarscape as described in its source, the book *Growing Artificial Societies* by Epstein and Axtell, with my best attempt at faithful error bounds of the measures used. Arguably my error bounds are smaller than should be accepted because they are smaller than the noise of the ABM, it just somewhat makes sure edge cases of the proposed strategy stays in bounds as well. Finally as part of the harness, it completes a parameter sweep over the chosen initial conditions as relevant to the desired emergent features, and makes sure the measured features were within the error bounds of the Mesa implementation.

  
Results
==========

  
Version 1: Line count complexity

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779567251/lexical_client_uploads/qozyvpp9ps1nzooos3ln.png)

My first attempt at a complexity measure was a lazy and simple line count. As you can see in this graph we quickly plateau at around 40 LOC.  
  
Now this run was ~12 hours and tried 213 strategies with ~13 successful ratchets, this experiments generation count is just a count of the times the LLM was prompted. This version was attempting 3 strategies per LLM output, probably affecting strategies viability, but you can still see a clear convergence in the results.  
  
Unfortunately and predictably given my choice of complexity measurement, Goodhart's law clearly comes into play. If you look at the strategies that were successful in this situation; it created mass of unreadable and compressed code with many walrus operators, single-pass procedural loops, and aggressive tuple unpacking.

import math, numpy as np  
from pathlib import Path  
  
  
class Trader:  
 def \_\_init\_\_(self,s,sp,m,v,p): self.w,self.m,self.v,self.p,self.al=\[s,sp\],m,v,p,True  
  
  
class SugarscapeModel:  
 def \_\_init\_\_(self,seed,width=50,height=50,initial\_population=200,endowment\_min=25,endowment\_max=50,metabolism\_min=1,metabolism\_max=5,vision\_min=1,vision\_max=5,enable\_trade=True,**kwargs):  
 self.rng,self.width,self.height,self.initial\_population,self.enable\_trade=np.random.default\_rng(seed),width,height,initial\_population,enable_trade  
 m=np.genfromtxt(Path(\_\_file\_\_).parent/"sugar-map.txt"); self.R=np.stack(\[m, np.flip(m,1)\]); self.M=self.R.copy(); self.occupancy,self.agents,self.all\_trade\_prices,self.total\_trade\_volume={},\[\],\[\],0  
 for _ in range(initial_population):  
 x,y=self.rng.integers(0,width),self.rng.integers(0,height)  
 while (x,y) in self.occupancy: x,y=self.rng.integers(0,width),self.rng.integers(0,height)  
 a=Trader(self.rng.integers(endowment\_min,endowment\_max+1),self.rng.integers(endowment\_min,endowment\_max+1),(self.rng.integers(metabolism\_min,metabolism\_max+1),self.rng.integers(metabolism\_min,metabolism\_max+1)),self.rng.integers(vision\_min,vision\_max+1),(x,y)); self.agents.append(a); self.occupancy\[(x,y)\]=a  
 def step(self):  
 self.R=np.minimum(self.R+1,self.M); living=\[a for a in self.agents if a.al\]; self.rng.shuffle(living)  
 for a in living:  
 m\_t=sum(a.m); c=\[((a.w\[0\]+self.R\[0,nx,ny\])**(a.m\[0\]/m\_t)*(a.w\[1\]+self.R\[1,nx,ny\])**(a.m\[1\]/m_t),abs(dx)+abs(dy),nx,ny) for dx in range(-a.v,a.v+1) for dy in range(-a.v,a.v+1) if 0<abs(dx)+abs(dy)<=a.v and 0<=(nx:=a.p\[0\]+dx)<self.width and 0<=(ny:=a.p\[1\]+dy)<self.height and (nx,ny) not in self.occupancy\]  
 if c: self.rng.shuffle(c); _,_,nx,ny=max(c,key=lambda x:(x\[0\],-x\[1\])); self.occupancy.pop(a.p,None); a.p=(nx,ny); self.occupancy\[a.p\]=a  
 a.w\[0\]+=self.R\[0,a.p\[0\],a.p\[1\]\]-a.m\[0\]; a.w\[1\]+=self.R\[1,a.p\[0\],a.p\[1\]\]-a.m\[1\]; self.R\[0,a.p\[0\],a.p\[1\]\]=self.R\[1,a.p\[0\],a.p\[1\]\]=0  
 if any(v<=0 for v in a.w): a.al=False; self.occupancy.pop(a.p,None)  
 if self.enable_trade:  
 living=\[a for a in self.agents if a.al\]; self.rng.shuffle(living)  
 for a in living:  
 for nx,ny in \[(a.p\[0\]+dx,a.p\[1\]+dy) for dx in range(-a.v,a.v+1) for dy in range(-a.v,a.v+1) if abs(dx)+abs(dy)<=a.v\]:  
 if 0<=(nx:=nx)<self.width and 0<=(ny:=ny)<self.height and (o:=self.occupancy.get((nx,ny))) and o.al and o!=a:  
 while all(v>0 for v in a.w + o.w):  
 mrs\_a,mrs\_o=(a.w\[1\]/a.m\[1\])/(a.w\[0\]/a.m\[0\]),(o.w\[1\]/o.m\[1\])/(o.w\[0\]/o.m\[0\])  
 if math.isclose(mrs\_a,mrs\_o) or mrs\_a<=0 or mrs\_o<=0: break  
 p=math.sqrt(mrs\_a*mrs\_o); s,b=(a,o) if mrs\_a>mrs\_o else (o,a); m\_ts,m\_tb=sum(s.m),sum(b.m); sa,spa=(1,int(p)) if p>=1 else (int(1/p),1)  
 u\_s,u\_b = s.w\[0\]**(s.m\[0\]/m\_ts)\*s.w\[1\]\*\*(s.m\[1\]/m\_ts), b.w\[0\]**(b.m\[0\]/m\_tb)\*b.w\[1\]\*\*(b.m\[1\]/m\_tb)  
 if (s.w\[0\]+sa)**(s.m\[0\]/m\_ts)*(s.w\[1\]-spa)**(s.m\[1\]/m\_ts)>u\_s and (b.w\[0\]-sa)**(b.m\[0\]/m\_tb)*(b.w\[1\]+spa)**(b.m\[1\]/m\_tb)>u\_b:  
 s.w\[0\]+=sa; b.w\[0\]-=sa; s.w\[1\]-=spa; b.w\[1\]+=spa; self.all\_trade\_prices.append(p); self.total\_trade\_volume+=1  
 else: break  
  
  
def create_model(seed=42,\*\*params): return SugarscapeModel(seed=seed,\*\*params)  
def run_model(model,steps=200):  
 for _ in range(steps): model.step()  
 living=\[a for a in model.agents if a.al\]  
 return {"agent\_wealths":\[sum(a.w) for a in living\], "final\_population":len(living), "initial\_population":model.initial\_population, "trade\_prices":model.all\_trade\_prices, "trade\_volume":model.total\_trade\_volume, "agent\_positions":\[a.p for a in living\], "grid\_width":model.width, "grid\_height":model.height, "steps\_run":steps}

  
Version 2: Combined AST Node Complexity and Cyclomatic Complexity

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779568558/lexical_client_uploads/vf7gwvimdrlstptdu5pv.png)

This version used a combined complexity metric of AST node counts and decision point counts (Weighted 40% and 60% respectively). I ended up running this for 36 hours or so, and it got 13 total successful ratchets/strategy attempts (Compared to the ~13 for the LOC complexity over 12 hours). This graphs generation count is counting each successful strategy attempt. One thing to keep in mind is that this versions starting strategy file was actually the ending strategy file of the last experiment, and therefore already quite simplified according to a line count perspective.

As you can see in the graph, it was much harder for the LLM to make progress with this. Now although I stopped, im sure you could run this for much longer and see it possibly converge. Im not sure if the fact that I made it only do one strategies per LLM call made it research slower? It could have but that feels unintuitive to me, I assumed allowing more attention to go to solving a more complex problem would make it faster. It likely had such slow progress because of how uninterpretable the file was, how compressed it already was from the original experiment, but even with that the llm was clearly able to make progress.  
  
The actual optimizations the LLM made were interesting, ironically it was able to shorten the line count too. Here are a few examples:

1.  It was able to realize that raising utility to the power of $m_t$ is a monotonic transformation, allowing it to simplify the equation from $U = (w_0 + R_0)^{m_0/m_t} * (w_1 + R_1)^{m_1/m_t}$ to $U = (w_0 + R_0)^{m_0} * (w_1 + R_1)^{m_1}$.
2.  The original calculated the marginal rate of substitution (MRS) using nested divisions, requiring 6 divisions and multiple nested brackets. It was able to use the algebraic identity$({w_1/m_1})/({w_0/w_0}) = w_1/w_0 * m_0/m_1$ to consolidate the calculation.
3.  It used to calculate float utilities divided by the sum of metabolisms, by raising both sides of the inequality to the power of $m_{ts}$ the LLM eliminated the divisions entirely.
4.  Eliminated the trader class, simply represents them in a list. Much lower complexity.
5.  Previously during agent movement the strategy dynamically generated coordinate ranges and manhattan distances on the fly. Now it pre-calculates all possible spatial offsets for maximum possible vision range, then filters this list, this replaces dynamic and nested math with a lookup loop.

import numpy as np
from pathlib import Path


class SugarscapeModel:
    def \_\_init\_\_(self,seed,width=50,height=50,initial\_population=200,endowment\_min=25,endowment\_max=50,metabolism\_min=1,metabolism\_max=5,vision\_min=1,vision\_max=5,enable\_trade=True,**kwargs):
        self.rng,self.width,self.height,self.initial\_population,self.enable\_trade=np.random.default\_rng(seed),width,height,initial\_population,enable_trade
        m=np.genfromtxt(Path(\_\_file\_\_).parent/"sugar-map.txt"); self.R=np.stack(\[m, m\[:,::-1\]\]); self.M=self.R.copy(); self.occupancy,self.agents,self.all\_trade\_prices,self.total\_trade\_volume={},\[\],\[\],0
        self.off=\[(dx,dy,abs(dx)+abs(dy))for dx in range(-5,6)for dy in range(-5,6)if dx or dy\]
        while len(self.agents)<initial_population:
            p=self.rng.integers(0,width),self.rng.integers(0,height)
            if p not in self.occupancy:
                a=\[\*self.rng.integers(endowment\_min,endowment\_max+1,2),\*self.rng.integers(metabolism\_min,metabolism\_max+1,2),self.rng.integers(vision\_min,vision\_max+1),*p,True\]
                self.agents.append(a); self.occupancy\[p\]=a
    def step(self):
        self.R=np.minimum(self.R+1,self.M); living=\[a for a in self.agents if a\[7\]\]; self.rng.shuffle(living)
        for a in living:
            if c := max((( (a\[0\]+self.R\[0,nx,ny\])\*\*a\[2\]\*(a\[1\]+self.R\[1,nx,ny\])**a\[3\],-d,nx,ny)for dx,dy,d in self.off if d<=a\[4\]and 0<=(nx:=a\[5\]+dx)<self.width and 0<=(ny:=a\[6\]+dy)<self.height and(nx,ny)not in self.occupancy),default=None):
                self.occupancy.pop((a\[5\],a\[6\]),None); a\[5\],a\[6\]=c\[2\],c\[3\]; self.occupancy\[(a\[5\],a\[6\])\]=a
            r=self.R\[:,a\[5\],a\[6\]\]; a\[0\]+=r\[0\]-a\[2\]; a\[1\]+=r\[1\]-a\[3\]; r\[:\] = 0
            if a\[0\]<=0 or a\[1\]<=0: a\[7\]=False; self.occupancy.pop((a\[5\],a\[6\]),None)
        if self.enable_trade:
            for a in \[a for a in living if a\[7\]\]:
                for dx,dy,d in self.off:
                    if d<=a\[4\] and (o:=self.occupancy.get((a\[5\]+dx,a\[6\]+dy))):
                        while True:
                            ma,mo=a\[1\]/a\[0\]\*a\[2\]/a\[3\],o\[1\]/o\[0\]\*o\[2\]/o\[3\]; p=(ma\*mo)\*\*.5; s,b=(a,o) if ma>mo else (o,a); sa,spa=(1,int(p)) if p>=1 else (int(1/p),1)
                            if s\[1\]<=spa or b\[0\]<=sa or (s\[0\]+sa)\*\*s\[2\]\*(s\[1\]-spa)\*\*s\[3\]<=s\[0\]\*\*s\[2\]\*s\[1\]\*\*s\[3\] or (b\[0\]-sa)\*\*b\[2\]\*(b\[1\]+spa)\*\*b\[3\]<=b\[0\]\*\*b\[2\]\*b\[1\]\*\*b\[3\]: break
                            s\[0\]+=sa; b\[0\]-=sa; s\[1\]-=spa; b\[1\]+=spa; self.all\_trade\_prices.append(p); self.total\_trade\_volume+=1


def create_model(seed=42,\*\*params): return SugarscapeModel(seed=seed,\*\*params)
def run_model(m,steps=200):
    for _ in range(steps): m.step()
    l=\[a for a in m.agents if a\[7\]\]
    return {"agent\_wealths":\[a\[0\]+a\[1\] for a in l\], "final\_population":len(l), "initial\_population":m.initial\_population, "trade\_prices":m.all\_trade\_prices, "trade\_volume":m.total\_trade\_volume, "agent\_positions":\[(a\[5\],a\[6\]) for a in l\], "grid\_width":m.width, "grid\_height":m.height, "steps\_run":steps}

  
Conclusion
=============

Unfortunately I am a big dummy and did not commit/save the original flattened sugarscape implementation, because of this we unfortunately can't do a good comparison to the original state of the strategy. I will say that the harness, if inspected, still meets justifiable standards of the sugarscape model. Understand the starting point was originally ~140 lines and must have passed the harness, therefore it ran mostly like the original mesa implementation.

The lessons I want to take away are this:

*Goodhart's law clearly dictates the "flavour" of the code.* Optimizing for text length just creates obfuscation. Optimizing for structural logic more cleanly translates to revelations about the system and how it can be optimized, although not exactly solving the obfuscation issue. The LLM isn't just reformatting the code, it can clearly identify newer algebraic expressions required to simplify loops and such, it is able to use itself as an algorithmic razor.  
  
ABMs in general suffer from a lot of human bias. Humans could design algorithms with their self discovery in mind, not just engineering in human concepts but allowing for room for the algorithm to discover and demystify its own concepts. I think we can start designing such that your experiment can reformat and optimize a cruder human guess/attempt at a thesis.  
  
Using this idea, we can replace the manual tweaking of code structure and simulation rules with automated and metric bound iteration. In my case to showcase attempting to find the minimum viable structure of a model, but in other cases it may be approaching a new and complex emergent phenomena in itself. To restate; We can be honest about the overfitting of ABMs that humans do and just allow for the robot to do it.  
  
The repo is here (be warned it's gross and not modular):  
[https://github.com/NobodyKnowNothing/Sugarscape-Auto-Ablation](https://github.com/NobodyKnowNothing/Sugarscape-Auto-Ablation)

  
In it contains logs of all this and the graphs I have posted. If someone can generalize this pipeline and throw it at more mesa models that would be amazing, I may do it myself if I can get a grant or if I feel like it. This technique is probably applicable to cellular automata and many other kinds of rule based emergence seeking simulations.