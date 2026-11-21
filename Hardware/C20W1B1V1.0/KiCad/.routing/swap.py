import collections,json,re,sys,uuid
from pathlib import Path
p=Path('.routing')
raw=Path('C20W1B1V1.0.kicad_pcb').read_bytes()
start=(p/'repaired.kicad_pcb').read_bytes()
pat=rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n'
uid=rb'\(uuid "([^"]+)"\)'
def items(board):
    return {re.search(uid,m[0])[1].decode():m[0] for m in re.finditer(pat,board,re.M)}
def name(b):
    return re.search(rb'\(net "([^"]+)"\)',b)[1].decode()
orig=items(raw)
base=items(start)
edge=start.rfind(b'\n)')
missing={'LTDC_R2','LTDC_R7','LTDC_HS','LTDC_B1','LTDC_B2','LTDC_B6'}
def append(data,records):
    i=data.rfind(b'\n)')
    return data[:i+1]+b''.join(records)+data[i+1:]
owners={}
variants={}
if sys.argv[1]=='build':
    groups=collections.defaultdict(list)
    for version in ('reflow','reflow2','reflow3','quick','target','fast'):
        for key,block in items((p/(version+'.kicad_pcb')).read_bytes()).items():
            net=name(block) if key not in orig else ''
            if net in missing:
                new=str(uuid.uuid4())
                owners[new]=(net,version)
                groups[net+':'+version].append(block.replace(key.encode(),new.encode()))
    (p/'swap-data.json').write_text(json.dumps([owners,{n:[b.decode() for b in bs] for n,bs in groups.items()}]))
    out=append(start,[b for bs in groups.values() for b in bs])
else:
    owners,variants=json.loads((p/'swap-data.json').read_text())
    d=json.loads((p/'swap-report.json').read_text(encoding='utf-8-sig'))
    collisions=collections.defaultdict(set)
    invalid=set()
    for v in d['violations']:
        keys=[i['uuid'] for i in v['items']]
        olds=[k for k in keys if k in base]
        for k in keys:
            if k not in owners:
                continue
            key=':'.join(owners[k])
            for u in olds:
                if u in orig:
                    invalid.add(key)
                else:
                    collisions[key].add(name(base[u]))
            if len(keys)==1 and v['type'] not in {'via_dangling','track_dangling'}:
                invalid.add(key)
            if any(i['description'].startswith('Prostok') for i in v['items']) and v['type']=='copper_edge_clearance':
                invalid.add(key)
    valid=sorted((len(collisions[n]),n,sorted(collisions[n])) for n in variants if n not in invalid)
    print(valid)
    if sys.argv[1]=='list':
        exit()
    choice=sys.argv[2]
    assert choice not in invalid
    drop=collisions[choice]
    def prune(m):
        key=re.search(uid,m[0])[1].decode()
        return b'' if key not in orig and name(m[0]) in drop else m[0]
    data=re.sub(pat,prune,start,flags=re.M)
    out=append(data,[s.encode() for s in variants[choice]])
(p/'merged'/'C20W1B1V1.0.kicad_pcb').write_bytes(out)
