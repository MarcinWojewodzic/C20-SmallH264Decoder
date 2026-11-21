from pathlib import Path
import re
r=Path('.routing')
working=Path('C20W1B1V1.0.kicad_pcb')
generated=(r/working.name).read_bytes()
source=working.read_bytes()
def copper(data):
    for record in re.finditer(rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n',data,re.M):
        key=re.search(rb'\(uuid "([^"]+)"\)',record[0])[1]
        yield key,record[0]
old=dict(copper(source))
new=dict(copper(generated))
assert old.keys() <= new.keys(), len(old.keys()-new.keys())
additions=[value for key,value in new.items() if key not in old]
assert additions
outer=source.rfind(b'\n)')
assert outer>=0
print('New copper objects:',len(additions))
combined=source[:outer+1]+b''.join(additions)+source[outer+1:]
(r/'merged').mkdir(exist_ok=True)
(r/'merged'/working.name).write_bytes(combined)
