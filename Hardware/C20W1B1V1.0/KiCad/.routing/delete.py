from pathlib import Path
import json,re
r=Path('.routing')
drop={item.encode() for item in json.loads((r/'delete.json').read_text())}
data=(r/'best.kicad_pcb').read_bytes()
p=rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n'
actual=set()
def remove(m):
    uid=re.search(rb'\(uuid "([^"]+)"\)',m[0])[1]
    if uid in drop:
        actual.add(uid)
        return b''
    return m[0]
data=re.sub(p,remove,data,flags=re.M)
assert actual==drop
(r/'repaired-base.kicad_pcb').write_bytes(data)
