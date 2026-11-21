import requests,pathlib,concurrent.futures,json,hashlib,time
jobs={
'BME280.pdf':['https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf'],
'LSM6DSV80X.pdf':['https://www.st.com/resource/en/datasheet/lsm6dsv80x.pdf','https://www.st.com.cn/resource/en/datasheet/lsm6dsv80x.pdf'],
'MMC5983MA.pdf':['https://www.memsic.com/Public/Uploads/uploadfile/files/20220119/MMC5983MADatasheetRevA.pdf','https://s3.amazonaws.com/snapeda/datasheet/MMC5983MA_Memsic_Inc.pdf']}
def run(pair):
 name,urls=pair;logs=[]
 for url in urls:
  try:
   r=requests.get(url,timeout=25);r.raise_for_status()
   if not r.content.startswith(b'%PDF'):raise ValueError('Not PDF')
   p=pathlib.Path('docs/datasheets')/name;p.write_bytes(r.content)
   logs.append(dict(file=str(p),url=url,size=len(r.content),sha256=hashlib.sha256(r.content).hexdigest()));break
  except Exception as e:logs.append(dict(url=url,error=str(e)))
 return logs
logs=list(concurrent.futures.ThreadPoolExecutor().map(run,jobs.items()))
pathlib.Path('docs/analysis/review_2026-11-16/download_log.json').write_text(json.dumps(logs,indent=2),encoding='utf-8');print(json.dumps(logs,indent=2))
