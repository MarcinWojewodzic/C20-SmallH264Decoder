from pathlib import Path
p=Path('.routing')
s=(p/'geometry.py').read_text().replace('obstacles=[]','obstacles=[]\npolygons=[]')
s=s.replace('''        if layer_mask:
            obstacles.append([0,net,layer_mask,*point(box.GetOrigin()),*point(box.GetEnd()),0])''','''        if layer_mask:
            if pad.GetShape() == p.PAD_SHAPE_RECT and abs(pad.GetOrientationDegrees()%90)<.001:
                obstacles.append([0,net,layer_mask,*point(box.GetOrigin()),*point(box.GetEnd()),0])
            else:
                poly=p.SHAPE_POLY_SET()
                pad.TransformShapeToPolygon(poly,next(l for l in layers if pad.IsOnLayer(l)),0,1000,p.ERROR_OUTSIDE)
                for i in range(poly.OutlineCount()):
                    line=poly.Outline(i)
                    polygons.append([point(line.CPoint(j)) for j in range(line.PointCount())])
                    obstacles.append([3,net,layer_mask,*point(box.GetOrigin()),*point(box.GetEnd()),len(polygons)-1])''')
s=s.replace('dict(obstacles=obstacles,targets=', 'dict(obstacles=obstacles,polygons=polygons,targets=')
(p/'exact-geometry.py').write_text(s)
s=(p/'grid.py').read_text()
s=s.replace('margin=.009','margin=.004')
s=s.replace('def paint(mask,kind,a,b,r):','def paint(mask,kind,a,b,r,polygon=None):')
s=s.replace('''    if kind==0:
        dx=''','''    if kind==3:
        hit=np.zeros((l-j,k-i),dtype=np.bool_)
        inside=np.zeros_like(hit)
        for (px,py),(qx,qy) in zip(polygon,polygon[1:]+polygon[:1]):
            ux,uy=qx-px,qy-py
            if ux or uy:
                t=np.clip(((x-px)*ux+(y-py)*uy)/(ux*ux+uy*uy),0,1)
                hit |= (x-px-t*ux)**2+(y-py-t*uy)**2<r*r
            if uy:
                inside ^= ((py>y)!=(qy>y)) & (x<(y-py)*ux/uy+px)
        mask[...,j:l,i:k] |= hit|inside
        return
    if kind==0:
        dx=''')
s=s.replace('''        a=(ax,ay)
        b=(bx,by)''','''        a=(ax,ay)
        b=(bx,by)
        poly=g['polygons'][int(r)] if kind==3 else None
        if kind==3:
            r=0''')
s=s.replace('''if kind==0:
                paint(via,kind,a,b,.25+margin)''','''if kind in (0,3):
                paint(via,kind,a,b,.25+margin,poly)''')
s=s.replace('r+.25+clearance+margin)','r+.25+clearance+margin,poly)').replace('r+width/2+clearance+margin)','r+width/2+clearance+margin,poly)')
s=s.replace('width=.127','width=.102')
s=s.replace("(d/'grid-routes.json')","(d/'exact-routes.json')")
(p/'exact-grid.py').write_text(s)
