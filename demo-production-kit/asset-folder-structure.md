# Asset Folder Structure

Follow this layout for every AI tool demo. Consistent organization means faster editing, easier reuse, and no lost files.

---

## Root Layout

```
ai-demos/
  [tool-name]/
    raw/
    working/
    final/
    publish/
```

---

## Detailed Structure

```
ai-demos/
  canva-ai/
    raw/
      recordings/
        20260519-canva-ai-take1-raw.mkv
        20260519-canva-ai-take2-raw.mkv
      screenshots/
        canva-homepage.png
        canva-ai-output-result.png
        canva-free-plan-limits.png
      notes/
        scorecard-canva-ai.md          ← filled after live test
        execution-log-canva-ai.md      ← timestamps, what happened
    working/
      edits/
        canva-ai-v1.prproj             ← Premiere / DaVinci project file
        canva-ai-v1-cut.mp4            ← rough cut export
      audio/
        voiceover-take1.wav
        voiceover-take2-clean.wav
      captions/
        canva-ai-captions.srt
      graphics/
        thumbnail-v1.png
        thumbnail-v2-approved.png
        lower-third-canva.png
    final/
      long-form/
        canva-ai-youtube-final.mp4     ← 1920×1080, H.264
      short-form/
        canva-ai-reels-final.mp4       ← 1080×1920, H.264
        canva-ai-shorts-final.mp4      ← 1080×1920, H.264
      thumbnail/
        canva-ai-thumbnail-final.png   ← 1280×720 PNG
    publish/
      canva-ai-youtube-description.txt
      canva-ai-tiktok-caption.txt
      canva-ai-instagram-caption.txt
      canva-ai-twitter-thread.txt
      canva-ai-linkedin-post.txt
      canva-ai-pinned-comment.txt
      canva-ai-scorecard-published.md  ← final scores for public
```

---

## File Naming Convention

```
YYYYMMDD-[tool-name]-[type]-[version].[ext]

Examples:
20260519-canva-ai-take1-raw.mkv
20260519-canva-ai-vo-take2-clean.wav
20260519-canva-ai-thumbnail-v2.png
20260519-canva-ai-reels-final.mp4
```

**Rules:**
- Always use lowercase with hyphens — no spaces, no underscores, no camelCase
- Always include the date prefix — prevents collisions and helps sort chronologically
- Always mark raw files as `-raw`
- Always mark approved finals as `-final` or `-approved`
- Never overwrite a raw file — create a new version instead

---

## Storage Targets

| Folder   | Where to store              | Backup?  |
|----------|-----------------------------|----------|
| `raw/`   | Local NAS or external SSD   | Yes — 2 copies |
| `working/`| Local drive + cloud backup | Yes      |
| `final/` | Cloud (Google Drive / Dropbox) | Yes   |
| `publish/`| Git repo or Notion         | Yes      |

**Minimum backup rule:** Raw recordings in at least 2 places before editing begins. A lost recording cannot be re-recorded identically.

---

## Cleanup After Publishing

After a video goes live:

1. Move raw recordings to cold storage (external drive / archival S3)
2. Delete working edit versions older than 90 days
3. Keep `final/` files indefinitely — these are the publishable masters
4. Keep `publish/` copy files in git repo for reuse

---

## Shared Demo Backlog Folder

```
ai-demos/
  _backlog/
    ai-tool-demo-backlog.md       ← master list of upcoming demos
    demo-workflow-template.md     ← blank template
    ai-tool-test-scorecard.md     ← blank scorecard
  _kit/                           ← this production kit
```
