import requests,pathlib,concurrent.futures,json,hashlib
urls=['https://www.st.com/resource/en/technical_note/CD00134799.pdf','https://www.mouser.cn/pdfDocs/tn0018-surface-mounting-guidelines-for-mems-sensors-in-an-lga-package-stmicroelectronics.pdf','https://www.mouser.cn/pdfdocs/enCD00134799.pdf']
def run(u):
 try:
  r=requests.get(u,timeout=15);r.raise_for_status()
  if not r.content.startswith(b'%PDF'):raise ValueError('not PDF')
  return u,r.content,None
 except Exception as e:return u,None,str(e)
logs=[]
for u,b,e in concurrent.futures.ThreadPoolExecutor().map(run,urls):
 if b:
  p=pathlib.Path('docs/datasheets')/('ST_TN0018.pdf' if 'www.st.com' in u else ('ST_TN0018_Mouser.pdf' if 'tn0018' in u else 'ST_TN0018_Mouser_older.pdf'));p.write_bytes(b);logs.append(dict(file=str(p),url=u,size=len(b),sha256=hashlib.sha256(b).hexdigest()))
 else:logs.append(dict(url=u,error=e))
pathlib.Path('docs/analysis/review_2026-11-16/download_TN0018.json').write_text(json.dumps(logs,indent=2));print(logs)
