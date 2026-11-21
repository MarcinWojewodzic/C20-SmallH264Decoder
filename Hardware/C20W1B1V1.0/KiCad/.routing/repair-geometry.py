import json,sys,re,math
from pathlib import Path
import pcbnew as p

def point(v):
    return [v.x/1e6,v.y/1e6]

layers=[p.F_Cu,p.In3_Cu,p.B_Cu]
b=p.LoadBoard(sys.argv[1])
report=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'))
targets={}
for item in report['unconnected_items']:
    a=item['items']
    net=re.search(r'\[([^\]]+)\]',a[0]['description'])[1]
    if net not in {'+3V3','GND'}:
        targets[net]=[v['uuid'] for v in a]
needed={u for pair in targets.values() for u in pair}
objects={}
obstacles=[]
polygons=[]
editable={}
for f in b.GetFootprints():
    for pad in f.Pads():
        net=str(pad.GetNetname())
        layer_mask=sum(1<<i for i,l in enumerate(layers) if pad.IsOnLayer(l))
        box=pad.GetBoundingBox()
        pos=point(pad.GetPosition())
        if layer_mask:
            if pad.GetShape() == p.PAD_SHAPE_RECT and abs(pad.GetOrientationDegrees()%90)<.001:
                obstacles.append([0,net,layer_mask,*point(box.GetOrigin()),*point(box.GetEnd()),0])
            else:
                poly=p.SHAPE_POLY_SET()
                pad.TransformShapeToPolygon(poly,next(l for l in layers if pad.IsOnLayer(l)),0,1000,p.ERROR_OUTSIDE)
                for i in range(poly.OutlineCount()):
                    line=poly.Outline(i)
                    polygons.append([point(line.CPoint(j)) for j in range(line.PointCount())])
                    obstacles.append([3,net,layer_mask,*point(box.GetOrigin()),*point(box.GetEnd()),len(polygons)-1])
        if pad.HasDrilledHole():
            dx,dy=point(pad.GetDrillSize())
            obstacles.append([2,net,7,*pos,*pos,max(dx,dy)/2])
        uid=pad.m_Uuid.AsString()
        if uid in needed:
            objects[uid]=[[i,*pos] for i in range(3) if layer_mask & (1<<i)]
for t in b.GetTracks():
    net=str(t.GetNetname())
    uid=t.m_Uuid.AsString()
    if isinstance(t,p.PCB_VIA):
        pos=point(t.GetPosition())
        obstacles.append([1,net,7,*pos,*pos,t.GetWidth(p.F_Cu)/2e6])
        obstacles.append([2,net,7,*pos,*pos,t.GetDrillValue()/2e6])
        if uid in needed:
            objects[uid]=[[i,*pos] for i in range(3)]
    elif t.GetLayer() in layers:
        layer=layers.index(t.GetLayer())
        a=point(t.GetStart())
        z=point(t.GetEnd())
        path=[a,z]
        if isinstance(t,p.PCB_ARC):
            cx,cy=point(t.GetCenter())
            angle=math.atan2(a[1]-cy,a[0]-cx)
            end=math.atan2(z[1]-cy,z[0]-cx)
            delta=(end-angle+math.pi)%(2*math.pi)-math.pi
            radius=math.dist(a,(cx,cy))
            path=[a]+[(cx+radius*math.cos(angle+delta*i/12),cy+radius*math.sin(angle+delta*i/12)) for i in range(1,12)]+[z]
            for left,right in zip(path,path[1:]):
                obstacles.append([1,net,1<<layer,*left,*right,t.GetWidth()/2e6+.001])
        else:
            if net and net not in {'+3V3','GND'}:
                editable[len(obstacles)]=uid
            obstacles.append([1,net,1<<layer,*a,*z,t.GetWidth()/2e6])
        if uid in needed:
            objects[uid]=[[layer,*v] for v in path]
bounds=b.GetBoardEdgesBoundingBox()
print('targets',len(targets),'objects',len(objects),'obstacles',len(obstacles))
Path('.routing/repair-geom.json').write_text(json.dumps(dict(obstacles=obstacles,polygons=polygons,editable=editable,targets={n:[objects[u] for u in pair] for n,pair in targets.items()},bounds=[*point(bounds.GetOrigin()),*point(bounds.GetEnd())])))


