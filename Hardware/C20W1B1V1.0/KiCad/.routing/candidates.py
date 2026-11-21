from pathlib import Path
import collections,json
import numpy as np
from scipy.ndimage import label

lib=Path('.routing/exact-grid.py').read_text()
exec(lib[:lib.index('for net,ends in sorted')].replace('cache=True','cache=False').replace('geom.json','repair-geom.json'))
allobs=g['obstacles']
bbox=x0,y0,nx,ny
results={}
for net in ['QSPI_CLK','/uC/SWCLK','/uC/RX','/uC/TX']:
    group=next(side for side in g['targets'][net] if side[0][0]==0)
    layer,cx,cy=group[0]
    radius=5.
    x0,y0,nx,ny=cx-radius,cy-radius,round(2*radius/resolution)+1,round(2*radius/resolution)+1
    subset=[(i,o) for i,o in enumerate(allobs) if min(o[3],o[5])<cx+radius+1 and max(o[3],o[5])>cx-radius-1 and min(o[4],o[6])<cy+radius+1 and max(o[4],o[6])>cy-radius-1]
    def flood(obs):
        g['obstacles']=obs
        tr,vi=masks(net,.220472 if net=='QSPI_CLK' else .102)
        labs,_=label(~tr[layer],np.ones((3,3)))
        _,y,x=cell(group[0])
        n=labs[y,x]
        area=labs==n if n else np.zeros_like(vi)
        return area,vi
    area,vi=flood([o for _,o in subset])
    print(net,area.sum(),int(np.count_nonzero(area&~vi)),flush=True)
    good=[]
    for j,o in subset:
        if str(j) not in g['editable'] or o[1]==net or math.dist(o[3:5],o[5:7])>8:
            continue
        candidate_area,candidate_via=flood([v for i,v in subset if i!=j])
        score=int(np.count_nonzero(candidate_area&~candidate_via))
        if score:
            good.append((score,j,o[1],g['editable'][str(j)]))
    results[net]=sorted(good,reverse=True)[:8]
    print(results[net],flush=True)
Path('.routing/candidates.json').write_text(json.dumps(results))
