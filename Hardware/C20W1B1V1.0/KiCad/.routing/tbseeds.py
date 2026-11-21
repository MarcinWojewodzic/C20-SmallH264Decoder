from pathlib import Path
import re
r=Path('.routing')
raw=(r/'target.kicad_pcb').read_bytes()
orig=Path('C20W1B1V1.0.kicad_pcb').read_bytes()
old_end=orig.rfind(b'\n)')
data=raw[len(orig[:old_end+1]):-len(orig[old_end+1:])]
assert len(data)==len(raw)-len(orig)
def fix(rec):
    s=rec[0]
    net=re.search(rb'\(net "([^"]+)"\)',s)[1].decode()
    if net=='LTDC_G4':
        s=s.replace(b'97.4479 67.5953',b'97.4329 67.6003')
    elif net=='LTDC_R3':
        if any(x in s for x in (b'156.7553',b'156.8784',b'137.4087 156.4944')):
            return b''
    elif net=='LTDC_B6':
        if b'156.7553' in s:
            if b'88.5086 128.414' not in s:
                return b''
            s=s.replace(b'116.8499 156.7553',b'110.0946 150')
    return s
data=re.sub(rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n',fix,data,flags=re.M)
(r/'tb-seeds.kicad_pcb').write_bytes(orig[:old_end+1]+data+orig[old_end+1:])
