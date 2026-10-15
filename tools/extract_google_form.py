import re, json, sys, html
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
m = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (.*?);</script>', s, re.S)
if not m:
    print("NO FB_PUBLIC_LOAD_DATA"); sys.exit()
data = json.loads(m.group(1))
def walk(o, out):
    if isinstance(o, str):
        if len(o) > 1: out.append(o)
    elif isinstance(o, list):
        for x in o: walk(x, out)
out=[]
walk(data, out)
seen=set()
for t in out:
    if t in seen: continue
    seen.add(t)
    print("-", html.unescape(t))
print("\n==== LINKS ====")
for u in sorted(set(re.findall(r'https?://[^\s"\'<>\\]+', s))):
    if 'gstatic' in u or 'googleapis' in u or 'google.com/forms' in u or 'schema.org' in u or 'w3.org' in u: continue
    print(u)
