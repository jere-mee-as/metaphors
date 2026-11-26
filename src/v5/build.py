import json,re,sys,collections; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from shell5 import page4
P=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'metaphors.json')))
def key(t):
    m=re.search(r'\b(?:is|are)\s+(?:a |an |the )?(.+)$',t,re.I)
    if not m: return '',''
    phr=m.group(1).strip(); w=re.sub(r'[^a-z]','',phr.split()[-1].lower())
    if w.endswith('ies'): w=w[:-3]+'y'
    elif len(w)>4 and w.endswith('s') and not w.endswith('ss'): w=w[:-1]
    return w,phr
tree=[];units=[]
for di,a in enumerate(P):
    g={'n':a['n'],'i':a.get('i',''),'items':[]}
    for ci,u in enumerate(a['u']):
        iid=f'{di}.{ci}'; g['items'].append({'id':iid,'n':u['n'],'i':u.get('i','')})
        for i in u['t']:
            t=a['t'][i]; w,phr=key(t['t'])
            units.append({'it':iid,'its':[iid],'t':t['t'],'w':w,'ph':phr,'p':t.get('p',''),'k':[k['f'] for k in t['k']]})
    tree.append(g)
cnt=collections.Counter(u['w'] for u in units if u['w'])
pics=[w for w,n in sorted(cnt.items(),key=lambda x:(-x[1],x[0])) if n>=3]
for u in units:
    if u['w'] in pics: u['its'].append('p:'+u['w'])
tree.insert(0,{'n':'By picture','i':'◇','nohome':1,'items':[{'id':'p:'+w,'n':w,'i':''} for w in pics]})
site={'tree':tree,'units':units,'noun':['metaphor','metaphors'],'by':'subject','PANEL':False,'PICK':1,
 'INTRO':'The pictures hidden in how we talk. The highlight is the picture being borrowed.'}
theme=r'''
:root{--bg:#f5f0e6;--fg:#2340b8;--fg2:#28357a;--dim:#4f5ca8;--line:#e6c3d6;--line2:#efd9e4;--acc:#c81d70;--hov:#efe6e3;--sel:#fbe3ef;--hl:#ffc2e2;--panel:#fbf7ef;--bar:#f5f0e6;
--display:Fraunces,Georgia,serif;--text:Fraunces,Georgia,serif;--dispw:800;--displs:-.02em}
body{font-variation-settings:"SOFT" 100,"WONK" 1}
#say{font-style:italic;font-size:27px}#say b{font-style:italic}
.mr{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:24px}
.mr .p1{font-weight:650;font-size:16.5px;line-height:1.25}
.mr .p1 em{font-style:italic;background:#ff4fae;color:#fff;padding:0 4px}
.mr .note{display:block;font-size:12.5px;font-style:italic;color:var(--dim);margin-top:4px;line-height:1.4}
.mr ul{list-style:none;margin:0;padding:0}.mr li{font-size:14.5px;line-height:1.4;padding:2px 0}
.mr li span::before{content:"“";color:var(--acc)}.mr li span::after{content:"”";color:var(--acc)}
.same{margin-top:6px;font-size:12.5px;color:var(--dim)}.same button{color:var(--fg2);text-decoration:underline;text-decoration-color:var(--line);margin-right:8px}.same button:hover{color:var(--acc)}
.pics{columns:3 220px;column-gap:24px}
.pics button{display:grid;grid-template-columns:110px 1fr 28px;gap:8px;align-items:center;width:100%;padding:3px 0;font-size:14.5px;break-inside:avoid}
.pics button:hover{color:var(--acc)}.pics i{display:block;height:8px;background:#ff4fae}.pics .m{text-align:right}
@media (max-width:860px){.mr{grid-template-columns:1fr;gap:6px}}
'''
js=r'''
SITE.BLOB=u=>[u.t,u.p,...u.k].join(' ');
const TT=(u,Q)=>{if(!u.ph||Q)return hl(u.t,Q);const i=u.t.toLowerCase().lastIndexOf(u.ph.toLowerCase());return i<0?esc(u.t):esc(u.t.slice(0,i))+'<em>'+esc(u.t.slice(i))+'</em>'};
SITE.SAY=(it,u,q)=>q?`Metaphors with “${esc(q)}”`:!it?'Metaphors for…':it.id.startsWith('p:')?`Metaphors that borrow a <b>${esc(it.n)}</b>`:`Metaphors for <b>${esc(it.n.toLowerCase())}</b>`;
SITE.GROUP=(u,it)=>it&&it.id.startsWith('p:')?ITEMS[u.it].g.n+' · '+ITEMS[u.it].n:'';
SITE.ROW=(u,Q)=>{const same=SITE.units.filter(x=>x!==u&&x.w&&x.w===u.w);
 return `<div class="mr"><div><span class="p1">${TT(u,Q)}</span>${u.p?`<span class="note onsel">${hl(u.p,Q)}</span>`:''}${same.length?`<div class="same onsel">Same picture: ${same.slice(0,4).map(x=>`<button data-jump="${x.ix}">${esc(x.t)}</button>`).join('')}${same.length>4?`<button data-id="p:${esc(u.w)}">all ${same.length+1}</button>`:''}</div>`:''}</div><ul>${u.k.map(k=>`<li><span>${hl(k,Q)}</span>${cpb(k)}</li>`).join('')}</ul></div>`};
SITE.FEATURE=()=>{const P=SITE.tree[0].items.map(it=>({it,n:(BY[it.id]||[]).length}));const mx=P[0].n;
 return `<h3>The pictures we borrow most</h3><div class="pics">${P.map(p=>`<button data-id="${p.it.id}"><span>${esc(p.it.n)}</span><i style="width:${p.n/mx*100}%"></i><span class="m">${p.n}</span></button>`).join('')}</div>`};
'''
page4('metaphors','Metaphors for…','family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..900,100,1;1,9..144,400..900,100,1',theme,site,js)
