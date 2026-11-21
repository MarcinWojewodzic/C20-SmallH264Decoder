from pathlib import Path
import json,sys
lib=Path('.routing/exact-grid.py').read_text()
exec(lib[:lib.index('for net,ends in sorted')].replace('cache=True','cache=False').replace('geom.json','repair-geom.json'))

plan={}
delete=[]
orig=g['obstacles'][:]
work=[(' /uC/SWCLK'.strip(),26135)]
p=Path('.routing/candidates.json')
if p.is_file():
    work=[(n,idx) for n,rows in json.loads(p.read_text()).items() for weight,idx,name,u in rows]
for net,idx in work:
    if net in plan or idx in delete:
        continue
    o=orig[idx]
    kind,oldnet,layers,ax,ay,bx,by,r=o
    layer=layers.bit_length()-1
    assert kind==1 and layers in (1,2,4)
    old=g['obstacles'][:]
    g['obstacles'].remove(o)
    w=.220472 if net=='QSPI_CLK' else .1524
    path=solve(net,g['targets'][net],w)
    if not path and net!='QSPI_CLK':
        w=.102
        path=solve(net,g['targets'][net],w)
    if not path:
        g['obstacles']=old
        print(net,oldnet,'blocked',flush=True)
        continue
    repl=solve(oldnet,[[[layer,ax,ay]],[[layer,bx,by]]],2*r)
    if not repl:
        g['obstacles']=old
        print(net,oldnet,'cannot reconnect',flush=True)
        continue
    len0=math.hypot(ax-bx,ay-by)
    len1=sum(math.hypot(a[1]-b[1],a[2]-b[2]) for a,b in zip(repl,repl[1:]))
    if len1-len0>3:
        g['obstacles']=old
        print(net,oldnet,'reconnect too long',len0,len1,flush=True)
        continue
    delete.append(idx)
    plan[net]=[w,path]
    plan[oldnet]=[2*r,repl]
    print(net,oldnet,'solved',len0,len1,flush=True)
    (d/'repair.json').write_text(json.dumps(plan))
    (d/'delete.json').write_text(json.dumps([g['editable'][str(i)] for i in delete]))
