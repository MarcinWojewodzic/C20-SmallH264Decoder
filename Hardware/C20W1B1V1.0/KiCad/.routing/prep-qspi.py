from pathlib import Path
p=Path('.routing')
s=(p/'exact-grid.py').read_text().replace('geom.json','repair-geom.json')
s=s.replace('''    for kind,name,layers,ax,ay,bx,by,r in g['obstacles']:
''','''    for kind,name,layers,ax,ay,bx,by,r in g['obstacles']:
        clearance=.103 if net.startswith('QSPI_') and name.startswith('QSPI_') else .1535
''')
s=s[:s.index('for net,ends in sorted')]
s+='''net='QSPI_CLK'
for width in (.220472,.1524,.127,.102):
    path=solve(net,g['targets'][net],width)
    print(width,len(path),flush=True)
    if path:
        (d/'qspi-route.json').write_text(json.dumps({net:[width,path]}))
        break
'''
(p/'qspi.py').write_text(s)
