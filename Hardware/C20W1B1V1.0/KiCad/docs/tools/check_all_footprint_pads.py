exec(open('docs/tools/review_2026_11_16.py',encoding='utf-8-sig').read().split('state={}')[0])
r=E.parse(out/'netlist.xml').getroot();libs={(l.get('lib'),l.get('part')):l for l in r.findall('./libparts/libpart')};results=[]
for c in r.findall('./components/comp'):
 ref=c.get('ref');fp=c.findtext('footprint') or '';lib,name=fp.split(':',1);p=pathlib.Path('Footprints' if lib=='Footprints' else 'C:/Program Files/KiCad/10.0/share/kicad/footprints/'+lib+'.pretty')/(name+'.kicad_mod')
 if not p.exists():results.append(dict(ref=ref,footprint=fp,error='missing file'));continue
 pads={x[1] for x in children(parse(p.read_text(encoding='utf-8')),'pad') if x[1]};ls=c.find('libsource');pins={x.get('num') for x in libs[(ls.get('lib'),ls.get('part'))].findall('./pins/pin')}
 results.append(dict(ref=ref,footprint=fp,symbol_pins=sorted(pins),footprint_pads=sorted(pads),missing_pads=sorted(pins-pads),extra_pads=sorted(pads-pins)))
(out/'footprint_pad_check.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('checked',len(results));print(json.dumps([x for x in results if x.get('error') or x.get('missing_pads') or x.get('extra_pads')],indent=2))
