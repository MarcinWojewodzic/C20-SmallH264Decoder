from pathlib import Path
import json,re
d=Path('.routing')
b=json.loads((d/'base.json').read_text(encoding='utf-8-sig'))
nets={re.search(r'\[([^\]]+)\]',i['items'][0]['description'])[1] for i in b['unconnected_items']} - {'GND','+3V3'}
s=(d/'work.dsn').read_text()
def split(m):
    name,members,rules=m.groups()
    active=[]
    skip=[]
    for tok in re.findall(r'"[^"]+"|[^\s]+',members):
        (active if tok.strip('"') in nets else skip).append(tok)
    def netclass(n,items):
        return '    (class '+n+' '+ ' '.join(items) +rules if items else ''
    return netclass(name,active)+netclass('Skip'+name.split(',')[0],skip)
s=re.sub(r'^    \(class (\S+) ([\s\S]*?)(\n      \(circuit[\s\S]*?^    \)\n)',split,s,flags=re.M)
(d/'target.dsn').write_text(s)
