import sys,re,html
# Convert YouTube auto-sub VTT (rolling duplicates) into "[h:mm:ss] text" lines without repeats.
lines=open(sys.argv[1],encoding='utf-8').read().splitlines()
out=[];last=""
i=0
while i<len(lines):
    m=re.match(r'(\d+):(\d\d):(\d\d)\.\d+ --> ',lines[i])
    if m:
        ts=f"{int(m.group(1))}:{m.group(2)}:{m.group(3)}"
        i+=1; txt=[]
        while i<len(lines) and lines[i].strip()!="":
            t=re.sub(r'<[^>]+>','',lines[i]).strip()
            if t and t!=last and not (last and t in last): txt.append(t)
            i+=1
        if txt:
            t=" ".join(txt); 
            if t!=last: out.append(f"[{ts}] {html.unescape(t)}"); last=t
    else: i+=1
open(sys.argv[2],"w").write("\n".join(out))
print(sys.argv[2], len(out), "lines")
