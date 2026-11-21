import xml.etree.ElementTree as E, csv, pathlib, hashlib, json, re, collections
base=pathlib.Path('docs'); r=E.parse(base/'analysis/netlist.xml').getroot(); cs=r.findall('./components/comp'); ns=r.findall('./nets/net')
with (base/'components.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Value','Footprint','Sheet','Datasheet_in_project'])
 for c in cs:w.writerow([c.get('ref'),c.findtext('value'),c.findtext('footprint'),c.find('sheetpath').get('names'),c.findtext('datasheet','')])
with (base/'analysis/connections.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Net','Reference','Pin','Pin_function','Pin_type'])
 for n in ns:
  for p in n.findall('node'):w.writerow([n.get('name'),p.get('ref'),p.get('pin'),p.get('pinfunction'),p.get('pintype')])
rows=[]
for p in sorted((base/'datasheets').glob('*.pdf')):
 b=p.read_bytes();assert b.startswith(b'%PDF');rows.append(dict(file=p.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(base/'files.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
source=[]
for p in sorted((base/'download_logs').glob('sources*.json')):source.extend(json.loads(p.read_text(encoding='utf-8')))
(base/'download_log.json').write_text(json.dumps(source,indent=2),encoding='utf-8')
print('Components',len(cs),'Nets',len(ns),'PDFs',len(rows))
print(collections.Counter(re.findall(r'^\[([^]]+)\]',(base/'analysis/erc.rpt').read_text(encoding='utf-8'),re.M)))
for ref in ['J1','J2','U3']:
 print(ref)
 for n in ns:
  for p in n.findall('node'):
   if p.get('ref')==ref:print(p.get('pin'),p.get('pinfunction'),n.get('name'))

