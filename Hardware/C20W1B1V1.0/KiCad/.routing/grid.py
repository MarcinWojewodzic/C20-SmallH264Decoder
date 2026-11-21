from pathlib import Path
import heapq,json,math,sys,time

import numba as nb
import numpy as np

d=Path('.routing')
g=json.loads((d/'geom.json').read_text())
routes={}
resolution=float(sys.argv[1]) if len(sys.argv)>1 else .05
x0,y0,x1,y1=g['bounds']
nx,ny=int((x1-x0)/resolution)+1,int((y1-y0)/resolution)+1
clearance=.1535
margin=.009

def paint(mask,kind,a,b,r):
    ax,ay=a
    bx,by=b
    i=max(0,int(math.floor((min(ax,bx)-r-x0)/resolution)))
    j=max(0,int(math.floor((min(ay,by)-r-y0)/resolution)))
    k=min(nx,int(math.ceil((max(ax,bx)+r-x0)/resolution))+1)
    l=min(ny,int(math.ceil((max(ay,by)+r-y0)/resolution))+1)
    if i>=k or j>=l:
        return
    x=x0+np.arange(i,k)[None,:]*resolution
    y=y0+np.arange(j,l)[:,None]*resolution
    if kind==0:
        dx=np.maximum(0,np.maximum(ax-x,x-bx))
        dy=np.maximum(0,np.maximum(ay-y,y-by))
    else:
        ux,uy=bx-ax,by-ay
        t=np.clip(((x-ax)*ux+(y-ay)*uy)/(ux*ux+uy*uy),0,1) if ux or uy else 0
        dx=x-ax-t*ux
        dy=y-ay-t*uy
    mask[...,j:l,i:k] |= dx*dx+dy*dy<r*r

def masks(net,width):
    track=np.zeros((3,ny,nx),dtype=np.bool_)
    via=np.zeros((ny,nx),dtype=np.bool_)
    for kind,name,layers,ax,ay,bx,by,r in g['obstacles']:
        a=(ax,ay)
        b=(bx,by)
        if kind==2:
            paint(via,1,a,b,r+.15+.25+margin)
            continue
        if net==name:
            if kind==0:
                paint(via,kind,a,b,.25+margin)
            continue
        paint(via,kind,a,b,r+.25+clearance+margin)
        for layer in range(3):
            if layers & (1<<layer):
                paint(track[layer],kind,a,b,r+width/2+clearance+margin)
    for mask,inset in [(track,.5+width/2),(via,.5+.25)]:
        n=math.ceil((inset+.025+margin)/resolution)
        mask[...,:n,:]=True
        mask[...,-n:,:]=True
        mask[...,:,:n]=True
        mask[...,:,-n:]=True
    return track,via

@nb.njit(cache=True)
def astar(track,via,starts,goals,via_cost):
    _,ny,nx=track.shape
    costs=np.full((3,ny,nx),2147483647,np.int32)
    parents=np.full((3,ny,nx),-1,np.int8)
    queue=[(0,0,0,0,0)]
    queue.pop()
    for s in starts:
        l,y,x=s
        if not track[l,y,x]:
            costs[l,y,x]=0
            heapq.heappush(queue,(0,0,l,y,x))
    dy=(0,1,-1,0,1,1,-1,-1)
    dx=(1,0,0,-1,1,-1,1,-1)
    rev=(3,2,1,0,7,6,5,4)
    while queue:
        _,d,l,y,x=heapq.heappop(queue)
        if d!=costs[l,y,x]:
            continue
        for gl,gy,gx in goals:
            if l==gl and y==gy and x==gx:
                path=[(l,y,x)]
                while parents[l,y,x]>=0:
                    p=parents[l,y,x]
                    if p>=8:
                        l=p-8
                    else:
                        y+=dy[p]
                        x+=dx[p]
                    path.append((l,y,x))
                return path
        for i in range(11):
            if i<8:
                ll=l
                yy=y+dy[i]
                xx=x+dx[i]
                if yy<0 or yy>=ny or xx<0 or xx>=nx:
                    continue
                dd=d+(10 if i<4 else 14)
                pp=rev[i]
            else:
                ll=i-8
                if ll==l or via[y,x]:
                    continue
                yy=y
                xx=x
                dd=d+via_cost
                pp=8+l
            if track[ll,yy,xx] or costs[ll,yy,xx]<=dd:
                continue
            h=2147483647
            for gl,gy,gx in goals:
                hy=abs(yy-gy)
                hx=abs(xx-gx)
                h=min(h,10*max(hy,hx)+4*min(hy,hx)+(via_cost if gl!=ll else 0))
            costs[ll,yy,xx]=dd
            parents[ll,yy,xx]=pp
            heapq.heappush(queue,(dd+h,dd,ll,yy,xx))
    return [(0,-1,-1)]

def cell(pt):
    l,x,y=pt
    return (l,round((y-y0)/resolution),round((x-x0)/resolution))

def coord(c):
    l,y,x=c
    return (l,round(x0+x*resolution,6),round(y0+y*resolution,6))

def solve(net,pair,width):
    masks0=masks(net,width)
    seeds=[{cell(p):tuple(p) for p in group} for group in pair]
    starts,goals=(np.array(list(group),dtype=np.int64) for group in seeds)
    path=astar(*masks0,starts,goals,round(3/resolution)*10)
    if len(path)<2:
        return []
    path=path[::-1]
    simple=[path[0]]
    direction=None
    for a,b in zip(path,path[1:]):
        delta=tuple(y-x for x,y in zip(a,b))
        if delta!=direction:
            if a!=simple[-1]:
                simple.append(a)
            direction=delta
    simple.append(path[-1])
    points=[seeds[0][path[0]],*(coord(c) for c in simple),seeds[1][path[-1]]]
    for a,b in zip(points,points[1:]):
        la,x,y=a
        lb,xx,yy=b
        if a==b:
            continue
        if la==lb:
            g['obstacles'].append([1,net,1<<la,x,y,xx,yy,width/2])
        else:
            g['obstacles'].append([1,net,7,x,y,x,y,.25])
            g['obstacles'].append([2,net,7,x,y,x,y,.15])
    return points

def distance(item):
    (a,_),(b,_)=((points[0][1:],points[0][0]) for points in item[1])
    return math.dist(a,b)

for net,ends in sorted(g['targets'].items(),key=distance):
    start=time.monotonic()
    width=.220472 if net=='QSPI_CLK' else .1524
    path=solve(net,ends,width)
    if not path and net!='QSPI_CLK':
        width=.127
        path=solve(net,ends,width)
    if path:
        routes[net]=[width,path]
    print(net,len(path),round(time.monotonic()-start,2),flush=True)
    (d/'grid-routes.json').write_text(json.dumps(routes))
