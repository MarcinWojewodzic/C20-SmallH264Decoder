import json,re,sys
from pathlib import Path
import pcbnew as p
layers=[p.F_Cu,p.In3_Cu,p.B_Cu]
source=Path(sys.argv[1])
routes=json.loads(Path(sys.argv[2]).read_text())
excluded=set(sys.argv[3:])
b=p.LoadBoard(str(source))
names=b.GetNetsByName()
ids=set()

def xy(pt):
    return p.VECTOR2I(round(pt[1]*1e6),round(pt[2]*1e6))

for net,(width,points) in routes.items():
    if net in excluded:
        continue
    for a,z in zip(points,points[1:]):
        if a==z:
            continue
        if a[0]!=z[0]:
            assert a[1:]==z[1:]
            t=p.PCB_VIA(b)
            t.SetPosition(xy(a))
            t.SetViaType(p.VIATYPE_THROUGH)
            t.SetLayerPair(p.F_Cu,p.B_Cu)
            t.SetWidth(500000)
            t.SetDrill(300000)
        else:
            t=p.PCB_TRACK(b)
            t.SetLayer(layers[a[0]])
            t.SetWidth(round(width*1e6))
            t.SetStart(xy(a))
            t.SetEnd(xy(z))
        t.SetNet(names[net])
        b.Add(t)
        ids.add(t.m_Uuid.AsString().encode())
r=Path('.routing')
p.SaveBoard(str(r/'grid-temp.kicad_pcb'),b)
additions=[]
for rec in re.finditer(rb'^\t\((?:segment|via)\r?\n[\s\S]*?^\t\)\r?\n',(r/'grid-temp.kicad_pcb').read_bytes(),re.M):
    if re.search(rb'\(uuid "([^"]+)"\)',rec[0])[1] in ids:
        additions.append(rec[0])
assert len(additions)==len(ids)
original=source.read_bytes()
e=original.rfind(b'\n)')
dest=r/'merged'/'C20W1B1V1.0.kicad_pcb'
dest.write_bytes(original[:e+1]+b''.join(additions)+original[e+1:])
print(len(additions),sorted(set(routes)-excluded))
