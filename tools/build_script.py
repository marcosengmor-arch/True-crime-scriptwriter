import html, re
FILES = {
 "911A": ("911 Call #1 — Oct 10, 2019", "1xH7nVTkM3EjnyvIjwh8FTlS0Z44FJnxC"),
 "911B": ("911 Call #2 — Nov 25, 2019", "1rzVr_3SIxaMkJzQaoV2yamb0Ji8bm8Kq"),
 "PT1":  ("PT 1 MSP Interrogation (Dec 28, 2019, Camera 1)", "1QtV2qPnjRlot9iSnDN9Iy0Q2R5PbViW3"),
 "PT2":  ("PT 2 MSP Interrogation (Dec 28, 2019, Camera 2)", "1Mas7Ms53h2_Lc82l_JmgaLmmD_90jly7"),
 "PT3":  ("PT 3 MSP Interrogation (Dec 30, 2019, jail interview, second half)", "1I0Naoly8xAT0xhfdPm6TP9YbGdieQ2rL"),
 "PT4":  ("PT 4 MSP Interrogation (Dec 30, 2019, jail interview, first half)", "12DAgSRVcOp03TAS_A1si1DErYwGyxEOI"),
}
RED="#c00000"; BLUE="#1155cc"
def secs(ts):
    p=[int(x) for x in ts.split(":")]
    while len(p)<3: p.insert(0,0)
    return p[0]*3600+p[1]*60+p[2]
def link(fkey, start):
    return f"https://drive.google.com/file/d/{FILES[fkey][1]}/view?usp=sharing&t={secs(start)}"
out=[]
def H(t,lvl=2): out.append(f"<h{lvl}>{html.escape(t)}</h{lvl}>")
def nar(t): out.append(f'<p><span style="color:{RED}">{html.escape(t)}</span></p>')
def ed(t): out.append(f"<p><b>@editor {html.escape(t)}</b></p>")
def clip(kind, fkey, start, end, note=""):
    label=f"{kind} {start}-{end}"
    n=f" <b>{html.escape(note)}</b>" if note else ""
    out.append(f'<p><b>{html.escape(kind)} <a href="{link(fkey,start)}">{html.escape(start)}-{html.escape(end)}</a> ({html.escape(FILES[fkey][0].split(" (")[0].split(" —")[0])})</b>{n}</p>')
def tr(lines):
    body="<br>".join(f"<i>{html.escape(l)}</i>" for l in lines)
    out.append(f'<p><span style="color:{BLUE}">{body}</span></p>')
def plain(t): out.append(f"<p>{html.escape(t)}</p>")
def fuzz(): out.append("<p>Small fuzz transition</p>")

out.append("<html><body>")
out.append("<h1>Mark Latunski — RTC Trial Script</h1>")
plain("Trial section: intro hook & setup, first narration point, first clip section.")
out.append(f'<p><b>Narration is in <span style="color:{RED}">RED</span></b><br><b>Transcriptions are <i><span style="color:{BLUE}">BLUE</span></i></b></p>')
out.append("<p><b>Clip sources</b> (every timestamp link below opens the file at that second):</p><ul>")
for k,(name,fid) in FILES.items():
    out.append(f'<li><a href="https://drive.google.com/file/d/{fid}/view?usp=sharing">{html.escape(name)}</a></li>')
out.append("</ul>")
plain("Case files: Michigan State Police incident 035-0007899-19 (PT 1 Case Report, 12/28/2019).")

# ---------------- INTRO ----------------
H("INTRO")
ed("open on black, 911 audio before any picture. Then slow push-in on a dark rural road (Shiawassee County farmland b-roll). Everything marked [muted] gets muted.")
clip("Play audio","911A","0:00:01","0:00:04")
tr(["Dispatcher: Shiawassee 911, where is your emergency?"])
clip("Play audio","911A","0:00:04","0:00:33")
tr(["Caller 1: I met this guy at the bus station who offered me a ride, and I'm not even sure where I am… I broke out of this [muted] basement and I need a ride. I'm in trouble. I'm in trouble."])
clip("Play audio","911A","0:01:02","0:01:31")
tr(["Caller 1: I don't know whether he drugged me. I woke up in the [muted] basement, okay? Chained in a basement with a leather thing on arm and ankle, and I cut it with the butcher knife that I have in my [muted] hand."])
nar("October 2019. A man from New York is walking down a back road in Shiawassee County, Michigan, in the dark, carrying a butcher knife. He has no idea where he is. He only knows what he just got out of.")
fuzz()
nar("Six weeks later. Same county. Same stretch of road.")
clip("Play audio","911B","0:00:12","0:00:25")
tr(["Dispatcher: Shiawassee County 911.",
    "Caller 2: Hey, I want to get away from some creepy guy. He had me tied up in his basement.",
    "Dispatcher: I'm sorry, what's that?",
    "Caller 2: I'm trying to escape from some guy who had me chained up in his basement."])
clip("Play audio","911B","0:00:44","0:00:45")
tr(["Caller 2: I don't even have shoes on."])
clip("Play audio","911B","0:01:22","0:01:23")
tr(["Caller 2: He's after me."])
clip("Play audio","911B","0:01:33","0:01:39")
tr(["Caller 2: Help me."])
ed("caller 2 is barefoot, in a leather kilt, jumping fences between farmhouses. Hold on the dark road, let the audio do the work.")
nar("Both men got away. Both told police they did not want to press charges. And the man they were running from stayed exactly where he was: in a brick house on Tyrrell Road, with a room in the basement that was not finished yet.")
nar("On Christmas Eve, a third man walked into that room. He never made a phone call.")
fuzz()
clip("Play clip","PT1","0:00:00","0:00:06")
tr(["Latunski: …is Mark David Latunski. And that is not my legal name.",
    "Detective 1: Oh, it isn't?",
    "Latunski: No. That is a stolen identity."])
ed("same line is on Camera 2 (PT 2, 0:00:00-0:00:05) if you want the wide angle for this beat.")
clip("Play clip","PT1","1:12:48","1:12:58")
tr(["Detective 2: Who, I'm sorry, who's your hero?",
    "Latunski: I killed Kevin Bacon. Kevin Bacon is my hero."])
clip("Play clip","PT1","1:54:01","1:54:44")
tr(["Detective 1: With your demeanor, you're so calm. And I'm just wondering, is this really the only person that this has happened with?",
    "Latunski: You're completely wrong."])
ed("hard cut to black on \"completely wrong\". One second of silence, then title card.")

# ---------------- SET UP ----------------
H("SET UP")
nar("On Christmas morning 2019, 25-year-old Kevin Bacon did not come home to his family in Swartz Creek, Michigan. His car was found in a parking lot, his phone and clothes still inside it. In his messages, his family found a man who lived half an hour away, in rural Shiawassee County. The last messages were from Christmas Eve.")
ed("show the Michigan State Police report cover page (incident 035-0007899-19) and the line \"missing since 12/24/2019\".")
nar("Just after midnight on December 28th, five officers approached a brick house on Tyrrell Road. Two of them crept across a frozen field first, to watch the windows. Through an upstairs window: a blue light, black leather gear, a chrome chain. Then the others pulled into the driveway and knocked. The man who opened the door was wearing a kilt.")
ed("report page 2, highlight: \"I could see a blue light, black leather gear/equipment, and chrome colored chain through an east side upper window.\"")
clip("Play clip","PT1","0:20:24","0:20:33", note="(the detective, five hours later, describing that moment)")
tr(["Detective 1: There's a welfare check… you let the troopers go in and search your house, and they see a man… who is that man?"])
nar("He said he was home alone. He said he had never heard of anyone named Kevin Bacon. And when the trooper asked to come in and look around, he said:")
ed("pull the quote straight from the report, full screen, typewriter reveal: \"Yeah sure, come on in.\"")
nar("At the far end of the basement, Trooper Viviano found a sliding barn door. Behind it, a second door, bolted from the outside and warm to the touch. Behind that, a hidden room with chains on the walls. And inside it, the young man they had come looking for.")
ed("on \"warm to the touch\" slow zoom on the report text. Do NOT show any scene photos of the room. Cut back to black before the last sentence.")
nar("Mark Latunski was handcuffed in his own hallway. As the cuffs went on, he exhaled and said, \"You're making a mistake.\" Then he asked for a detective, so he could clear up the misunderstanding and go back inside his house.")
nar("At 5:56 that morning, two detective sergeants sat down with him at the Corunna state police post. Before anything else, they needed his name. That was the first problem.")

# ---------------- INTERVIEW START ----------------
H("INTERVIEW START")
clip("Play clip","PT1","0:00:00","0:01:17")
tr(["Latunski: …is Mark David Latunski. And that is not my legal name.",
    "Detective 1: Oh, it isn't?",
    "Latunski: No. That is a stolen identity. Mark David Latunski was last… or at least the last record that I have of Mark David Latunski was 1972. He was born in 1969. He has black hair, he has brown eyes… So, what happened to Mark David Latunski? I have no idea.",
    "Detective 2: Okay.",
    "Latunski: However, all of the people that I grew up with knew that I'm not Mark David Latunski, and they just failed to tell me."])
clip("Play clip","PT1","0:03:45","0:04:01")
tr(["Latunski: So, is my name Mark David Latunski? No. My name is Edgar Thomas Hill.",
    "Detective 1: So you're Edgar Thomas Hill."])
clip("Play clip","PT1","0:04:27","0:05:02")
tr(["Detective 1: Okay. What is the name that you prefer to be called?",
    "Latunski: …So the name that I go by is Olykos.",
    "Detective 1: How do you spell it?",
    "Latunski: O-L-Y-K-O-S."])
ed("4 seconds zoom on Latunski's face while he spells it.")
clip("Play clip","PT1","0:06:38","0:06:47")
tr(["Detective 1: And are you willing to give up these rights and answer my questions at this time?",
    "Latunski: I'm perfectly happy to talk, yes."])
nar("For the next fifteen minutes, the man calling himself Olykos explained that he was the last living member of a Norwegian clan, that bankers in New York were managing a trust fund in his name, and that his employer of twelve years had really been paying him his own money. None of it had anything to do with Kevin Bacon. The detectives let him talk. They had already read the messages between the two men. They knew where this was going. So did he.")
clip("Play clip","PT1","0:20:24","0:21:16")
tr(["Detective 1: There's a welfare check… you let the troopers go in and search your house, and they see a man… who is that man?",
    "Latunski: Well… when you talk to those, you know, on those sites, you can get any name.",
    "Detective 1: What sites did you meet him on?",
    "Latunski: Um, gosh… I think that one was Grindr."])
clip("Play clip","PT1","0:21:17","0:21:48", note="(cut before he drifts into the trust fund again)")
tr(["Latunski: But no matter. We chatted for a while. He described the things that he wanted. I did what I could to bring those things about, and after we sat and made an agreement about what was going to happen… he was supposed to disappear. Be gone."])
clip("Play clip","PT1","0:23:04","0:23:08")
tr(["Detective 1: So what was the agreement?",
    "Detective 2: In total?"])
ed("freeze on Latunski for 2 seconds before the narration.")
nar("What he said next, calmly, over the following two hours, is the reason this case made headlines around the world. It is also the reason this video has to be careful about what it shows you.")
ed("end of trial section.")

# ---------------- NOTES ----------------
H("Writer's notes (not for the edit)")
out.append("<ul>")
for t in [
 "Checked against the channel's writing guide: narration breaks of 20 to 59 seconds, no clip run over three minutes, intro built as a mystery hook (two 911 calls before the suspect is named), set up broken by a short clip so the viewer hears the detective before the interview starts.",
 "Hook logic: two men called 911 from the same road after getting out of Latunski's basement in the two months before Kevin Bacon died (Oct 10 and Nov 25, 2019). Neither pressed charges. Both calls are in the Trial Audio folder; Latunski is questioned about both men in the Dec 30 interview (PT 4 from 18:51, PT 3 from 8:03) and about the November runaway in the main interview (PT 1 from 2:06:08). Neighbor statements on the November incident are in the case report, supplemental 0003, pages 2-5.",
 "YouTube safety: no cause of death, no description of the body or the room beyond \"chains on the walls\", no mention of what happened after the death. 911 callers' swearing is marked [muted]. The detectives' reference to \"sex room\" in the report is not shown on screen.",
 "All timestamps come from my own transcription of the six files; every link opens the Drive file at that second. Interview time (5:56 AM) is from Camera 2.",
 "Clips already lined up for the next sections: \"I don't feel that I did anything wrong\" (PT 1, 1:09:58), \"Have you taken the life of anybody else?\" (PT 1, 1:57:44), the Nov 25 runaway in his words (PT 1, 2:06:08), \"Mark was killed with a stroke of a pen\" (PT 4, 6:31) and \"there is not a cache of bodies around somewhere\" (PT 3, 25:14).",
]:
    out.append(f"<li>{html.escape(t)}</li>")
out.append("</ul></body></html>")
htmltext="\n".join(out)
OUT="/home/user/true-crime-scriptwriter/latunski-trial/script/latunski_trial_script"
open(OUT+".html","w").write(htmltext)
def to_md(h):
    h=re.sub(r'<span style="color:#c00000">(.*?)</span>',r'🔴 \1',h,flags=re.S)
    h=re.sub(r'<span style="color:#1155cc">(.*?)</span>',r'🔵 \1',h,flags=re.S)
    h=re.sub(r'<h1>(.*?)</h1>',r'# \1\n',h); h=re.sub(r'<h2>(.*?)</h2>',r'\n## \1\n',h)
    h=re.sub(r'<a href="([^"]+)">(.*?)</a>',r'[\2](\1)',h)
    h=re.sub(r'<b>(.*?)</b>',r'**\1**',h,flags=re.S); h=re.sub(r'<i>(.*?)</i>',r'*\1*',h,flags=re.S)
    h=h.replace("<br>","  \n").replace("<ul>","").replace("</ul>","").replace("<li>","- ").replace("</li>","\n")
    h=re.sub(r'<p>(.*?)</p>',r'\1\n',h,flags=re.S).replace("<html><body>","").replace("</body></html>","")
    return re.sub(r'\n{3,}','\n\n',html.unescape(h))
open(OUT+".md","w").write("> Markdown copy for reading on GitHub. 🔴 = narration (red in the Doc), 🔵 = transcription (blue in the Doc). The formatted version is `latunski_trial_script.html` and the Google Doc linked in the README.\n\n"+to_md(htmltext))
# word count of script body (excluding notes and source list)
body=htmltext.split("<h2>INTRO</h2>")[1].split("<h2>Writer")[0]
text=re.sub(r"<[^>]+>"," ",body)
print("script words:", len(text.split()))
print("html bytes:", len(htmltext))
