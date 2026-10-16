"""Build full timestamped transcripts.
 align: punctuated transcript (sentences) + caption track -> "(h:mm:ss) sentence" lines, monotonic.
 chunk:  caption track only -> merged ~12s chunks with timestamps."""
import sys,re,difflib,html
norm=lambda s: re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",s.lower())).strip()
def load_caps(p):
    caps=[l for l in open(p).read().splitlines() if l.startswith("[")]
    st=[re.match(r"\[([^\]]+)\]",l).group(1) for l in caps]
    tx=[norm(re.sub(r"^\[[^\]]+\]\s*","",l)) for l in caps]
    return st,tx
def sentences(p):
    raw=open(p).read()
    raw=re.sub(r"^videoplayback.*\n","",raw)
    paras=[x.strip() for x in raw.split("\n") if x.strip()]
    out=[]
    for para in paras:
        for s in re.split(r'(?<=[.?!])\s+(?=[A-Z"\'])',para):
            s=s.strip()
            if not s: continue
            if len(s)>260:
                w=s.split(); 
                for i in range(0,len(w),22): out.append(" ".join(w[i:i+22]))
            else: out.append(s)
    return out
def align(tpath,cpath,out,title):
    st,tx=load_caps(cpath); sents=sentences(tpath)
    pos=0; lines=[]; n=len(tx); N=len(sents)
    for k,s in enumerate(sents):
        q=norm(s)
        expected=int(k/N*n)
        if len(q)<20:
            lines.append((st[min(pos,n-1)],s)); continue
        best=(0,None); lo=pos; hi=min(n,max(pos,expected)+150)
        for i in range(lo,hi):
            win=" ".join(tx[i:i+5])
            m=difflib.SequenceMatcher(None,q,win).find_longest_match(0,len(q),0,len(win)).size
            if m>best[0]: best=(m,i)
            if m>=len(q)*0.9: break
        if best[1] is not None and best[0]>=max(22,len(q)*0.6):
            pos=best[1]; lines.append((st[pos],s))
        else:
            lines.append((st[min(pos,n-1)],s))
    write(out,title,lines); return len(lines)
def chunk(cpath,out,title,secs=12):
    caps=[l for l in open(cpath).read().splitlines() if l.startswith("[")]
    def sec(ts):
        p=[int(x) for x in ts.split(":")]
        while len(p)<3: p.insert(0,0)
        return p[0]*3600+p[1]*60+p[2]
    lines=[]; cur=None; buf=[]
    for l in caps:
        ts=re.match(r"\[([^\]]+)\]",l).group(1); t=re.sub(r"^\[[^\]]+\]\s*","",l).strip()
        if t in ("[Music]","[Applause]") or not t: continue
        if cur is None: cur=ts
        buf.append(t)
        if sec(ts)-sec(cur)>=secs:
            lines.append((cur," ".join(buf))); cur=None; buf=[]
    if buf: lines.append((cur," ".join(buf)))
    write(out,title,lines); return len(lines)
def write(out,title,lines):
    h=[f"<h2>{html.escape(title)}</h2>"]
    for ts,s in lines: h.append(f"<p>({html.escape(ts)}) {html.escape(s)}</p>")
    open(out,"w").write("\n".join(h))
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="align": print(align(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]))
    else: print(chunk(sys.argv[2],sys.argv[3],sys.argv[4]))
