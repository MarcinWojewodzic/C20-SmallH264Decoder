import requests,concurrent.futures,pathlib,json,hashlib
urls={
'Amphenol_62684_drawing':'https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/62684.pdf',
'Amphenol_62684_spec':'https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/110-450h.pdf',
'Amphenol_FPC_application':'https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-097.pdf',
'Amphenol_OPU_datasheet':'https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/flex/flexconnectors_050mm_opu.pdf'}
def get(x):
 n,u=x
 try:
  r=requests.get(u,timeout=35);r.raise_for_status();assert r.content.startswith(b'%PDF');pathlib.Path('docs/datasheets/'+n+'.pdf').write_bytes(r.content)
  return dict(name=n,url=u,status='ok',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:return dict(name=n,url=u,status='failed',error=str(e))
r=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,urls.items()))
pathlib.Path('docs/sources_connectors.json').write_text(json.dumps(r,indent=2));print(r)
