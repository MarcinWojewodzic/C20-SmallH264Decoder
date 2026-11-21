import collections,json,re,sys
from pathlib import Path
def load(filename):
    return json.loads(Path(filename).read_text(encoding='utf-8-sig'))
a,b=map(load,sys.argv[1:3])
def key(v):
    return (v['type'],tuple(sorted(i['uuid'] for i in v['items'])))
old={key(v) for v in a['violations']}
new=[v for v in b['violations'] if key(v) not in old]
for r in (a,b):
    print(collections.Counter(v['type'] for v in r['violations']))
    print(collections.Counter(re.search(r'\[([^\]]+)\]',v['items'][0]['description'])[1] for v in r['unconnected_items']))
print('New violations:',len(new))
for v in new:
    print(v['type'],v['description'],*[i['description']+str(i['pos']) for i in v['items']])
