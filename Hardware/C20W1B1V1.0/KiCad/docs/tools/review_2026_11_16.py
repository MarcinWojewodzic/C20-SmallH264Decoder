import re,json,pathlib,xml.etree.ElementTree as E,collections,csv,hashlib
out=pathlib.Path('docs/analysis/review_2026-11-16')
def parse(text):
 toks=iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text))
 def item(t):
  if t=='(':
   a=[]
   for k in toks:
    if k==')':return a
    a.append(item(k))
  if t.startswith('"'):return json.loads(t)
  return t
 return item(next(toks))
def children(a,key):return [x for x in a if isinstance(x,list) and x and x[0]==key]
state={}
for p in pathlib.Path('.').glob('*.kicad_sch'):
 root=parse(p.read_text(encoding='utf-8'))
 for a in children(root,'symbol'):
  props={x[1]:x[2] for x in children(a,'property')};ref=props.get('Reference','')
  if ref and not ref.startswith('#'):state[ref]={'sheet':p.name,'properties':props,'dnp':children(a,'dnp')}
 if p.name=='Sensors.kicad_sch':
  for lib in children(children(root,'lib_symbols')[0],'symbol'):
   print('\nSYMBOL',lib[1])
   for unit in children(lib,'symbol'):
    for pin in children(unit,'pin'):print(children(pin,'number')[0][1],children(pin,'name')[0][1],pin[1], 'hidden' if 'hide' in str(pin) else '')
r=E.parse(out/'netlist.xml').getroot();ns=r.findall('./nets/net');cs=r.findall('./components/comp')
print('COUNTS',len(cs),len(ns))
for c in cs:
 ref=c.get('ref')
 if ref.startswith('U') or ref in ['C55','C72','C73']: print('COMP',ref,c.findtext('value'),c.findtext('footprint'),c.find('sheetpath').get('names'))
for n in ns:
 nodes=n.findall('node')
 if any(x.get('ref') in ['U7','U9','U?'] for x in nodes) or 'I2C' in n.get('name').upper():print('NET',n.get('name'),' '.join(x.get('ref')+'.'+x.get('pin')+'('+str(x.get('pinfunction'))+')' for x in nodes))
with (out/'connections.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Net','Reference','Pin','Function','Type'])
 for n in ns:
  for p in n.findall('node'):w.writerow([n.get('name'),p.get('ref'),p.get('pin'),p.get('pinfunction'),p.get('pintype')])
(out/'symbol_properties.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
(out/'input_sha256.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path('.').glob('*.kicad_sch')},indent=2),encoding='utf-8')
old=E.parse('docs/analysis/review_2026-11-14/netlist.xml').getroot()
def mapping(root):return {(p.get('ref'),p.get('pin')):n.get('name') for n in root.findall('./nets/net') for p in n.findall('node')}
a,b=mapping(old),mapping(r)
print('CHANGES OLD PINS',[(k,v,b.get(k)) for k,v in a.items() if b.get(k)!=v])
