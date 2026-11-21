import requests,pathlib,concurrent.futures,json,hashlib
urls=['https://www.st.com/resource/en/datasheet/dm01115474.pdf','https://www.st.com.cn/resource/en/datasheet/dm01115474.pdf','https://www.mouser.com/datasheet/2/389/lsm6dsv80x-3524424.pdf']
def run(url):
 try:
  r=requests.get(url,timeout=20);r.raise_for_status()
  if not r.content.startswith(b'%PDF'):raise ValueError('not PDF')
  return url,r.content,None
 except Exception as e:return url,None,str(e)
logs=[]
for u,b,e in concurrent.futures.ThreadPoolExecutor().map(run,urls):
 if b:
  p=pathlib.Path('docs/datasheets/LSM6DSV80X.pdf')
  if not p.exists():p.write_bytes(b)
  logs.append(dict(url=u,size=len(b),sha256=hashlib.sha256(b).hexdigest()))
 else:logs.append(dict(url=u,error=e))
pathlib.Path('docs/analysis/review_2026-11-16/download_lsm_retry.json').write_text(json.dumps(logs,indent=2),encoding='utf-8');print(logs)
