import requests,pathlib,concurrent.futures,json,hashlib
urls=['https://www.mouser.cn/pdfDocs/lsm6dsv80x-2.pdf','https://www.mouser.com/pdfDocs/lsm6dsv80x-2.pdf','https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6678/LSM6DSV80X.pdf']
def run(u):
 try:
  r=requests.get(u,timeout=18);r.raise_for_status()
  if not r.content.startswith(b'%PDF'):raise ValueError('not PDF')
  return u,r.content,None
 except Exception as e:return u,None,str(e)
logs=[]
for u,b,e in concurrent.futures.ThreadPoolExecutor().map(run,urls):
 if b:
  p=pathlib.Path('docs/datasheets')/('LSM6DSV80X_Rev1_DigiKey.pdf' if 'digikey' in u else 'LSM6DSV80X.pdf');p.write_bytes(b);logs.append(dict(file=str(p),url=u,size=len(b),sha256=hashlib.sha256(b).hexdigest()))
 else:logs.append(dict(url=u,error=e))
pathlib.Path('docs/analysis/review_2026-11-16/download_lsm_final.json').write_text(json.dumps(logs,indent=2));print(logs)
