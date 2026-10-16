"""Append the full timestamped transcripts (scripts/sources/*_full_transcript.html) to a script -> *_extended.html/.md"""
import re,html,sys
R="/home/user/true-crime-scriptwriter/scripts/"
HEAD='<h2>APPENDIX — FULL TRANSCRIPTS OF THE SOURCE FOOTAGE</h2><p>Complete transcripts of every source file used above, in order, with timestamps, for clip selection and fact-checking. Speaker attribution is given in the script section; the appendix is the raw record.</p>'
def build(name,parts):
    h=open(R+name+".html").read().replace("</body></html>","")
    app="\n".join(open(R+"sources/"+p).read() for p in parts)
    full=(h+HEAD+"\n"+app+"</body></html>").replace("&#x27;","'")
    open(R+name+"_extended.html","w").write(full)
    md=open(R+name+".md").read().rstrip()+"\n\n## APPENDIX — FULL TRANSCRIPTS OF THE SOURCE FOOTAGE\n\n"
    for p in parts:
        t=open(R+"sources/"+p).read()
        t=re.sub(r"<h2>(.*?)</h2>",r"\n### \1\n",t); t=re.sub(r"<p>(.*?)</p>",r"\1\n",t)
        md+=html.unescape(t)+"\n"
    open(R+name+"_extended.md","w").write(md)
    print(name+"_extended", len(full),"bytes", len(re.sub("<[^>]+>"," ",full).split()),"words")
build("jodi_arias_full_script",["arias_part1_full_transcript.html"])
build("dalia_dippolito_full_script",["dippolito_dalia_full_transcript.html","dippolito_michael_full_transcript.html"])
