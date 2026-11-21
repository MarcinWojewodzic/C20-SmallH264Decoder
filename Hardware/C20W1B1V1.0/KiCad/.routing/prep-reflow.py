from pathlib import Path
p=Path('.routing')
s=(p/'exact-grid.py').read_text()
s=s.replace("g=json.loads((d/'geom.json').read_text())","g=json.loads((d/'reflow-geom.json').read_text())")
s=s.replace("for net,ends in sorted(g['targets'].items(),key=distance):","""priority='LTDC_R2 LTDC_R7 LTDC_HS LTDC_B1 LTDC_B2 LTDC_B6'.split()
for net,ends in sorted(g['targets'].items(),key=lambda item:(priority.index(item[0]) if item[0] in priority else 10,distance(item))):""")
s=s.replace('exact-routes.json','reflow-routes.json')
(p/'reflow.py').write_text(s)
