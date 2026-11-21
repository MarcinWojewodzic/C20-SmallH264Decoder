import struct, zipfile
from pathlib import Path
p=Path('.routing')
path='app/freerouting/management/jobs/RoutingJobSchedulerActionThread.class'
with zipfile.ZipFile(p/'router25.jar') as original:
    c=original.read(path)
    old=bytes.fromhex('00020002000000092a2ab40010b600c8b1')
    assert c.count(old)==1
    i=c.index(old)
    length=struct.unpack_from('>I',c,i-4)[0]
    code=bytes.fromhex('0000000200000001b100000000')
    patched=c[:i-4]+struct.pack('>I',len(code))+code+c[i+length:]
    out=p/'patch'/path
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(patched)
