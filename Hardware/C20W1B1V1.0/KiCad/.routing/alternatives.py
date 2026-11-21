import collections,json,re,sys,uuid
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

r=Path('.routing')
source=Path('C20W1B1V1.0.kicad_pcb').read_bytes()
edge=source.rfind(b'\n)')
idre=rb'\(uuid "([^"]+)"\)'
copper=rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n'
original={re.search(idre,item[0])[1] for item in re.finditer(copper,source,re.M)}
labels={}
alts=[]
seen=set()
ownership={}
invalid=set()
sizes=[]
if sys.argv[1]=='build':
    files=['best','quick','fast','target','tb-fixed','reflow','reflow2','reflow3']
    for filename in files:
        p=r/(filename+'.kicad_pcb')
        if not p.is_file():
            continue
        groups=collections.defaultdict(list)
        for m in re.finditer(copper,p.read_bytes(),re.M):
            rec=m[0]
            u=re.search(idre,rec)[1]
            if u in original:
                continue
            name=re.search(rb'\(net "([^"]+)"\)',rec)[1].decode()
            if (filename=='quick' and name in {'SCL','SDA'}) or (filename=='fast' and name=='TFT_CLK_SPI'):
                continue
            groups[name].append(re.sub(idre,b'(uuid "TEMP")',rec))
        for net,blocks in sorted(groups.items()):
            fingerprint=(net,tuple(sorted(blocks)))
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            alt=len(alts)
            contents=bytearray()
            for block in blocks:
                uid=str(uuid.uuid4())
                ownership[uid]=alt
                contents+=block.replace(b'(uuid "TEMP")',('(uuid "'+uid+'")').encode())
            labels[alt]=(net,filename)
            sizes.append(len(blocks))
            alts.append(contents.decode())
    (r/'alts.json').write_text(json.dumps([alts,labels,ownership,sizes]))
    destination=r/'merged'/'C20W1B1V1.0.kicad_pcb'
    destination.write_bytes(source[:edge+1]+''.join(alts).encode()+source[edge+1:])
    print(len(alts),len(ownership),len({v[0] for v in labels.values()}))
else:
    alts,labels,ownership,sizes=json.loads((r/'alts.json').read_text())
    labels={int(k):v for k,v in labels.items()}
    conflicts=set()
    for name in sys.argv[2:]:
        report=json.loads((r/name).read_text(encoding='utf-8-sig'))
        for v in report['violations']:
            if v['type'] in {'lib_footprint_issues','track_dangling','via_dangling'}:
                continue
            owners={ownership.get(a['uuid']) for a in v['items']} - {None}
            if len(owners)==1:
                invalid.update(owners)
            elif len(owners)==2:
                conflicts.add(tuple(sorted(owners)))
    outlines=collections.defaultdict(list)
    for k,(net,origin) in labels.items():
        outlines[net].append(k)
    constraints=list(outlines.values())+list(conflicts)
    ix=[]
    iy=[]
    for line,group in enumerate(constraints):
        ix.extend([line]*len(group))
        iy.extend(group)
    n=len(alts)
    matrix=coo_matrix((np.ones(len(ix)),(ix,iy)),shape=(len(constraints),n)).tocsc()
    upper=[float(i not in invalid) for i in range(n)]
    costs=[-1+min(sizes[i],200)*.00002+(0 if labels[i][1]=='best' else .006) for i in range(n)]
    result=milp(costs,integrality=np.ones(n),bounds=Bounds(np.zeros(n),upper),
                constraints=LinearConstraint(matrix,ub=np.ones(len(constraints))),
                options={'time_limit':10})
    assert result.x is not None,result.message
    selected=[i for i,v in enumerate(result.x) if v>.5]
    data=''.join(alts[i] for i in selected).encode()
    (r/'merged'/'C20W1B1V1.0.kicad_pcb').write_bytes(source[:edge+1]+data+source[edge+1:])
    print('selected',len(selected),'excluded',len(invalid),'conflicts',len(conflicts))
    print([labels[i] for i in selected])

