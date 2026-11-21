import re,json,pathlib,xml.etree.ElementTree as E,collections,csv
out=pathlib.Path('docs/analysis/review_2026-11-13_2235')
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
state={}
for p in pathlib.Path('.').glob('*.kicad_sch'):
 root=parse(p.read_text(encoding='utf-8'))
 for a in root:
  if isinstance(a,list) and a and a[0]=='symbol':
   props={x[1]:x[2] for x in a if isinstance(x,list) and x and x[0]=='property'}
   ref=props.get('Reference','')
   if ref and not ref.startswith('#'):
    state[ref]={'sheet':p.name,'properties':props,'dnp':next((x[1] for x in a if isinstance(x,list) and x and x[0]=='dnp'),'unknown')}
(out/'symbol_properties.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
r=E.parse(out/'netlist.xml').getroot();old=E.parse('docs/analysis/netlist.xml').getroot()
oldcs={c.get('ref'):c.findtext('value') for c in old.findall('./components/comp')}
cs=r.findall('./components/comp'); ns=r.findall('./nets/net')
print('Components',len(cs),'Nets',len(ns),'new',len(cs)-len(oldcs))
for ref in ['R8','R9','R14','R15','R16']:print(ref,state[ref]['dnp'],state[ref]['properties'])
with (out/'components.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Value','Footprint','Sheet','DNP','Change'])
 for c in cs:
  ref=c.get('ref');value=c.findtext('value');w.writerow([ref,value,c.findtext('footprint'),c.find('sheetpath').get('names'),state[ref]['dnp'],'new' if ref not in oldcs else ('changed from '+oldcs[ref] if oldcs[ref]!=value else 'unchanged')])
with (out/'connections.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Net','Reference','Pin','Pin_function','Pin_type'])
 for n in ns:
  for p in n.findall('node'):w.writerow([n.get('name'),p.get('ref'),p.get('pin'),p.get('pinfunction'),p.get('pintype')])
manifest=[dict(file=p.name,sha256=__import__('hashlib').sha256(p.read_bytes()).hexdigest()) for p in sorted(pathlib.Path('.').glob('*.kicad_sch'))]
(out/'input_sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(collections.Counter(re.findall(r'^\[([^]]+)\]',(out/'erc.rpt').read_text(encoding='utf-8'),re.M)))
