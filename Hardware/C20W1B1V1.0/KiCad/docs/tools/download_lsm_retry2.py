import requests,pathlib,re,concurrent.futures,json
urls=['https://www.lcsc.com/datasheet/C46898862.pdf','https://datasheet.lcsc.com/lcsc/2505161701_STMicroelectronics-LSM6DSV80XTR_C46898862.pdf','https://www.st.com/content/ccc/resource/technical/document/datasheet/group4/b7/98/71/31/2c/a5/45/e7/DM01115474/files/DM01115474.pdf/jcr:content/translations/en.DM01115474.pdf']
def run(u):
 try:
  r=requests.get(u,timeout=15);print(u,r.status_code,len(r.content),r.content[:12])
  if r.content.startswith(b'%PDF'):pathlib.Path('docs/datasheets/LSM6DSV80X.pdf').write_bytes(r.content);return {'url':u,'size':len(r.content)}
  if 'lcsc.com/datasheet' in u:print(re.findall(r'https?[^\s"<>]+',r.text)[:15])
 except Exception as e:print(str(e))
res=list(concurrent.futures.ThreadPoolExecutor().map(run,urls));pathlib.Path('docs/analysis/review_2026-11-16/download_lsm_retry2.json').write_text(json.dumps(res,indent=2))
