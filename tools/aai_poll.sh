#!/bin/bash
declare -A IDS=( [911_pt1]=ae754b62-a0cd-4d47-b95d-17a995f46703 [911_pt2]=4059d210-4c12-425f-8ec5-9e5f518d9b20 [video_pt1]=b5924557-b1a9-47f6-be15-8c035944d01b [video_pt2]=fd0a2987-e80c-4424-96c0-07d15d6239bc [video_pt3]=37421e50-f8dc-409c-855e-280d813f7866 [video_pt4]=b1d67d95-888f-458b-ac83-959b8b5588f6 )
pending=1
while [ $pending -gt 0 ]; do
  pending=0
  for n in "${!IDS[@]}"; do
    [ -f transcripts/$n.txt ] && continue
    s=$(curl -sS -m 60 "https://api.assemblyai.com/v2/transcript/${IDS[$n]}")
    st=$(echo "$s" | python3 -I -c 'import sys,json;print(json.load(sys.stdin).get("status"))' 2>/dev/null)
    if [ "$st" = "completed" ]; then
      echo "$s" > transcripts/$n.json
      python3 -I - transcripts/$n.json transcripts/$n.txt <<'PY'
import sys,json
s=json.load(open(sys.argv[1]))
def ts(ms):
    x=ms//1000; return f"{x//3600}:{(x%3600)//60:02d}:{x%60:02d}"
with open(sys.argv[2],"w") as f:
    for u in s.get("utterances") or []:
        f.write(f"[{ts(u['start'])}-{ts(u['end'])}] {u['speaker']}: {u['text']}\n")
PY
      echo "$n completed: $(wc -l < transcripts/$n.txt) utterances, duration $(echo "$s" | python3 -I -c 'import sys,json;print(json.load(sys.stdin).get("audio_duration"))')"
    elif [ "$st" = "error" ]; then
      echo "$n ERROR: $(echo "$s" | head -c 300)"; echo "ERROR" > transcripts/$n.txt
    else
      pending=$((pending+1))
    fi
  done
  [ $pending -gt 0 ] && sleep 30
done
echo ALL DONE
