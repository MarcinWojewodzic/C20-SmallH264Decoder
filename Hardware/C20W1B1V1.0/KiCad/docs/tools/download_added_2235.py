import requests,concurrent.futures,pathlib,json,hashlib
urls={'TPS54495':'https://www.ti.com/lit/ds/symlink/tps54495.pdf','MAX98357A_MAX98357B':'https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf','AOTA-B252010S':'https://abracon.com/datasheets/AOTA-B252010S.pdf','Kyocera_clock_Z_XZ':'https://global.kyocera.com/prdct/electro/product/pdf/clock_z_xz_e.pdf'}
def get(x):
 n,u=x
 try:
  r=requests.get(u,timeout=25);r.raise_for_status();assert r.content.startswith(b'%PDF'),'not PDF';pathlib.Path('docs/datasheets/'+n+'.pdf').write_bytes(r.content);return dict(name=n,url=u,status='ok',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:return dict(name=n,url=u,status='failed',error=str(e))
r=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,urls.items()));pathlib.Path('docs/download_logs/sources_added_2235.json').write_text(json.dumps(r,indent=2));print(r)
