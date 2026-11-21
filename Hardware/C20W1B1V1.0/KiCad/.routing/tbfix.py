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
        def clamp(m):
            x,y=map(float,m.groups())
            if y>156.68:
                return (' %.6f %.6f)'%(x,156.68)).encode()
            return m[0]
        s=re.sub(rb' (?P<x>\d+\.\d+) (?P<y>\d+\.\d+)\)',clamp,s)
    elif net=='TFT_CLK_SPI':
        s=s.replace(b'104.7891 58.6631',b'104.7301 58.6091')
    elif net=='LTDC_B6':
        return b''
    return s
data=re.sub(rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n',fix,data,flags=re.M)
(r/'tb-fixed.kicad_pcb').write_bytes(orig[:old_end+1]+data+orig[old_end+1:])
