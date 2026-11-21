from pathlib import Path
import collections,hashlib,os,re,sys
root=Path('.routing')
board=Path('C20W1B1V1.0.kicad_pcb')
before=board.read_bytes()
assert hashlib.sha256(before).hexdigest()=='14705fb95fe5a3e77d3b97f43488a75564373c86ac5a2607d492ece174d70af4'
after=(root/'b1-solution.kicad_pcb').read_bytes()
pattern=rb'^\t\((segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n'
def partition(data):
    return {re.search(rb'\(uuid "([^"]+)"\)',m[0])[1]:(m[1],m[0]) for m in re.finditer(pattern,data,re.M)}
old,new=map(partition,(before,after))
assert re.sub(pattern,b'',before,flags=re.M)==re.sub(pattern,b'',after,flags=re.M)
removed=set(old)-set(new)
assert len(removed)==1 and b'(net "FMC_DQ3")' in old[next(iter(removed))][1]
assert all(old[key]==new[key] for key in old.keys()&new.keys())
stats=collections.Counter()
widths=collections.Counter()
for key in new.keys()-old.keys():
    kind,record=new[key]
    assert b'(net "+3V3")' not in record and b'(net "GND")' not in record
    if kind==b'via':
        assert b'(layers "F.Cu" "B.Cu")' in record
        stats['via']+=1
    else:
        layer=re.search(rb'\(layer "([^"]+)"\)',record)[1].decode()
        assert layer in {'F.Cu','In3.Cu','B.Cu'}
        stats[layer]+=1
        widths[re.search(rb'\(width ([^)]+)\)',record)[1].decode()]+=1
print('Added',dict(stats),'widths',dict(widths),'removed',len(removed))
(root/'original.kicad_pcb').write_bytes(before)
temp=root/'install.kicad_pcb'
temp.write_bytes(after)
os.replace(temp,board)
