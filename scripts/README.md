# Full episode scripts (spec) — one complete work per case

Each case has **one complete document**: the full episode script in the RTC format (narration in red, transcriptions in blue, `Play clip` lines with timestamped links, `@editor` notes) **plus the full timestamped transcript of every source file** as an appendix, in the same layout as the channel's reference docs.

| Case | Google Doc (script + full transcript) | Repo copy | Sources |
|---|---|---|---|
| Jodi Arias (Mesa PD interrogation, July 15, 2008, Part 1) | https://docs.google.com/document/d/1qS9jx4Kh9-JjQg6q9NGUQFeRTWroHuflSi5Pio3cXz0/edit | `jodi_arias_full_script_extended.md` / `.html` | `sources/arias_*` |
| Dalia Dippolito (Boynton Beach PD interrogation + Michael Dippolito interview, Aug 5, 2009) | https://docs.google.com/document/d/1vngApOk5qjErD87LemwEgljVle-BR-TQpTDK-y-h9HM/edit | `dalia_dippolito_full_script_extended.md` / `.html` | `sources/dippolito_*` |

`jodi_arias_full_script.*` and `dalia_dippolito_full_script.*` are the script-only versions (same script, no appendix).

Transcription lines are verbatim from the released recordings (supplied transcripts plus the videos' caption tracks); narration is original and based on verified public record. No dialogue is reconstructed.

## Checked against the channel's writing guide
The full guide is in `../latunski-trial/sources/rtc_writing_guide_full.md`. `tools/check_guide.py` measures every script against it:

- narration breaks of at most about 45–60 s (≈ 150 words) — longest break: Arias 52 s, Dippolito 38 s;
- at most about three minutes of interrogation between narration breaks — longest run: Arias 178 s, Dippolito 171 s; no single clip over 90 s except one 98 s exchange;
- YouTube-safe wording (injuries summarised as "stab wounds" / "gunshot wound", no scene or autopsy photos, swearing left to the editor to mute);
- intro hook built as a mystery, set up gives who / what / where / when / why, rapport-building cut;
- writer's share (narration + intro/set-up transcriptions) inside the 700–1,500-word range; interview transcriptions are included as a courtesy for the transcription team.

## Build
`tools/script_arias.py` and `tools/script_dippolito.py` build the scripts on `tools/scriptlib.py`; `tools/full_transcript.py` builds the timestamped transcripts in `sources/*_full_transcript.html` (sentence-to-caption alignment or caption chunking); `tools/build_extended.py` appends them to the scripts; `tools/check_guide.py` reports narration/clip timings.
