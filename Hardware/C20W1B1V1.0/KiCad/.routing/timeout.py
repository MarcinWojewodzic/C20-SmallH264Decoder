import struct,zipfile
from pathlib import Path
p=Path('.routing')
path='app/freerouting/autoroute/pipeline/AutorouteConnectionRouter.class'
with zipfile.ZipFile(p/'router25.jar') as z:
    c=z.read(path)
    old=bytes([6])+struct.pack('>d',100000)
    assert c.count(old)==1
    target=p/'patch'/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(c.replace(old,bytes([6])+struct.pack('>d',2000)))
