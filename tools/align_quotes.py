"""Find the caption timestamp of a quote: python3 -I align_quotes.py captions.txt 'quote one' 'quote two' ..."""
import sys,re,difflib
caps=[l for l in open(sys.argv[1]).read().splitlines() if l.startswith("[")]
norm=lambda s: re.sub(r"[^a-z0-9 ]"," ",s.lower())
norm=lambda s: re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",s.lower())).strip()
texts=[norm(re.sub(r"^\[[^\]]+\]\s*","",l)) for l in caps]
stamps=[re.match(r"\[([^\]]+)\]",l).group(1) for l in caps]
for q in sys.argv[2:]:
    qn=norm(q); best=(0,None)
    for i in range(len(texts)):
        win=" ".join(texts[i:i+6])
        r=difflib.SequenceMatcher(None,qn,win).find_longest_match(0,len(qn),0,len(win)).size
        if r>best[0]: best=(r,i)
    i=best[1]
    print(f"{stamps[i] if i is not None else '??'}  match={best[0]}/{len(qn)}  | {q[:70]}")
