import os,sys,pathlib
sys.path.insert(0,os.path.join(os.environ['TEMP'],'codex_pdf_review'))
from pypdf import PdfReader
for name in ['STM32H753_DS12117_octopart','IS45S32400J_datasheet','TPS923610','TPS54495']:
 r=PdfReader('docs/datasheets/'+name+'.pdf');out=pathlib.Path('docs/analysis/review_2026-11-16')/(name+'.txt');out.write_text('\n'.join(f'\nPAGE {i+1}\n'+(p.extract_text() or '') for i,p in enumerate(r.pages)),encoding='utf-8')
print('done')
