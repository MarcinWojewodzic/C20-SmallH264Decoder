exec(open('docs/tools/review_2026_11_16.py',encoding='utf-8-sig').read().split('state={}')[0])
for name in ['Bosch_LGA-8_2.5x2.5mm_P0.65mm_ClockwisePinNumbering','Bosch_LGA-14_3x2.5mm_P0.5mm','LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y','LGA-16_3x3mm_P0.5mm']:
 p=pathlib.Path('C:/Program Files/KiCad/10.0/share/kicad/footprints/Package_LGA.pretty')/(name+'.kicad_mod');r=parse(p.read_text(encoding='utf-8'));print(name)
 for a in children(r,'pad'):print(a[1],children(a,'at'),children(a,'size'))
r=E.parse(out/'netlist.xml').getroot()
for n in r.findall('./nets/net'):
 nodes=n.findall('node')
 if any(p.get('ref') in ['U2','U8','J1','J2'] for p in nodes) and n.get('name') not in ['GND','+3V3']:print(n.get('name'), ' '.join(p.get('ref')+'.'+p.get('pin')+' '+str(p.get('pinfunction')) for p in nodes))
