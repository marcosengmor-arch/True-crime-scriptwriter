"""Builder for spec scripts whose clips come from public source videos (timestamps from captions or set at edit)."""
import html, re
RED="#c00000"; BLUE="#1155cc"; E=html.escape
class Doc:
    def __init__(s,title,subtitle,sources,note):
        s.o=[f"<html><body><h1>{E(title)}</h1>", f"<p>{E(subtitle)}</p>",
             f'<p><b>Narration is in <span style="color:{RED}">RED</span></b><br><b>Transcriptions are <i><span style="color:{BLUE}">BLUE</span></i></b></p>',
             "<p><b>Source footage</b></p>","<ul>"+"".join(f'<li><a href="{E(u)}">{E(n)}</a></li>' if u else f"<li>{E(n)}</li>" for n,u in sources)+"</ul>",
             f"<p>{E(note)}</p>"]
    def h(s,t): s.o.append(f"<h2>{E(t)}</h2>")
    def nar(s,t): s.o.append(f'<p><span style="color:{RED}">{E(t)}</span></p>')
    def ed(s,t): s.o.append(f"<p><b>@editor {E(t)}</b></p>")
    def clip(s,src,ts,scene="",kind="Play clip",url=""):
        tsx=f'<a href="{E(url)}">{E(ts)}</a>' if url else E(ts)
        sc=f" — {E(scene)}" if scene else ""
        s.o.append(f"<p><b>{E(kind)} {tsx} ({E(src)}){sc}</b></p>")
    def tr(s,lines): s.o.append(f'<p><span style="color:{BLUE}">'+"<br>".join(f"<i>{E(l)}</i>" for l in lines)+"</span></p>")
    def fuzz(s): s.o.append("<p>Small fuzz transition</p>")
    def notes(s,items): s.o.append("<h2>Writer's notes</h2><ul>"+"".join(f"<li>{E(i)}</li>" for i in items)+"</ul>")
    def html(s): return "\n".join(s.o)+"</body></html>"
    def md(s):
        h=s.html()
        h=re.sub(r'<span style="color:#c00000">(.*?)</span>',r'🔴 \1',h,flags=re.S)
        h=re.sub(r'<span style="color:#1155cc">(.*?)</span>',r'🔵 \1',h,flags=re.S)
        h=re.sub(r'<h1>(.*?)</h1>',r'# \1\n',h); h=re.sub(r'<h2>(.*?)</h2>',r'\n## \1\n',h)
        h=re.sub(r'<a href="([^"]+)">(.*?)</a>',r'[\2](\1)',h)
        h=re.sub(r'<b>(.*?)</b>',r'**\1**',h,flags=re.S); h=re.sub(r'<i>(.*?)</i>',r'*\1*',h,flags=re.S)
        h=h.replace("<br>","  \n").replace("<ul>","").replace("</ul>","").replace("<li>","- ").replace("</li>","\n")
        h=re.sub(r'<p>(.*?)</p>',r'\1\n',h,flags=re.S).replace("<html><body>","").replace("</body></html>","")
        return re.sub(r'\n{3,}','\n\n',html.unescape(h))
    def save(s,path):
        open(path+".html","w").write(s.html()); open(path+".md","w").write(s.md())
        hh=s.html(); wc=lambda L: sum(len(re.sub(r"<[^>]+>"," ",x).split()) for x in L)
        print(path.split("/")[-1], "narration:",wc(re.findall(r'<span style="color:#c00000">(.*?)</span>',hh,re.S)),"transcription:",wc(re.findall(r'<span style="color:#1155cc">(.*?)</span>',hh,re.S)),"clips:",hh.count("Play clip")+hh.count("Play audio"))
