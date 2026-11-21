import requests,concurrent.futures,pathlib,json,hashlib
urls={
'STM32H753_mirror':'https://www.lcsc.com/datasheet/C114410.pdf',
'ISSI_mirror':'https://www.issi.com/WW/pdf/42-45S32400J.pdf?download=1',
'Molex_drawing_mirror':'https://www.mouser.com/datasheet/2/276/522710679_sd-232670.pdf',
'Panasonic_ERJ':'https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/AOA0000C313.pdf',
'Amphenol_drawing_mirror':'https://datasheet.ersaelectronics.com/static/datasheets/amphenol-communications-solutions/amphenol-communications-solutions-62684-452121ahlf.pdf',
'AN4938_mirror':'https://raw.githubusercontent.com/sparkfun/SparkFun_Qwiic_WAV_Trigger_Pro/main/docs/assets/component_documentation/an4938-getting-started-with-stm32h74xig-and-stm32h75xig-mcu-hardware-development-stmicroelectronics.pdf'}
def f(x):
 n,u=x
 try:
  r=requests.get(u,timeout=15);r.raise_for_status();assert r.content.startswith(b'%PDF'),'not PDF';pathlib.Path('docs/datasheets/'+n+'.pdf').write_bytes(r.content)
  return dict(name=n,url=u,status='ok',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:return dict(name=n,url=u,status='failed',error=str(e))
r=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(f,urls.items()));pathlib.Path('docs/sources_mirrors.json').write_text(json.dumps(r,indent=2));print(r)
