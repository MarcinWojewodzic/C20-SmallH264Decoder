from pathlib import Path
p=Path('.routing')
s=(p/'grid.py').read_text()
s=s.replace('via=np.zeros((ny,nx),dtype=np.bool_)','via=np.zeros((3,ny,nx),dtype=np.bool_)')
s=s.replace('''        paint(via,kind,a,b,r+.25+clearance+margin)''','''        for i,span in enumerate((3,6,7)):
            if layers & span:
                paint(via[i],kind,a,b,r+.25+clearance+margin)''')
s=s.replace('''if ll==l or via[y,x]:
                    continue
                yy=y
                xx=x
                dd=d+via_cost''','''if ll==l:
                    continue
                span=0 if l+ll==1 else (1 if l+ll==3 else 2)
                if via[2,y,x] and via[span,y,x]:
                    continue
                yy=y
                xx=x
                dd=d+via_cost+(100 if via[2,y,x] else 0)''')
s=s.replace('''    for a,b in zip(points,points[1:]):
''','''    blind=[]
    for a,b in zip(points,points[1:]):
''').replace('''            g['obstacles'].append([1,net,7,x,y,x,y,.25])
            g['obstacles'].append([2,net,7,x,y,x,y,.15])
    return points''','''            _,gy,gx=cell(a)
            span=(1<<la)|(1<<lb) if masks0[1][2,gy,gx] else 7
            if span!=7:
                blind.append([x,y])
            g['obstacles'].append([1,net,span,x,y,x,y,.25])
            g['obstacles'].append([2,net,span,x,y,x,y,.15])
    return points,blind''')
s=s.replace('''    path=solve(net,ends,width)''','''    found=solve(net,ends,width)''',1)
s=s.replace('''    if not path and net!='QSPI_CLK':
        width=.127
        path=solve(net,ends,width)
    if path:
        routes[net]=[width,path]
    print(net,len(path),round(time.monotonic()-start,2),flush=True)
    (d/'grid-routes.json').write_text(json.dumps(routes))''','''    if not found and net!='QSPI_CLK':
        width=.105
        found=solve(net,ends,width)
    if found:
        path,blind=found
        routes[net]=[width,path,blind]
    print(net,len(found[0]) if found else 0,round(time.monotonic()-start,2),flush=True)
    (d/'blind-routes.json').write_text(json.dumps(routes))''')
(p/'blind.py').write_text(s)
