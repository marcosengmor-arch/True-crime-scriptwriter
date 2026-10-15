# Full episode scripts (spec)

Scripts in the interrogation-channel format built from public interrogation footage. Transcription lines are verbatim from the released recordings (supplied transcripts plus the videos' caption tracks); narration is original and based on verified public record.

| Case | Script | Sources |
|---|---|---|
| Jodi Arias (Mesa PD, July 15, 2008) | `jodi_arias_full_script.md` / `.html` | `sources/arias_*` |
| Dalia Dippolito (Boynton Beach PD, Aug 5, 2009) | `dalia_dippolito_full_script.md` / `.html` | `sources/dippolito_*` |

Built by `tools/script_arias.py` and `tools/script_dippolito.py` on top of `tools/scriptlib.py`. Timestamps were matched with `tools/align_quotes.py` against caption tracks converted by `tools/vtt2txt.py`.
