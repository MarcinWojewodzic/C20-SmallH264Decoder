from pathlib import Path
g=Path('.routing/grid.py').read_text()
exec(g[:g.index('for net,ends in sorted')].replace('cache=True','cache=False'))
from scipy.ndimage import label
for net in ('QSPI_CLK','/uC/SWCLK','/uC/RX','/uC/TX','LTDC_CLK','LTDC_HS','LTDC_R6'):
    if net not in globals()['g']['targets']:
        continue
    track,via=masks(net,.220472 if net=='QSPI_CLK' else .127)
    print(net)
    for points in globals()['g']['targets'][net]:
        for l,x,y in points:
            _,yy,xx=cell((l,x,y))
            ids,_=label(~track[l],np.ones((3,3)))
            n=ids[yy,xx]
            region=ids==n if n else np.zeros((ny,nx),dtype=bool)
            print(l,x,y,'blocked',not n,'region',region.sum(),'via sites',np.count_nonzero(region&~via))
            if region.sum()<1500:
                rr=3.0
                print(sorted({o[1] for o in globals()['g']['obstacles'] if o[2]&(1<<l) and min(o[3],o[5])-rr<=x<=max(o[3],o[5])+rr and min(o[4],o[6])-rr<=y<=max(o[4],o[6])+rr}))

