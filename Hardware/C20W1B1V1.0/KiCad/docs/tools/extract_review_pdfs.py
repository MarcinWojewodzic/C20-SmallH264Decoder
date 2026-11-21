import os,sys,pathlib
sys.path.insert(0,os.path.join(os.environ['TEMP'],'codex_pdf_review'))
from pypdf import PdfReader
import pypdfium2 as pdfium
out=pathlib.Path('docs/analysis/review_2026-11-16')
for name,pages in [('BME280',[37,38,41,42]),('MMC5983MA',[9,10,19]),('NHD-4.0-480480AF-ASXP-CTP',[3,4,5]),('FT5426G',[])]:
 p=pathlib.Path('docs/datasheets')/(name+'.pdf');r=PdfReader(p)
 (out/(name+'.txt')).write_text('\n'.join(f'\nPAGE {i+1}\n'+(x.extract_text() or '') for i,x in enumerate(r.pages)),encoding='utf-8')
 d=pdfium.PdfDocument(str(p))
 for i in pages:
  if i<len(d):d[i].render(scale=1.8).to_pil().save(out/(name+'_p'+str(i+1)+'.png'))
print('PDF extraction complete')
