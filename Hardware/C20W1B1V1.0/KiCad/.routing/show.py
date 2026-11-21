from pathlib import Path
import re
r=Path('.routing')
b=(r/'target.kicad_pcb').read_bytes()
for net in ('LTDC_R3','LTDC_B6','LTDC_R7','LTDC_B2','LTDC_B4'):
    recs=[record[0] for record in re.finditer(rb'^\t\((?:segment|arc|via)\r?\n[\s\S]*?^\t\)\r?\n',b,re.M) if f'(net "{net}")'.encode() in record[0]]
    print(net,len(recs))
    for rec in recs:
        print(' '.join(re.findall(r'\((?:start|end|at|layer) [^)]+\)',rec.decode())))
