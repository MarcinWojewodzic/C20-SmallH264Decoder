from pathlib import Path
p=Path('.routing')
s=(p/'tbfix.py').read_text()
i=s.index("    elif net=='LTDC_R3':")
j=s.index('    return s',i)
s=s[:i]+'''    elif net=='LTDC_R3':
        if any(x in s for x in (b'156.7553',b'156.8784',b'137.4087 156.4944')):
            return b''
    elif net=='LTDC_B6':
        if b'156.7553' in s:
            if b'88.5086 128.414' not in s:
                return b''
            s=s.replace(b'116.8499 156.7553',b'110.0946 150')
'''+s[j:]
s=s.replace('tb-fixed.kicad_pcb','tb-seeds.kicad_pcb')
(p/'tbseeds.py').write_text(s)
