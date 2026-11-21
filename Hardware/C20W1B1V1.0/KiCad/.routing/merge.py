import collections
import json
import re
import sys
from pathlib import Path
import pcbnew as p

root=Path('.routing')
source=Path('C20W1B1V1.0.kicad_pcb')
old=p.LoadBoard(str(source))
routed=p.LoadBoard(str(source))
assert p.ImportSpecctraSES(routed,sys.argv[1])
base=json.loads((root/'base.json').read_text(encoding='utf-8-sig'))
nets={re.search(r'\[([^\]]+)\]',i['items'][0]['description'])[1] for i in base['unconnected_items']} - {'GND','+3V3'}

def xy(v):
    return (v.x,v.y)

def close(a,b):
    return max(abs(x-y) for x,y in zip(a,b)) <= 700

def matches(t,u):
    if type(t)!=type(u) or t.GetLayer()!=u.GetLayer():
        return False
    if isinstance(t,p.PCB_VIA):
        return close(xy(t.GetPosition()),xy(u.GetPosition()))
    if abs(t.GetWidth()-u.GetWidth())>700:
        return False
    a,b=xy(t.GetStart()),xy(t.GetEnd())
    c,d=xy(u.GetStart()),xy(u.GetEnd())
    return (close(a,c) and close(b,d)) or (close(a,d) and close(b,c))

orig=collections.defaultdict(list)
for t in old.GetTracks():
    orig[str(t.GetNetname())].append(t)
stats=collections.Counter()
for t in routed.GetTracks():
    name=str(t.GetNetname())
    if name not in nets:
        continue
    if any(matches(t,u) for u in orig[name]):
        stats[(name,'existing')]+=1
        continue
    layer=str(t.GetLayerName())
    if not isinstance(t,p.PCB_VIA) and layer not in {'F.Cu','B.Cu','In3.Cu'}:
        raise RuntimeError((name,layer))
    if not isinstance(t,p.PCB_VIA):
        for endpoint, setter in [(t.GetStart(),t.SetStart),(t.GetEnd(),t.SetEnd)]:
            for u in orig[name]:
                if isinstance(u,p.PCB_VIA) or u.GetLayer()==t.GetLayer():
                    points=[u.GetPosition()] if isinstance(u,p.PCB_VIA) else [u.GetStart(),u.GetEnd()]
                    match=next((v for v in points if close(xy(v),xy(endpoint))),None)
                    if match is not None:
                        setter(match)
                        break
    copy=t.Duplicate()
    copy.SetNet(old.GetNetsByName()[name])
    copy.SetLocked(False)
    old.Add(copy)
    stats[(name,'added')]+=1
print(sorted(stats.items()))
assert p.SaveBoard(str(root/source.name),old)

