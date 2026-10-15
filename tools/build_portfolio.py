"""Builds the portfolio documents (HTML for Google Docs import + Markdown copies)."""
import html, re, sys, json, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/true-crime-scriptwriter/portfolio"
LINKS = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
FILES = {
 "911A": ("911 Call #1", "1xH7nVTkM3EjnyvIjwh8FTlS0Z44FJnxC"),
 "911B": ("911 Call #2", "1rzVr_3SIxaMkJzQaoV2yamb0Ji8bm8Kq"),
 "PT1":  ("PT 1", "1QtV2qPnjRlot9iSnDN9Iy0Q2R5PbViW3"),
 "PT2":  ("PT 2", "1Mas7Ms53h2_Lc82l_JmgaLmmD_90jly7"),
 "PT3":  ("PT 3", "1I0Naoly8xAT0xhfdPm6TP9YbGdieQ2rL"),
 "PT4":  ("PT 4", "12DAgSRVcOp03TAS_A1si1DErYwGyxEOI"),
}
RED="#c00000"; BLUE="#1155cc"
def secs(ts):
    p=[int(x) for x in ts.split(":")]
    while len(p)<3: p.insert(0,0)
    return p[0]*3600+p[1]*60+p[2]
def link(fkey,start): return f"https://drive.google.com/file/d/{FILES[fkey][1]}/view?usp=sharing&t={secs(start)}"
E=html.escape

class Doc:
    def __init__(s,title): s.o=[f"<html><body><h1>{E(title)}</h1>"]; s.title=title
    def h(s,t,l=2): s.o.append(f"<h{l}>{E(t)}</h{l}>")
    def p(s,t): s.o.append(f"<p>{t}</p>")          # raw html allowed
    def pe(s,t): s.o.append(f"<p>{E(t)}</p>")
    def nar(s,t): s.o.append(f'<p><span style="color:{RED}">{E(t)}</span></p>')
    def ed(s,t): s.o.append(f"<p><b>@editor {E(t)}</b></p>")
    def clip(s,kind,f,a,b,note=""):
        n=f" <b>{E(note)}</b>" if note else ""
        s.o.append(f'<p><b>{E(kind)} <a href="{link(f,a)}">{E(a)}-{E(b)}</a> ({E(FILES[f][0])})</b>{n}</p>')
    def tr(s,lines): s.o.append(f'<p><span style="color:{BLUE}">'+"<br>".join(f"<i>{E(l)}</i>" for l in lines)+"</span></p>")
    def fuzz(s): s.o.append("<p>Small fuzz transition</p>")
    def ul(s,items): s.o.append("<ul>"+"".join(f"<li>{i}</li>" for i in items)+"</ul>")
    def ule(s,items): s.ul([E(i) for i in items])
    def table(s,head,rows):
        t='<table border="1" cellpadding="4"><tr>'+"".join(f"<th>{E(h)}</th>" for h in head)+"</tr>"
        for r in rows: t+="<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>"
        s.o.append(t+"</table>")
    def html(s): return "\n".join(s.o)+"</body></html>"
    def md(s):
        h=s.html()
        h=re.sub(r'<span style="color:#c00000">(.*?)</span>',r'🔴 \1',h,flags=re.S)
        h=re.sub(r'<span style="color:#1155cc">(.*?)</span>',r'🔵 \1',h,flags=re.S)
        h=re.sub(r'<h1>(.*?)</h1>',r'# \1\n',h); h=re.sub(r'<h2>(.*?)</h2>',r'\n## \1\n',h); h=re.sub(r'<h3>(.*?)</h3>',r'\n### \1\n',h)
        h=re.sub(r'<a href="([^"]+)">(.*?)</a>',r'[\2](\1)',h)
        h=re.sub(r'<b>(.*?)</b>',r'**\1**',h,flags=re.S); h=re.sub(r'<i>(.*?)</i>',r'*\1*',h,flags=re.S)
        h=re.sub(r'<table[^>]*>',"\n",h).replace("</table>","\n")
        h=re.sub(r'<tr>(.*?)</tr>',lambda m:"| "+" | ".join(re.findall(r'<t[hd]>(.*?)</t[hd]>',m.group(1),re.S))+" |\n"+("|---"*len(re.findall(r'<th>',m.group(1)))+"|\n" if "<th>" in m.group(1) else ""),h,flags=re.S)
        h=h.replace("<br>","  \n").replace("<ul>","").replace("</ul>","").replace("<li>","- ").replace("</li>","\n")
        h=re.sub(r'<p>(.*?)</p>',r'\1\n',h,flags=re.S)
        h=h.replace("<html><body>","").replace("</body></html>","")
        return re.sub(r'\n{3,}','\n\n',html.unescape(h))
    def save(s,name):
        open(f"{OUT}/{name}.html","w").write(s.html()); open(f"{OUT}/{name}.md","w").write(s.md())
        txt=re.sub(r"<[^>]+>"," ",s.html()); print(name, "words:", len(txt.split()))

# =====================================================================
# DOC 1 — FULL EPISODE SCRIPT
# =====================================================================
d=Doc("Mark Latunski — Full Episode Script (spec)")
d.pe("Spec script in the Red Tree Crime format, written from the released Michigan State Police interrogation footage, the two 911 recordings and the MSP case report (incident 035-0007899-19). Every clip link opens the Drive file at that second.")
d.p(f'<b>Narration is in <span style="color:{RED}">RED</span></b><br><b>Transcriptions are <i><span style="color:{BLUE}">BLUE</span></i></b>')
d.ul([f'<a href="https://drive.google.com/file/d/{fid}/view?usp=sharing">{E(n)}</a>' for n,fid in [
 ("911 Call #1 — Oct 10, 2019",FILES["911A"][1]),("911 Call #2 — Nov 25, 2019",FILES["911B"][1]),
 ("PT 1 — Dec 28, 2019 interview, camera 1 (3h19m)",FILES["PT1"][1]),("PT 2 — Dec 28, 2019 interview, camera 2",FILES["PT2"][1]),
 ("PT 4 — Dec 30, 2019 jail interview, first half",FILES["PT4"][1]),("PT 3 — Dec 30, 2019 jail interview, second half",FILES["PT3"][1])]])
d.h("INTRO")
d.ed("open on black, 911 audio before any picture. Then slow push-in on a dark rural road (Shiawassee County farmland b-roll). Everything marked [muted] gets muted.")
d.clip("Play audio","911A","0:00:01","0:00:04"); d.tr(["Dispatcher: Shiawassee 911, where is your emergency?"])
d.clip("Play audio","911A","0:00:04","0:00:33"); d.tr(["Caller 1: I met this guy at the bus station who offered me a ride, and I'm not even sure where I am… I broke out of this [muted] basement and I need a ride. I'm in trouble. I'm in trouble."])
d.clip("Play audio","911A","0:01:02","0:01:31"); d.tr(["Caller 1: I don't know whether he drugged me. I woke up in the [muted] basement, okay? Chained in a basement with a leather thing on arm and ankle, and I cut it with the butcher knife that I have in my [muted] hand."])
d.nar("October 2019. A man from New York is walking down a back road in Shiawassee County, Michigan, in the dark, carrying a butcher knife. He has no idea where he is. He only knows what he just got out of.")
d.fuzz(); d.nar("Six weeks later. Same county. Same stretch of road.")
d.clip("Play audio","911B","0:00:12","0:00:25"); d.tr(["Dispatcher: Shiawassee County 911.","Caller 2: Hey, I want to get away from some creepy guy. He had me tied up in his basement.","Dispatcher: I'm sorry, what's that?","Caller 2: I'm trying to escape from some guy who had me chained up in his basement."])
d.clip("Play audio","911B","0:00:44","0:00:45"); d.tr(["Caller 2: I don't even have shoes on."])
d.clip("Play audio","911B","0:01:22","0:01:23"); d.tr(["Caller 2: He's after me."])
d.clip("Play audio","911B","0:01:33","0:01:39"); d.tr(["Caller 2: Help me."])
d.ed("caller 2 is barefoot, in a leather kilt, jumping fences between farmhouses. Hold on the dark road, let the audio do the work.")
d.nar("Both men got away. Both told police they did not want to press charges. And the man they were running from stayed exactly where he was: in a brick house on Tyrrell Road, with a room in the basement that was not finished yet.")
d.nar("On Christmas Eve, a third man walked into that room. He never made a phone call.")
d.fuzz()
d.clip("Play clip","PT1","0:00:00","0:00:06"); d.tr(["Latunski: …is Mark David Latunski. And that is not my legal name.","Detective 1: Oh, it isn't?","Latunski: No. That is a stolen identity."])
d.clip("Play clip","PT1","1:12:48","1:12:58"); d.tr(["Detective 2: Who, I'm sorry, who's your hero?","Latunski: I killed Kevin Bacon. Kevin Bacon is my hero."])
d.clip("Play clip","PT1","1:54:01","1:54:44"); d.tr(["Detective 1: With your demeanor, you're so calm. And I'm just wondering, is this really the only person that this has happened with?","Latunski: You're completely wrong."])
d.ed("hard cut to black on \"completely wrong\". One second of silence, then title card.")
d.h("SET UP")
d.nar("On Christmas morning 2019, 25-year-old Kevin Bacon did not come home to his family in Swartz Creek, Michigan. His car was found in a parking lot, his phone and clothes still inside it. In his messages, his family found a man who lived half an hour away, in rural Shiawassee County. The last messages were from Christmas Eve.")
d.ed("show the MSP report cover page (incident 035-0007899-19) and the line \"missing since 12/24/2019\".")
d.nar("Just after midnight on December 28th, five officers approached a brick house on Tyrrell Road. Two of them crept across a frozen field first, to watch the windows. Through an upstairs window: a blue light, black leather gear, a chrome chain. Then the others pulled into the driveway and knocked. The man who opened the door was wearing a kilt.")
d.nar("He said he was home alone. He said he had never heard of anyone named Kevin Bacon. And when the trooper asked to come in and look around, he said:")
d.ed("pull the quote straight from the report, full screen, typewriter reveal: \"Yeah sure, come on in.\"")
d.nar("At the far end of the basement, Trooper Viviano found a sliding barn door. Behind it, a second door, bolted from the outside and warm to the touch. Behind that, a hidden room with chains on the walls. And inside it, the young man they had come looking for.")
d.ed("on \"warm to the touch\" slow zoom on the report text. Do NOT show any scene photos of the room.")
d.nar("Mark Latunski was handcuffed in his own hallway. As the cuffs went on, he exhaled and said, \"You're making a mistake.\" Then he asked for a detective, so he could clear up the misunderstanding and go back inside his house. At 5:56 that morning, two detective sergeants sat down with him at the Corunna state police post. Before anything else, they needed his name. That was the first problem.")
d.h("INTERVIEW START")
d.clip("Play clip","PT1","0:00:00","0:01:17"); d.tr(["Latunski: …is Mark David Latunski. And that is not my legal name.","Detective 1: Oh, it isn't?","Latunski: No. That is a stolen identity. Mark David Latunski was last… or at least the last record that I have of Mark David Latunski was 1972. He was born in 1969. He has black hair, he has brown eyes… So, what happened to Mark David Latunski? I have no idea.","Detective 2: Okay.","Latunski: However, all of the people that I grew up with knew that I'm not Mark David Latunski, and they just failed to tell me."])
d.clip("Play clip","PT1","0:03:45","0:04:01"); d.tr(["Latunski: So, is my name Mark David Latunski? No. My name is Edgar Thomas Hill.","Detective 1: So you're Edgar Thomas Hill."])
d.clip("Play clip","PT1","0:04:27","0:05:02"); d.tr(["Detective 1: Okay. What is the name that you prefer to be called?","Latunski: …So the name that I go by is Olykos.","Detective 1: How do you spell it?","Latunski: O-L-Y-K-O-S."])
d.clip("Play clip","PT1","0:06:38","0:06:47"); d.tr(["Detective 1: And are you willing to give up these rights and answer my questions at this time?","Latunski: I'm perfectly happy to talk, yes."])
d.nar("For the next fifteen minutes, the man calling himself Olykos explained that he was the last living member of a Norwegian clan, that bankers in New York were managing a trust fund in his name, and that his employer of twelve years had really been paying him his own money. None of it had anything to do with Kevin Bacon. The detectives let him talk. They had already read the messages between the two men. They knew where this was going. So did he.")
d.clip("Play clip","PT1","0:20:24","0:21:16"); d.tr(["Detective 1: There's a welfare check… you let the troopers go in and search your house, and they see a man… who is that man?","Latunski: Well… when you talk to those, you know, on those sites, you can get any name.","Detective 1: What sites did you meet him on?","Latunski: Um, gosh… I think that one was Grindr."])
d.clip("Play clip","PT1","0:21:17","0:21:48",note="(cut before the trust fund tangent)"); d.tr(["Latunski: But no matter. We chatted for a while. He described the things that he wanted. I did what I could to bring those things about, and after we sat and made an agreement about what was going to happen… he was supposed to disappear. Be gone."])
d.clip("Play clip","PT1","0:23:04","0:23:08"); d.tr(["Detective 1: So what was the agreement?","Detective 2: In total?"])
d.clip("Play clip","PT1","0:27:29","0:28:32"); d.tr(["Detective 1: So the man in the basement. When did he come to your house?","Latunski: I picked him up. We met, physically met, in Swartz Creek… I says, I will bring all of the things that you would need so that you can see them. I will lay them out in front of you. Then I'll step back. You need to decide, because I'm not going to force you.","Detective 1: On what day?","Latunski: Well, that would be the 24th. Christmas Eve. Yes, it was Christmas Eve."])
d.clip("Play clip","PT1","0:30:09","0:30:50"); d.tr(["Latunski: He says, can I text a friend and say, you know what, I'm just gonna be out… And he says, okay, now that I've said it, I'm going to turn my phone off."])
d.clip("Play clip","PT1","0:32:21","0:32:36"); d.tr(["Detective 1: You locked his vehicle?","Latunski: I locked his vehicle.","Detective 1: So his stuff is in his vehicle?","Latunski: His stuff was in his vehicle.","Detective 1: And then is he in the back of your van then?","Latunski: He stayed in the back of my van… And then I left the parking lot."])
d.nar("A locked car in a parking lot. A phone switched off. Clothes left behind. Everything Kevin's family had found three days later, Latunski was now describing as a plan. His plan, in his words, was an agreement: Kevin would go to the house, and afterwards Kevin would disappear. Then the detectives asked him what happened in the basement. He told them. In detail, for the better part of an hour, in the same flat voice he had used to talk about trust funds.")
d.ed("no clip here. Hold on a wide shot of the interview room, slow zoom, for the length of the narration. What he describes is not usable on this platform.")
d.clip("Play clip","PT1","0:39:37","0:40:09"); d.tr(["Detective 2: Where's the knife now?","Latunski: It is upstairs… because I cleaned it off. And it is upstairs in the dresser drawer. I think on the right-hand side, top."])
d.clip("Play clip","PT1","0:47:21","0:47:34"); d.tr(["Detective 1: Okay, so did it take place upstairs in your bedroom or downstairs where he is right now?","Latunski: It was all downstairs."])
d.nar("The knife was exactly where he said it would be. The lab would later find what appeared to be blood on it. By now the detectives had a confession, a location and a weapon. What they did not have was an explanation for the man in front of them. So they changed approach. They stopped asking what he did, and started asking how he felt about it.")
d.clip("Play clip","PT1","1:09:58","1:10:22"); d.tr(["Latunski: …I'm not going to wash this off. I— and even when I was talking to someone, I don't feel that I did anything wrong.","Detective 2: Did you tell anybody else about this other than us?"])
d.clip("Play clip","PT1","1:10:22","1:11:32"); d.tr(["Latunski: I did, because part of my culture is that if you have an honorable death, then you have to tell somebody before you pass three houses… I says, okay, let's say that the police have a problem with it. Then what? They throw me in jail, or they try to. I guess I'll just have to deal with that."])
d.clip("Play clip","PT1","1:12:33","1:12:58"); d.tr(["Latunski: He's a judge advocate in New York. And I sent him a text and I said, you know what, I did this. I says, and I love him. He's my hero.","Detective 2: Who, I'm sorry, who's your hero?","Latunski: I killed Kevin Bacon. Kevin Bacon is my hero."])
d.ed("freeze on \"Kevin Bacon is my hero\" for 2 seconds. Show the text message line from the report: \"I killed Kevin Bacon, Kevin Bacon is my hero.\"")
d.clip("Play clip","PT1","1:13:39","1:13:55",note="(cut before the nursing-home story)"); d.tr(["Latunski: And at that point I went, I'm done. You know what, I did it, I complied, and then I went to sleep and went off to Christmas."])
d.nar("He went to Christmas dinner. The next day he dropped his dog off at his husband's apartment and went to the gym. On the 27th, his husband drove him home and stayed five minutes. Nobody noticed anything. And through all of it, the text message was sitting on his phone, sent to a friend in New York before he had even left the house. Detective Sergeant Dirkse now did something that looks strange from the outside, and is one of the oldest tools in the room. He agreed with him.")
d.clip("Play clip","PT1","1:26:50","1:27:07"); d.tr(["Detective 2: And, you know, I want to commend you because not everybody could do this. And follow through on your word, with his wishes.","Latunski: Not everyone would commend me. I know that there are people who would look at it and say, hell no."])
d.clip("Play clip","PT1","1:36:54","1:37:02"); d.tr(["Detective 2: So has this ever happened before?","Latunski: No.","Detective 2: You've never assisted anybody with these type of wishes?","Latunski: No, I haven't."])
d.clip("Play clip","PT1","1:47:08","1:47:30"); d.tr(["Detective 1: Have you ever been requested in the past to do something that you did to Kevin, where they wanted to end their life? Have you ever assisted?","Latunski: No. There have been people who have hinted at it."])
d.nar("Three times they asked. Three times, no. Then Detective Sergeant Moore stopped being polite about it.")
d.clip("Play clip","PT1","1:54:01","1:55:57"); d.tr(["Detective 1: I have a feeling this probably wasn't the first person where you helped them end their life. And maybe I'm wrong… but with your demeanor, you're so calm. Is this really the only person that this has happened with?","Latunski: You're completely wrong. However, and I'm going to put a however in there. As we started the conversation, exactly where is Mark Latunski? …I remember going out into a field with a shovel, burying something, when I was this big. In the location that has now been converted into the cemetery that contains the cemetery plot for Mark Latunski."])
d.ed("let the silence after \"cemetery plot\" breathe. Cut to Detective 1's face.")
d.clip("Play clip","PT1","1:56:36","1:57:50"); d.tr(["Detective 1: At the property that you're at now, have you buried anything on the property?","Latunski: My dog is buried here… I have buried a horse. And actually, I didn't bury the horse.","Detective 1: Have you buried anything else? Because I'm going to have a cadaver dog go out and just do a property sweep.","Latunski: You can cover your bases. To my knowledge, there is absolutely nothing there buried.","Detective 1: Okay. Have you taken the life of anybody else?","Latunski: No."])
d.clip("Play clip","PT1","1:59:14","1:59:26"); d.tr(["Latunski: …so the cadaver dog will find that scent right there. If it doesn't, your cadaver dog is broken."])
d.nar("They brought the dog. It found nothing. But the detectives had one more name to put to him. Five weeks before Christmas, a young man in a leather kilt had run out of this same house screaming for help, and two state troopers had come to the door. The second 911 call you heard at the start of this video.")
d.clip("Play clip","PT1","2:06:08","2:06:45"); d.tr(["Detective 1: Back in November, the troopers came out because there was somebody who ran from your house. If that was a consensual act, at what point, or what caused him to flee? Which leads me to believe that Kevin isn't the only one."])
d.clip("Play clip","PT1","2:10:43","2:11:22"); d.tr(["Latunski: He had my $300 leather kilt and he's walking across the yard… He walked past that house. He walked past the next house. And then he books it two and a half, three houses down and decides to start climbing fences. I'm like, what?"])
d.clip("Play clip","PT1","2:11:24","2:11:50",note="(approximate, inside a longer answer)"); d.tr(["Latunski: …my personal opinion is that he found the nicest piece of leatherware, he shimmied into it, and he was going to walk with it."])
d.nar("A man running barefoot across frozen fields, climbing fences and screaming that he was about to be killed, was, in Latunski's telling, a man stealing a kilt. The detectives moved on. Two and a half hours in, they asked one last time.")
d.clip("Play clip","PT1","2:33:03","2:33:41"); d.tr(["Detective 1: You say there's nobody else that you've done this to, as far as where their life has ended down there?","Latunski: Nope.","Detective 2: Is that the truth? You've been truthful so far.","Latunski: It's the truth. I can't tell a lie for anything. I have never done anything. I've never done this."])
d.nar("After a break, Latunski signed a consent form for DNA swabs and photographs. He asked which name they wanted him to sign. Then, while a detective took samples from under his fingernails, he explained why he had not washed his hands.")
d.clip("Play clip","PT1","3:10:39","3:11:30"); d.tr(["Detective 2: Well, you said you did take a shower though.","Latunski: I took a light shower… obviously there's still stuff under my nails. But I very deliberately didn't want to wash them off.","Detective 1: You didn't want to wash them off?","Latunski: …I just look at it and I say, to wash someone off would be a sign of disrespect."])
d.clip("Play clip","PT1","2:53:00","2:53:18"); d.tr(["Latunski: And then am I going to be able to go back home and take care of the dog?","Detective 2: I don't know yet.","Latunski: Okay, great. I'm tired and I want to get some sleep, and today's a gym day."])
d.clip("Play clip","PT1","3:16:01","3:16:19"); d.tr(["Detective 1: Well, at this point, we are going to put you back in that cell there, and under the circumstances, you're going to be going to the jail tonight."])
d.h("TWO DAYS LATER")
d.nar("Latunski was arraigned on December 30th on open murder and mutilation charges, in front of a courtroom full of cameras. That afternoon, after he had spoken to his lawyers, a detective visited him in the jail interview room. By then Latunski knew he should not be talking. He talked anyway.")
d.clip("Play clip","PT4","0:00:36","0:00:57"); d.tr(["Latunski: I did talk with the attorneys that they have, and they said that I really shouldn't say anything.","Detective: Okay, that's your prerogative. I'm not gonna force you.","Latunski: You know what, it kind of goes against my nature to not talk."])
d.clip("Play clip","PT4","0:03:40","0:04:05"); d.tr(["Latunski: And you understand that my name is not Mark, right?","Detective: …the reason I was calling you Mark is because everything that I have in documentation is Mark.","Latunski: Everything that you have in documentation is wrong. My legal name is Edgar. Mark is a stolen identity. It's my nephew."])
d.clip("Play clip","PT4","0:06:31","0:07:05"); d.tr(["Detective: Do you remember back in 2013, September of 2013, you had talked with a trooper from the Lansing Post, claiming that Mark was killed with a stroke of a pen. Does that ring a bell?","Latunski: Yes."])
d.nar("Six years before Kevin Bacon, Latunski had called police to report that Mark Latunski was dead. Now the detective wanted to know whether that had been a figure of speech. And then he asked the question every detective in this case had been asking since the first hour.")
d.clip("Play clip","PT3","0:24:16","0:26:02"); d.tr(["Detective: My concern is, and I think a normal person would have this concern, is that this wasn't the first time… I want to make sure that there's no other victims out there.","Latunski: And that is the same question that the other chap, the detective, he said: you're too calm and collected. My nature is calm and collected. I will tell you, and it is absolutely definitive, I have never done this. There is not a cache of bodies around somewhere, if that's what you're asking for.","Detective: Is there one other body, one other person?","Latunski: No, not at all."])
d.h("OUTRO")
d.nar("The cadaver dog found nothing on the property. The two men who had called 911 in October and November were never charged with anything, and neither was Latunski for what happened to them. In September 2022 he pleaded guilty to open murder and to mutilation of a body, with no deal from prosecutors. A judge then had to decide whether the killing was premeditated. In October he ruled that it was, calling it a cold calculation, and on December 15th, 2022, Mark Latunski was sentenced to life in prison without the possibility of parole.")
d.nar("Kevin Bacon was 25. He was a hairstylist and a student, and the people who loved him describe him as the person who made everyone else feel welcome. He went to meet a stranger on Christmas Eve and trusted him. That trust is the whole case.")
d.ed("end on a photo of Kevin provided by the family, if the channel has clearance. Otherwise hold on black.")
d.h("Writer's notes")
d.ule(["Narration is about 1,100 words; transcription about 1,800. Narration breaks stay under 60 seconds and no clip run exceeds three minutes.",
 "YouTube safety: the killing, the body and everything Latunski did afterwards are handled in one narration line (\"What he describes is not usable on this platform\"). No clip in the script contains a description of a wound, a body or the mutilation.",
 "Every timestamp comes from my own transcription of the six files. Two clips are cut inside a longer answer and marked approximate.",
 "Plea and sentence confirmed against AP/WXYZ (Dec 15, 2022) and ABC12 (Sept 2022 plea)."])
d.save("latunski_full_script")

# =====================================================================
# DOC 2 — RESEARCH DOSSIER + CLIP BANK
# =====================================================================
d=Doc("Mark Latunski — Research Dossier & Clip Bank")
d.pe("Working file behind the Latunski scripts. Sources: MSP case report 035-0007899-19 (13 pages, printed 12/1/2022), the two 911 recordings, 4h15m of interview footage (transcribed with timestamps), and press coverage of the plea and sentencing. Anything not in those sources is marked.")
d.h("Timeline")
d.table(["When","What","Source"],[
 ["1996–2007","Latunski works as a bench chemist at Flint Ink.","Interview PT 1, 0:09:52"],
 ["2007–Feb 2019","Quality manager at American Chemical Technologies, Fowlerville. Loses the job in early 2019 (husband says February, for erratic behavior; a neighbor says April).","Report supp. 0003/0012; PT 1, 0:11:25"],
 ["Sept 2013","Tells a Lansing Post trooper that \"Mark was killed with a stroke of a pen\".","PT 4, 0:06:31"],
 ["Sept 25, 2019","Husband moves out of the Tyrrell Road house, afraid of him. The basement room is finished after he leaves.","Report supp. 0012"],
 ["Oct 10, 2019","911 call #1: a man from New York, lost on a back road at night with a butcher knife, says he woke up chained in a basement and cut himself free. Asks police not to make a report. Latunski later says the man stayed with him a week and they are still friends.","911 audio #1; PT 3, 0:08:03"],
 ["Nov 25, 2019, 4:48 pm","911 call #2: a barefoot man in a leather kilt runs between neighbors' houses screaming \"He is going to kill me\". Latunski follows in his SUV. The man declines to press charges. MSP report 35-7199-19.","911 audio #2; report supp. 0003 pp. 4–5"],
 ["Dec 21, 2019, ~10:30 pm","A neighbor hears an explosion and sees a large fire in Latunski's back yard burning for about three hours.","Report supp. 0003 p. 3"],
 ["Dec 24, 2019, near dusk","Kevin Bacon, 25, meets Latunski in a parking lot on Miller Road, Swartz Creek, after chatting on Grindr. His car is locked with his phone and clothes inside. Killed in the basement room that night.","PT 1, 0:27:29–0:32:36; report OIC supp."],
 ["Dec 25, 2019","Kevin reported missing (Genesee County). Latunski attends Christmas dinner at his husband's apartment.","Report; PT 1, 1:13:39"],
 ["Dec 26–27","Latunski drops off the dog, goes to the gym; husband drives him home on the 27th at ~10:30 pm and stays five minutes.","Report supp. 0012"],
 ["Dec 27, 10:31 pm","Clayton Twp PD asks MSP for help checking Latunski's address: Kevin's family found messages between the two.","Report p. 1"],
 ["Dec 28, 12:41 am","Five officers approach the house. Sgt Berdan and Tpr Salski watch from the field; Tpr Viviano, Ofc Lee and Ofc Wurtz knock. Latunski, in a kilt: \"Umm no. I don't know who that is\" / \"Yeah sure, come on in.\"","Report pp. 1–2, supp. 0007"],
 ["Dec 28, ~12:55 am","Viviano finds the hidden room behind a barn door and a bolted inner door. \"Oh my God. Lock him up.\" Latunski: \"You're making a mistake.\"","Report supp. 0005/0007"],
 ["Dec 28, 1:21 am","Time of death declared by Dr. Kluger (Owosso Memorial).","Report supp. 0007"],
 ["Dec 28, 5:56 am","Interview begins at the Corunna detachment with D/Sgt Moore and D/Sgt Dirkse. Miranda signed as \"Wilk Olykos Vilks\".","PT 1/PT 2"],
 ["Dec 28, 8:55 am","Consent for DNA, fingernail swabs, photographs and vehicle search.","PT 1, 3:05:23"],
 ["Dec 28, ~9:20 am","Lodged at Shiawassee County Jail on open murder.","Report supp. 0005"],
 ["Dec 28","Neighbor canvass; Hyundai Santa Fe impounded; lab seizes bedding, knife from dresser drawer, swabs; cadaver K9 sweep of the property: nil results.","Report supp. 0002/0003/0004, OIC supp."],
 ["Dec 29","Husband interviewed. Jail re-contact for the phone passcode; Latunski refuses.","Report supp. 0012, OIC supp."],
 ["Dec 30","Search warrant for the iPhone; mason jars seized from the house; two-count arrest warrant (open murder, disinterment and mutilation); arraignment with heavy media. Afternoon jail interview (PT 4 + PT 3).","OIC supp.; PT 4/PT 3"],
 ["Sept 2022","Pleads guilty to open murder and mutilation, no plea deal.","ABC12"],
 ["Oct 20, 2022","Judge Matthew Stewart finds first-degree premeditated murder (\"cold calculation\").","AP/WXYZ"],
 ["Dec 15, 2022","Sentenced to life without parole; 11 months concurrent on the mutilation count.","AP/WXYZ, WISTV"],
])
d.h("People")
d.table(["Name","Role","Notes"],[
 ["Kevin Bacon","Victim, 25, Swartz Creek","Hairstylist and student (press). Met Latunski on Grindr. Reported missing Christmas Day."],
 ["Mark David Latunski","Suspect, Bennington Twp, Shiawassee County","Also calls himself Edgar Thomas Hill, Olykos, Wilk/Willi Olykos Vilks. Chemist, four children, divorced; married a man in Florida who moved out Sept 2019."],
 ["Tpr Robert Viviano","MSP Flint Post","Had prior rapport (arrested Latunski on a Friend of Court warrant). Got consent to search; found the room."],
 ["Sgt Terry Berdan","MSP patrol sergeant","Planned the approach; watched through the windows; author of the original report."],
 ["Tpr Nicholas Salski","MSP","Cuffed Latunski; transported him; found a ring under the seat."],
 ["Ofc Rich Lee, Ofc Rod Wurtz","Clayton Twp PD","Missing-person investigators who brought the case to MSP."],
 ["D/Sgt James Moore","MSP, officer in charge","Lead interviewer (Detective 1 in the scripts). Search warrants, OIC supplemental."],
 ["D/Sgt Joshua Dirkse","MSP","Second interviewer (Detective 2). Took DNA and photos. Read the chat logs before the interview."],
 ["D/Sgt Tom Dhooghe, Tprs Hartman, Pritchett, Littleton, Donahue","MSP","Scene search and neighbor canvass."],
 ["Sgt Yount","MSP cadaver K9","Property sweep, nil results."],
 ["APA Adam Masserang; Magistrate Dale DeGarmo","Prosecution / court","Warrants Dec 28–30."],
 ["Judge Matthew Stewart","Shiawassee County Circuit Court","First-degree finding and sentence (2022)."],
])
d.h("Facts that carry the story")
d.ule([
 "Two 911 escapes from the same house in the two months before the murder; neither man pressed charges. This is the hook and it is fully documented.",
 "Consent search. Latunski denied knowing Kevin, then invited the officers in. The room was behind two doors; the inner one was warm.",
 "He asked for a detective himself, to \"clear up the misunderstanding\".",
 "The first ten minutes of the interview are about his name, not the crime.",
 "He texted a friend in New York before leaving the house: \"I killed Kevin Bacon, Kevin Bacon is my hero.\"",
 "He went to Christmas dinner, the gym, and had his husband over for five minutes, without anyone noticing anything.",
 "Asked if there were other victims, he answered \"you're completely wrong\" and then told a story about burying something in a field as a child, in what is now the cemetery with Mark Latunski's plot.",
 "He explained the November runaway as a man stealing a $300 kilt.",
 "He deliberately did not wash: \"to wash someone off would be a sign of disrespect.\"",
 "On Dec 30, after his lawyers told him not to talk, he talked, and denied \"a cache of bodies\".",
])
d.h("Clip bank")
d.pe("Best moments across the six files. Category: D = denial/evasion, B = bizarre, A = admission, T = detective tactic, E = emotion, X = too graphic for YouTube (narration only).")
rows=[
 ("911A","0:00:04","0:00:33","E","\"I broke out of this basement… I'm in trouble.\"","yes"),
 ("911A","0:01:02","0:01:31","E","Woke up chained, cut the strap with a butcher knife.","yes (mute swearing)"),
 ("911A","0:04:30","0:04:58","D","\"Please don't make an incident out of this. I beg you.\"","yes"),
 ("911A","0:05:11","0:05:36","D","\"If you go with somebody under your own free will, it's not kidnapping.\"","yes"),
 ("911B","0:00:12","0:00:25","E","\"He had me chained up in his basement.\"","yes"),
 ("911B","0:01:22","0:01:39","E","\"He's after me.\" / \"Help me.\"","yes"),
 ("PT1","0:00:00","0:01:17","B","\"That is not my legal name. That is a stolen identity.\"","yes"),
 ("PT1","0:03:45","0:04:01","B","\"My name is Edgar Thomas Hill.\"","yes"),
 ("PT1","0:04:27","0:05:02","B","\"The name that I go by is Olykos.\" Spells it.","yes"),
 ("PT1","0:07:11","0:08:03","B","Signs the Miranda form: \"what name do you want?\" / \"Wilk Olykos Vilks\".","yes"),
 ("PT1","0:15:34","0:15:56","B","Rates: $200 an hour, $1,500 a day, \"honest money\".","borderline"),
 ("PT1","0:20:24","0:21:16","A","\"Who is that man?\" / \"I think that one was Grindr.\"","yes"),
 ("PT1","0:21:17","0:23:04","A","\"We made the agreement and he was supposed to disappear, be gone.\"","yes (cut at 0:21:48)"),
 ("PT1","0:27:29","0:28:32","A","Met in Swartz Creek on Christmas Eve; \"I'm not going to force you.\"","yes"),
 ("PT1","0:30:09","0:30:50","A","Kevin texts a friend, turns his phone off.","yes"),
 ("PT1","0:32:21","0:32:36","A","Locked Kevin's car with his things inside.","yes"),
 ("PT1","0:36:21","0:39:37","X","Describes the killing.","no"),
 ("PT1","0:39:37","0:41:36","A","Knife in the dresser drawer; description of the knife.","yes (first 30 s)"),
 ("PT1","0:57:19","0:57:35","A","\"Did you do this by yourself?\" / \"I did it all by myself.\"","yes"),
 ("PT1","0:57:52","1:05:40","X","What he did after the death; dehydrator.","no"),
 ("PT1","1:08:36","1:09:16","B","Never washed the sheets; \"I'm not gonna wash him off.\"","borderline"),
 ("PT1","1:09:58","1:10:19","D","\"I don't feel that I did anything wrong.\"","yes"),
 ("PT1","1:10:22","1:11:32","B","\"Honorable death… tell somebody before you pass three houses.\"","yes"),
 ("PT1","1:12:33","1:12:58","A","\"I killed Kevin Bacon. Kevin Bacon is my hero.\"","yes"),
 ("PT1","1:13:39","1:13:55","B","\"I complied, and then I went to sleep and went off to Christmas.\"","yes"),
 ("PT1","1:23:18","1:23:29","T","Detective: \"I play that with my dog. I'm the alpha dog in this house.\" (rapport)","yes"),
 ("PT1","1:26:50","1:27:07","T","Detective: \"I want to commend you… follow through on your word.\"","yes"),
 ("PT1","1:36:54","1:37:02","D","\"Has this ever happened before?\" / \"No.\"","yes"),
 ("PT1","1:47:08","1:47:30","D","\"There have been people who have hinted at it.\"","yes"),
 ("PT1","1:54:01","1:55:57","T/B","\"You're so calm… is this really the only person?\" / \"You're completely wrong. However… where is Mark Latunski?\" Field, shovel, cemetery plot.","yes"),
 ("PT1","1:56:36","1:57:50","T","Cadaver dog warning; dog and horse buried; \"absolutely nothing there buried.\"","yes"),
 ("PT1","1:59:14","1:59:26","B","\"If it doesn't, your cadaver dog is broken.\"","yes"),
 ("PT1","2:06:08","2:06:45","T","Detective brings up the November runaway: \"leads me to believe Kevin isn't the only one.\"","yes"),
 ("PT1","2:10:43","2:12:12","D","The $300 kilt explanation.","yes"),
 ("PT1","2:18:12","2:18:17","E","\"You've been in here a long time.\" / \"I know, I am tired of this.\"","yes"),
 ("PT1","2:33:03","2:33:41","D","\"I can't tell a lie for anything. I've never done this.\"","yes"),
 ("PT1","2:52:58","2:53:29","B","\"Am I going to be able to go back home and take care of the dog?… today's a gym day.\"","yes"),
 ("PT1","3:05:23","3:05:48","A","Signs consent, says the date and time himself: Dec 28, 8:55 AM.","yes"),
 ("PT1","3:06:01","3:06:58","B","Social Security number \"is for someone who isn't me.\"","yes"),
 ("PT1","3:10:39","3:11:30","B","\"To wash someone off would be a sign of disrespect.\"","yes"),
 ("PT1","3:14:20","3:14:51","E","\"That red mark is from the handcuffs… in the back of the car for three hours.\"","yes"),
 ("PT1","3:16:01","3:16:19","T","\"You're going to be going to the jail tonight.\"","yes"),
 ("PT2","0:00:00","0:00:46","B","Camera 2 angle of the \"stolen identity\" opening.","yes"),
 ("PT4","0:00:36","0:00:57","B","\"They said I really shouldn't say anything… it goes against my nature to not talk.\"","yes"),
 ("PT4","0:01:52","0:02:44","B","Won't eat the jail food: pudding \"turned the roof of my mouth numb\".","yes"),
 ("PT4","0:03:40","0:04:13","B","\"My legal name is Edgar. Mark is a stolen identity. It's my nephew.\"","yes"),
 ("PT4","0:06:31","0:07:17","T/B","2013: \"Mark was killed with a stroke of a pen\"; the 911 call back then.","yes"),
 ("PT4","0:12:34","0:13:17","B","\"Was that literal or figurative?\" / \"Mark is gone, don't know where he is.\"","yes"),
 ("PT4","0:18:51","0:20:06","T","Detective turns to the Nov 25 incident.","yes"),
 ("PT3","0:08:03","0:08:24","T","October: the man from New York. \"We're good friends. To this day.\"","yes"),
 ("PT3","0:14:34","0:15:08","T","\"Why would he be running from your house in a kilt with a knife, scared to death?\" / \"Um, no.\"","yes"),
 ("PT3","0:24:16","0:26:02","T/D","\"No other victims?\" / \"There is not a cache of bodies around somewhere.\"","yes"),
 ("PT3","0:28:12","0:30:28","B","Detective: \"What does it have to do with Kevin?\" / I-69 and tulips.","yes"),
]
d.table(["File","Start","End","Cat.","Moment","YouTube safe?"],[[E(f),f'<a href="{link(f,a)}">{a}</a>',b,c,E(m),s] for f,a,b,c,m,s in rows])
d.h("Five alternative cold opens")
d.ule([
 "The two 911 calls (used in the script): two escapes, no charges, then a third man who never called.",
 "The name: open on \"That is not my legal name. That is a stolen identity,\" then the detective on Dec 30 asking about \"Mark was killed with a stroke of a pen\" in 2013. Who is the man in the chair?",
 "The door: build entirely from the report. Blue light in the window, a man in a kilt, \"I don't know who that is,\" \"Yeah sure, come on in,\" a door warm to the touch. Cut to the interview only at the title card.",
 "The text message: open on \"I killed Kevin Bacon. Kevin Bacon is my hero,\" then rewind to Christmas dinner, the gym, the five-minute visit from his husband. Nobody noticed anything.",
 "The question: cut together every time a detective asks \"is this the only one?\" across both interviews (1:36:54, 1:47:08, 1:54:01, 1:57:44, 2:33:03, PT3 0:25:57), ending on \"your cadaver dog is broken.\"",
])
d.h("Not used, and why")
d.ule([
 "The description of the killing and everything after it (PT 1, 0:36–1:06 and 2:20–2:42): not usable on YouTube in any wording. Handled with one narration line.",
 "The trust fund, I-69, Norwegian clan and \"Thomas of Wales\" monologues (roughly 40 minutes in total): one narration summary. A single clip of it would need subtitles and would stall the video.",
 "Names of the two 911 callers, the husband and the neighbors: redacted in the report and not needed.",
 "The chat logs between Kevin and Latunski: summarized in the report as too graphic to quote; referenced only as \"the messages\".",
])
d.save("latunski_research_dossier")

# =====================================================================
# DOC 3 — INTERROGATION BREAKDOWN
# =====================================================================
d=Doc("How Two Detectives Got Three Hours Out of Mark Latunski — Interrogation Breakdown")
d.pe("An analysis of the December 28 and December 30, 2019 Michigan State Police interviews of Mark Latunski, written for interrogation-format scripting. Timestamps refer to the released footage (PT 1 = Dec 28 camera 1; PT 4 and PT 3 = Dec 30, first and second half).")
d.h("The starting position")
d.pe("The detectives walked in with more than most interviewers ever get: a body found by consent search, a suspect who had asked to speak to a detective, and chat logs between the suspect and the victim that D/Sgt Dirkse had already read. The risk was not getting a confession. The risk was getting a confession that was unusable, from a man who, within the first minute, said his name was a stolen identity. Everything they did over the next three hours was about keeping him talking while making the record hold up.")
d.h("Phase 1 — Let the name go (0:00–0:08)")
d.pe("Latunski opens by denying that he is Mark Latunski. D/Sgt Moore does not argue. He asks what name Latunski prefers, how to spell it, and lets him sign the Miranda form as \"Wilk Olykos Vilks\" with date of birth \"unknown\" (PT 1, 0:07:11–0:08:03). Arguing about identity would have cost the interview before it started. Writing the signature down as given, with the time on it, kept the waiver clean and gave the court a man who understood every question he was asked.")
d.h("Phase 2 — Fifteen minutes of nothing (0:08–0:20)")
d.pe("Trust funds, New York bankers, Flint Ink, Norwegian coming-of-age, the Thomas of Wales clan. Moore asks only short, factual follow-ups (\"what did you do for Flint Ink?\", \"how long did you work there?\"). This is the rapport phase, and it also quietly builds the biography the prosecutor will need: twelve years as a quality manager, a job lost in early 2019, paid companionship since April. He is calm, articulate and oriented. That matters later.")
d.h("Phase 3 — The pivot question (0:20:24)")
d.pe("Moore ties the ramble back to the reason they are there in one sentence: \"you let the troopers go in and search your house and they see a man… who is that man?\" Latunski answers with Grindr, then with the word \"agreement\". From here the detectives mostly ask \"so what was the agreement?\" and \"what did you do?\" and let him fill the silence. The full description of the killing comes without a single confrontation (0:36–0:40). The knife's location follows immediately (0:39:37) and is confirmed by the search team the same day.")
d.h("Phase 4 — Lock the physical record (0:47–1:00)")
d.pe("Once the narrative is on tape, they go back over it for the details that evidence can check: where in the house (\"it was all downstairs\"), position on the floor, the sketch of the room (0:55:13), whether anyone helped (\"I did it all by myself\", 0:57:19), which night (\"the 24th into the 25th\", 0:59:36). None of this is for the viewer. All of it is for the case file. For a script, this section is where the clips get short and the narration carries the weight.")
d.h("Phase 5 — Agree with him (1:00–1:30)")
d.pe("Dirkse: \"that shows me the type of person you are\" (1:00:13), \"you're a man of your word\" (1:00:20), \"I want to commend you because not everybody could do this\" (1:26:50), \"we're open to a lot of things\" (2:42:10). Moore on the pack dynamics: \"I play that with my dog. I'm the alpha dog in this house\" (1:23:18). This is minimization and affirmation. It looks grotesque in isolation and it is the reason the text message (\"I killed Kevin Bacon, Kevin Bacon is my hero\", 1:12:48), the Christmas dinner (1:13:39) and the admission that he did not wash (1:08:36) all come out unprompted. The viewer needs the narration to say what the detectives are doing, or the detectives look complicit.")
d.h("Phase 6 — Other victims, three ways (1:36–2:34)")
d.ule([
 "Soft, from Dirkse: \"has this ever happened before?\" (1:36:54). No.",
 "Broader, from Moore: \"have you ever been requested in the past… have you ever assisted?\" (1:47:08). \"There have been people who have hinted at it.\"",
 "Direct, with the demeanor read: \"with your demeanor, you're so calm… is this really the only person?\" (1:54:01). \"You're completely wrong. However…\" and the story about a field, a shovel and the cemetery plot of Mark Latunski.",
 "Leverage: \"I'm going to have a cadaver dog go out\" (1:57:26). He volunteers the dog, the horse and the bucket of sand on the hyacinths (1:58:19), then: \"if it doesn't, your cadaver dog is broken.\"",
 "Evidence: the November runaway (2:06:08), framed as \"if that was consensual, what caused him to flee?\" He answers with the kilt.",
 "Final, moral: \"is that the truth? You've been truthful so far\" (2:33:11). \"I can't tell a lie for anything.\"",
])
d.pe("Six asks, each with a different footing. None produced a second victim, and the K9 sweep came back nil. But the sequence is the spine of the episode, because it is the only place where the detectives and the viewer want the same thing.")
d.h("Phase 7 — Consent, samples, photographs (2:59–3:16)")
d.pe("After the break, Dirkse reads the consent form line by line and has Latunski initial each part and write the date and time himself (3:05:23). Fingernail swabs are taken on camera while Latunski explains that he deliberately did not wash (3:10:39). The photographs show no injuries, which closes off any later self-defense claim. Then Moore tells him plainly that he is going to jail tonight (3:16:01). No bargaining, no promise.")
d.h("Phase 8 — The second interview (Dec 30)")
d.pe("Two days later, after arraignment and after his lawyers told him not to talk, a detective re-Mirandizes him in the jail interview room (PT 4, 0:03:11–0:06:25) and gets a yes. The questions are narrow: the 2013 \"stroke of a pen\" call, the November runaway, the man from New York in October, and once more, \"no other victims?\" (PT 3, 0:24:16). Each answer is on tape, with counsel's advice acknowledged by the suspect on camera (PT 4, 0:00:36). This is the cleanest piece of the whole file.")
d.h("What this means for the script")
d.ule([
 "The interview has a natural three-act shape: name (0:00–0:20), confession (0:20–1:00), other victims (1:36–2:34). The Dec 30 interview is the epilogue.",
 "The graphic middle (0:36–1:06, 2:20–2:42) must be carried by narration. The detectives' questions in those stretches are also unusable because they repeat the detail.",
 "The affirmation tactics need one narration line of context each time they appear, or the audience turns on the detectives.",
 "The \"is this the only one?\" sequence should be cut as a ladder, in order, with the cadaver dog as the rung the audience remembers.",
])
d.save("latunski_interrogation_breakdown")

# =====================================================================
# DOC 4 — YOUTUBE-SAFE STYLE GUIDE
# =====================================================================
d=Doc("YouTube-Safe Writing for Interrogation Channels — Working Guide")
d.pe("My working rules for scripting police-interrogation and bodycam videos that keep monetization, keep the audience, and keep the victim's dignity. Examples come from the Mark Latunski case (Michigan State Police, 2019).")
d.h("Three principles")
d.ul([
 "<b>Say what happened, not how it looked.</b> The audience needs the fact (a stabbing, a shooting, a strangulation) to follow the case. They do not need the wound. \"Blunt force trauma\", \"a gunshot wound to the chest\", \"the cause of death was asphyxiation\" are complete sentences.",
 "<b>Let the suspect be strange, not the writer.</b> The suspect's calm, his vocabulary, his flat affect, his small talk about the gym: those are the horror. A narrator who reaches for adjectives competes with the footage and loses.",
 "<b>Tell the viewer what you are not telling them.</b> \"What he described next is why this video has to be careful about what it shows you\" is both compliant and the strongest line of suspense available. Use it once per video, at the darkest point.",
])
d.h("Rewrite table")
d.table(["Not usable","Usable"],[
 ["He stabbed him in the back of the neck and it didn't kill him, so he did it again.","He attacked Kevin with a knife. It was not quick."],
 ["He hung the body by the feet to drain the blood into the dirt.","The body was found in a hidden room in the basement. Nothing about that room was improvised."],
 ["He cut off the testicles, cooked them with Worcestershire sauce and ate them.","What he did afterwards is the reason this case made headlines around the world, and the reason this video has to be careful about what it shows you."],
 ["He ordered a dehydrator to make jerky out of the muscle.","He had already ordered equipment to continue."],
 ["Spray of blood on the east wall.","Evidence on the walls confirmed where it happened."],
 ["The body was partially skinned / mutilated.","The charge was murder and mutilation of a body."],
 ["The sex room upstairs with a sling and chains.","Through an upstairs window: a blue light, black leather gear, a chrome chain."],
 ["They met for a BDSM / cannibalism fetish encounter arranged on Grindr.","They met on a dating app. The messages between them described what both men said they wanted. The police report calls them too graphic to quote."],
 ["He shot her in the face.","She died of a gunshot wound."],
 ["The baby was shaken until it stopped breathing.","The child died of head injuries that doctors said could not have been an accident."],
 ["Suspect: \"fuck you, get the fuck away from here.\"","Keep the clip, editor mutes. Transcribe as [muted]."],
 ["Photos of the victim's body, the scene, the autopsy.","Report pages, warrant text, the suspect's sketch, exterior of the house, the interview room."],
 ["\"Monster\", \"sick\", \"evil\", \"deranged\" in narration.","\"In the same flat voice he had used to talk about trust funds.\""],
 ["Naming the two 911 callers / the husband / neighbors.","\"A man from New York\", \"a young man in a leather kilt\", \"his husband\", \"a neighbor\"."],
 ["\"The gay cannibal\", \"Grindr killer\".","Mark Latunski. The case is not about the app or his sexuality, and the platform and the victim's family read it that way too."],
])
d.h("What goes on screen")
d.ule([
 "Yes: police report text (typewriter reveal, highlighted lines), warrants, the suspect's own sketch, booking photo, the house exterior, 911 audio over a static location shot, interview footage.",
 "No: scene photographs with the body or blood, autopsy material, the victim's private messages verbatim, sexual imagery seized from the house.",
 "The victim's photo only with family clearance, and only in the outro.",
])
d.h("Pacing math")
d.ule([
 "A narration break of 45–60 seconds is 110–150 words at a normal true-crime read (about 2.5 words per second). Write to 120 and cut.",
 "Three minutes of interrogation between breaks is the ceiling. In practice, the strongest sections run 60–100 seconds of clip, then 20–40 seconds of narration.",
 "Clips shorter than four seconds need an @editor note (freeze, zoom, hold), or they disappear in the edit.",
 "A full script at 700–1,500 words of narration with 40–60 clips covers a 25–40 minute video.",
])
d.h("Transcription conventions")
d.ule([
 "Narration red, transcription blue italic, clip lines bold with the timestamp as a link that opens the file at that second.",
 "Speakers labelled by role (Detective 1, Detective 2, Caller 1), not by name, unless the name is in the public record and matters.",
 "Ellipses mark cuts inside a clip. A cut inside a long answer gets \"(approximate)\" after the timestamp.",
 "Swearing is kept in the clip and marked [muted] in the transcript; it is never written out.",
 "Every @editor note is one sentence and says what to show, for how long, and on which word.",
])
d.h("The victim")
d.pe("Name them once at the start, once at the end, and with a verb that is not \"was found\". Kevin Bacon was a hairstylist and a student who went to meet a stranger on Christmas Eve and trusted him. One sentence like that, in the outro, does more than any amount of detail in the middle.")
d.save("youtube_safe_style_guide")

# =====================================================================
# DOC 5 — PORTFOLIO INDEX (needs LINKS)
# =====================================================================
if LINKS:
    d=Doc("True Crime Interrogation Scripts — Portfolio")
    d.pe("Writing samples for police-interrogation and bodycam true crime channels. Everything here was written from primary sources: released interrogation footage, 911 recordings and police reports, transcribed and time-coded by me. The scripts follow the interrogation-channel format (red narration, blue transcription, timestamped clip links, @editor notes) and are written YouTube-safe.")
    d.h("Samples")
    items=[
     ("full","Mark Latunski — Full Episode Script","Complete 30-minute episode: cold open built on two 911 calls, consent-search setup, the Dec 28 interview, the Dec 30 jail interview, plea and sentence. About 1,100 words of narration, 43 time-coded clips."),
     ("trial","Mark Latunski — Opening (intro hook, setup, first clip section)","The opening of the same case as a standalone sample, with writer's notes on the hook and the safety choices."),
     ("dossier","Mark Latunski — Research Dossier & Clip Bank","The working file behind the scripts: full timeline from the 13-page MSP report, people, 50-moment clip bank with timestamps and safety flags, five alternative cold opens, and what was left out and why."),
     ("breakdown","How Two Detectives Got Three Hours Out of Mark Latunski","An interrogation breakdown in eight phases, with timestamps, showing how the detectives' tactics map onto the structure of an episode."),
     ("style","YouTube-Safe Writing for Interrogation Channels","My working rules: a rewrite table of unusable to usable wording, what goes on screen, pacing math for narration breaks, transcription conventions."),
    ]
    d.ul([f'<b><a href="{LINKS[k]}">{E(t)}</a></b><br>{E(desc)}' for k,t,desc in items])
    d.h("How I work a case")
    d.ule([
     "Read every page of the report first and build the timeline before watching anything.",
     "Transcribe all footage with timestamps and speaker labels, then build a clip bank sorted by what each moment does (denial, admission, bizarre, tactic, emotion) and whether it is platform-safe.",
     "Find the hook in the paperwork, not in the headline. In the Latunski case it was two 911 calls nobody had connected.",
     "Write narration to the clock: 120 words per break, no clip run over three minutes, every clip link opening the file at the second.",
     "Run a safety pass last: no wounds, no bodies, no victim's messages verbatim, swearing marked for muting, the victim named with a verb at the start and the end.",
    ])
    d.h("Sources used in these samples")
    d.ule([
     "Michigan State Police incident 035-0007899-19, original and supplemental reports (printed 12/1/2022).",
     "Shiawassee County 911 recordings of Oct 10 and Nov 25, 2019.",
     "MSP interview recordings of Dec 28, 2019 (two cameras) and Dec 30, 2019.",
     "AP, WXYZ, ABC12 and WISTV reporting on the September 2022 plea and the December 15, 2022 sentence.",
    ])
    d.save("portfolio_index")
