from pathlib import Path
p=Path('.routing')
s=(p/'exact-geometry.py').read_text().replace('polygons=[]','polygons=[]\neditable={}')
s=s.replace('''        else:
            obstacles.append([1,net,1<<layer,*a,*z,t.GetWidth()/2e6])''','''        else:
            if net and net not in {'+3V3','GND'}:
                editable[len(obstacles)]=uid
            obstacles.append([1,net,1<<layer,*a,*z,t.GetWidth()/2e6])''')
s=s.replace('polygons=polygons,targets=', 'polygons=polygons,editable=editable,targets=')
s=s.replace("'geom.json'","'repair-geom.json'")
(p/'repair-geometry.py').write_text(s)
