# OBS Recording Setup — AI Tool Demos

**Label:** Manual setup required. This document describes the recommended OBS configuration — not executed automatically.

---

## Install OBS

Download from [obsproject.com](https://obsproject.com) — free, open source, Windows / Mac / Linux.

---

## Recommended Scene Collection for AI Tool Demos

Create one Scene Collection called **"AI Demo"** with the following scenes:

### Scene 1 — Full Browser (primary)
- Source: **Window Capture** → select your browser window (Chrome / Arc / Firefox)
- Resolution: 1920×1080 (or 1280×720 for faster exports)
- Use this for: showing the AI tool UI

### Scene 2 — Browser + Face Cam (talking head)
- Source 1: Window Capture (browser, full width)
- Source 2: Video Capture Device (webcam) — bottom right, 320×180, rounded mask
- Use this for: intros, reactions, explanations

### Scene 3 — Terminal / Code Only
- Source: Window Capture → Terminal / VS Code
- Use this for: code demos, API key setup
- Optional: add a **Color Correction** filter → boost contrast slightly

### Scene 4 — Zoom / Detail
- Duplicate Scene 1, add a **Crop/Pad** filter and scale up the center region by ~1.5×
- Use this for: highlighting a specific UI element or result

### Scene 5 — Outro Card
- Source: Image → your outro card PNG (1920×1080)
- Optional: add a 5-second **Scene Transition** (fade)

---

## Output Settings

**Settings → Output → Recording:**

| Setting        | Value                     |
|----------------|---------------------------|
| Recording Path | `~/Recordings/ai-demos/`  |
| Format         | MKV (safer on crash) → remux to MP4 after |
| Encoder        | Hardware (NVENC / AMF / VideoToolbox) if available; else x264 |
| Rate Control   | CRF / CQP                 |
| CQ Level       | 18 (high quality)         |
| Preset         | Quality                   |
| Audio Bitrate  | 320 kbps                  |

**Settings → Video:**

| Setting          | Value         |
|------------------|---------------|
| Base Resolution  | 1920×1080     |
| Output Resolution| 1920×1080     |
| FPS              | 30 (60 for smoother UI scroll) |

---

## Audio Setup

**Sources → Audio Input Capture** → select your microphone  
- Apply **Noise Suppression** filter (RNNoise plugin or built-in)
- Apply **Compressor** filter: Ratio 4:1, Threshold -18dB, Attack 6ms, Release 60ms
- Apply **Limiter** filter: Threshold -3dB

Test: speak normally — peaks should hit -12dB to -6dB in the audio meter.

---

## Hotkeys (recommended)

| Action               | Hotkey        |
|----------------------|---------------|
| Start / Stop Record  | Ctrl+Shift+R  |
| Pause / Resume       | Ctrl+Shift+P  |
| Switch to Scene 1    | F1            |
| Switch to Scene 2    | F2            |
| Switch to Scene 3    | F3            |
| Switch to Scene 4    | F4            |

---

## Vertical / Short-Form Recording (TikTok / Reels / Shorts)

Option A — Letterbox method:
- Set OBS output to 1080×1920
- Use a vertical browser window (resize Chrome to ~400px wide, tall)
- Pad sides with black or blurred background

Option B — Reframe in post:
- Record at 1920×1080 as normal
- In your editor (Premiere / CapCut / DaVinci) reframe to 9:16 and add motion crop / zoom

**Recommended:** Option B — easier to repurpose one recording into multiple formats.

---

## File Naming Convention

```
YYYYMMDD-[tool-name]-[take]-[version].mkv
Example: 20260519-canva-ai-take1-raw.mkv
```

Remux to MP4 after recording:
```bash
ffmpeg -i 20260519-canva-ai-take1-raw.mkv -c copy 20260519-canva-ai-take1-raw.mp4
```

---

## Pre-Recording Checklist

- [ ] Close all browser tabs not needed for the demo
- [ ] Clear browser notifications (Do Not Disturb mode on)
- [ ] Hide personal bookmarks bar or use a clean browser profile
- [ ] Set browser zoom to 100% (Ctrl+0)
- [ ] Close Slack, email, calendar alerts
- [ ] Plug in power (laptop battery throttles encoding)
- [ ] Test audio level — speak a sentence, verify -12dB peaks
- [ ] Do a 10-second test record, play back to verify audio + video
- [ ] Start OBS recording
- [ ] Wait 3 seconds before speaking (gives editor a clean cut-in)
