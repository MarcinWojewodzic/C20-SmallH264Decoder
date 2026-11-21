import requests,concurrent.futures,pathlib,json,hashlib,re
base=pathlib.Path('docs'); out=base/'datasheets'
u={
'STM32H753_datasheet':'https://www.st.com/resource/en/datasheet/stm32h753ii.pdf',
'RM0433':'https://www.st.com/resource/en/reference_manual/rm0433-stm32h743-753-and-stm32h750-value-line-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf',
'ES0392':'https://www.st.com/resource/en/errata_sheet/es0392-stm32h742xig-and-stm32h743xig-device-limitations-stmicroelectronics.pdf',
'AN4938':'https://www.st.com/resource/en/application_note/an4938-getting-started-with-stm32h74xig-and-stm32h75xig-mcu-hardware-development-stmicroelectronics.pdf',
'PM0253':'https://www.st.com/resource/en/programming_manual/pm0253-stm32f7-series-and-stm32h7-series-cortexm7-processor-programming-manual-stmicroelectronics.pdf',
'IS45S32400J':'https://www.issi.com/WW/pdf/42-45S32400J.pdf',
'TPS923610':'https://www.ti.com/lit/ds/symlink/tps923610.pdf',
'AOTA-B252008S':'https://abracon.com/datasheets/AOTA-B252008S.pdf',
'Molex_522710679_drawing':'https://www.molex.com/pdm_docs/sd/522710679_sd.pdf',
'Panasonic_low_resistance_ERJ':'https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C331.pdf',
}
def get(item):
 n,url=item
 try:
  r=requests.get(url,timeout=50);r.raise_for_status()
  if not r.content.startswith(b'%PDF'): raise ValueError('Response is not PDF')
  (out/(n+'.pdf')).write_bytes(r.content)
  return dict(name=n,url=url,status='ok',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:return dict(name=n,url=url,status='failed',error=str(e))
res=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(get,u.items()))
(base/'sources.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
