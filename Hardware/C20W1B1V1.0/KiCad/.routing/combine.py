from pathlib import Path
import collections,re,json,sys
r=Path('.routing')
src=Path('C20W1B1V1.0.kicad_pcb')
source=src.read_bytes()
def records(data):
    return {re.search(rb'\(uuid "([^"]+)"\)',record[0])[1]:record[0] for record in re.finditer(rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n',data,re.M)}
old=records(source)
def added(filename):
    group=collections.defaultdict(list)
    for uid,block in records((r/filename).read_bytes()).items():
        if uid not in old:
            name=re.search(rb'\(net "([^"]+)"\)',block)[1].decode()
            group[name].append(block)
    return group
quick=added('quick.kicad_pcb')
fast=added('fast.kicad_pcb')
bad=set(['LTDC_G4','LTDC_R3','LTDC_R7','LTDC_B6','TFT_CLK_SPI'])
bad.update(sys.argv[1:])
goodquick={n for n in quick if n not in {'SCL','SDA'}}
for n,blocks in fast.items():
    if n not in bad and n not in goodquick:
        quick[n]=blocks
quick={n:b for n,b in quick.items() if n not in sys.argv[1:]}
outer=source.rfind(b'\n)')
(r/'merged'/src.name).write_bytes(source[:outer+1]+b''.join(b for g in quick.values() for b in g)+source[outer+1:])
print(sorted(quick))
