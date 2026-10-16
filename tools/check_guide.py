"""Check a script HTML against the RTC writing guide:
 - narration breaks (consecutive narration paragraphs with no clip between) <= ~60 s (~150 words at 2.5 w/s)
 - clip runs between narration breaks <= ~3 min
 - single clips <= 3 min
 - total narration + transcription word counts
"""
import re,sys,html
WPS=2.5
def sec(ts):
    p=[int(x) for x in ts.split(":")]
    while len(p)<3: p.insert(0,0)
    return p[0]*3600+p[1]*60+p[2]
def check(path):
    h=open(path).read().split("APPENDIX")[0]
    items=[]
    for m in re.finditer(r'<(h2|p)>(.*?)</\1>',h,re.S):
        body=m.group(2)
        if m.group(1)=="h2": items.append(("H",re.sub("<[^>]+>","",body))); continue
        if 'color:#c00000' in body: items.append(("N",len(re.sub("<[^>]+>"," ",body).split())))
        elif 'color:#1155cc' in body: items.append(("T",len(re.sub("<[^>]+>"," ",body).split())))
        elif body.startswith("<b>Play"):
            r=re.search(r'(\d+:\d+(?::\d+)?)-(\d+:\d+(?::\d+)?)',re.sub("<[^>]+>","",body))
            items.append(("C",sec(r.group(2))-sec(r.group(1)) if r else None, re.sub("<[^>]+>","",body)[:60]))
    print("==",path.split("/")[-1])
    nar=0;run=0;run_n=0;nb=0;sect="";problems=[]
    for it in items:
        if it[0]=="H":
            if nar: nb+=1; print(f"  narration break {nb}: {nar} words ~{nar/WPS:.0f}s" + ("  <-- LONG" if nar/WPS>65 else "")); nar=0
            if run: print(f"  clip run: {run}s ({run_n} clips)"+("  <-- >3min" if run>185 else "")); run=0; run_n=0
            sect=it[1]; print(" ["+sect+"]"); continue
        if it[0]=="N":
            if run: print(f"  clip run: {run}s ({run_n} clips)"+("  <-- >3min" if run>185 else "")); run=0; run_n=0
            nar+=it[1]
        elif it[0]=="C":
            if nar: nb+=1; print(f"  narration break {nb}: {nar} words ~{nar/WPS:.0f}s" + ("  <-- LONG" if nar/WPS>65 else "")); nar=0
            d=it[1]
            if d is None: print(f"  clip (no timestamp): {it[2]}"); run+=30; run_n+=1
            else:
                run+=d; run_n+=1
                if d>180: print(f"  single clip {d}s  <-- >3min: {it[2]}")
    if nar: nb+=1; print(f"  narration break {nb}: {nar} words ~{nar/WPS:.0f}s" + ("  <-- LONG" if nar/WPS>65 else ""))
    if run: print(f"  clip run: {run}s ({run_n} clips)"+("  <-- >3min" if run>185 else ""))
    N=sum(i[1] for i in items if i[0]=="N"); T=sum(i[1] for i in items if i[0]=="T")
    print(f"  TOTAL narration {N} words, transcription {T} words, script total {N+T}")
for p in sys.argv[1:]: check(p)
