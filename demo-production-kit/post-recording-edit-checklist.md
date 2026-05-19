# Post-Recording Edit Checklist

Run this after every recording session, before exporting or publishing anything.  
**Label:** Manual process — no automated editing happens here.

---

## Step 1 — Ingest & Backup (do first, before anything else)

- [ ] Copy raw recording to at least 2 storage locations
- [ ] Rename file to convention: `YYYYMMDD-[tool]-take[N]-raw.mkv`
- [ ] Remux MKV to MP4 if needed: `ffmpeg -i input.mkv -c copy output.mp4`
- [ ] Log the recording in `raw/notes/execution-log-[tool].md` (timestamps, takes, notes)
- [ ] Listen back to full audio before starting edit — catch any mic / noise issues early

---

## Step 2 — Rough Cut

- [ ] Import raw file(s) into editor (Premiere / DaVinci / CapCut)
- [ ] Cut the top and tail (remove pre-roll silence and post-roll fumbling)
- [ ] Remove obvious mistakes, restarts, and long pauses
- [ ] Place the hook shot first — confirm it lands within first 3 seconds
- [ ] Arrange shots in order from shot list
- [ ] Export rough cut for review: `[tool]-v1-roughcut.mp4`

---

## Step 3 — Audio Polish

- [ ] Normalize audio: peaks at -6dB to -3dB, floor at -18dB
- [ ] Remove background noise (DaVinci: Magic Voice Isolation / Premiere: Enhance Speech)
- [ ] Remove breath sounds between sentences (optional — don't over-process)
- [ ] Add music bed (royalty-free only) at -20dB to -25dB under voice
- [ ] Duck music under speech automatically (if editor supports it)
- [ ] Check audio on earbuds AND speakers — different EQ profiles

---

## Step 4 — Visual Polish

- [ ] Color grade: add slight contrast boost and warm or cool grade to match brand
- [ ] Zoom in on key moments (prompt entry, output reveal) if not captured with Scene 4
- [ ] Add animated cursor highlight if needed (ScreenFlow / Camtasia feature)
- [ ] Speed up processing/loading scenes (2x or cut entirely if > 15 seconds)
- [ ] Slow down or hold on output reveal — give viewers time to read
- [ ] Remove any accidental PII: blur email addresses, personal bookmarks, API keys

---

## Step 5 — Captions / Subtitles

- [ ] Auto-generate captions (Premiere, DaVinci, CapCut, or Descript)
- [ ] Review and fix every caption — AI transcription has errors
- [ ] Style: white text, black outline or dark background, centered, 2–3 words per frame
- [ ] Burn-in captions for TikTok / Reels / Shorts (viewers watch without sound)
- [ ] Export separate `.srt` file for YouTube upload

---

## Step 6 — Text Overlays & Graphics

- [ ] Add hook text overlay (first 3–5 seconds)
- [ ] Add prompt text overlay when you type ("My prompt: ...")
- [ ] Add score badge overlay in verdict section
- [ ] Add CTA text overlay at end ("Subscribe / Follow / Link in Bio")
- [ ] Add lower third with your name / brand (long-form only)
- [ ] Check: no overlays cover important UI elements

---

## Step 7 — Platform Versions

- [ ] Long-form: export 1920×1080, H.264, 30fps, target bitrate 8–12 Mbps
- [ ] Short-form 9:16: reframe to 1080×1920, add motion crop if needed
- [ ] Verify short-form starts with hook in first 0–1 second (no dead air)
- [ ] Shorts / Reels: max 60 seconds — trim if needed
- [ ] TikTok: avoid showing other platforms' logos if possible (algorithmic risk)

---

## Step 8 — Thumbnail

- [ ] Create thumbnail per `thumbnail-brief-template.md`
- [ ] Export: 1280×720 PNG, < 2 MB
- [ ] Check at small size (120×68 px) — text must be legible
- [ ] A/B test: prepare 2 thumbnail versions for YouTube Studio split test

---

## Step 9 — Publishing Assets

- [ ] Write title(s) from `caption-and-title-template.md`
- [ ] Write description with timestamps
- [ ] Add tags
- [ ] Write platform captions (TikTok, Instagram, Twitter, LinkedIn)
- [ ] Write pinned comment
- [ ] Save all copy in `publish/` folder

---

## Step 10 — Final Export & QC

- [ ] Watch the full long-form export start to finish — catch any cut errors
- [ ] Watch the short-form on a phone — verify it looks good on mobile
- [ ] Verify audio sync on all exports
- [ ] Verify no personal data / credentials visible anywhere
- [ ] File naming convention correct on all exports
- [ ] All files backed up before upload

---

## Step 11 — Upload (manual — do not automate without approval)

- [ ] Upload long-form to YouTube (schedule if not posting immediately)
- [ ] Upload short-form to YouTube Shorts, TikTok, Instagram Reels
- [ ] Add thumbnail, description, tags, captions in each platform
- [ ] Set end screens and cards (YouTube)
- [ ] Post pinned comment immediately after publishing
- [ ] Cross-post text version to Twitter / LinkedIn

---

## Step 12 — Log & Iterate

- [ ] Fill in `performance_log.md` with publish dates and initial metrics
- [ ] Schedule 7-day and 30-day metric review
- [ ] Note what to improve for next demo
- [ ] Update scorecard in `raw/notes/` if any scores changed after full review
