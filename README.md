# 📥 downbaDOWNLOADER.exe

A sleek and powerful YouTube Downloader built for Windows — no Python or FFmpeg installation needed. Just run and download with ease.

---

## ⚡ Features

- ✅ **Standalone `.exe`** — No Python or dependencies required
- 🎞️ Download **videos** in high quality (up to 4K)
- 🎧 Extract **audio** in multiple formats (`mp3`, `wav`, `m4a`, `opus`)
- 📃 Supports **playlist downloads**
- 🌙 **Dark mode toggle**
- 📂 All downloads are saved next to the executable in an `output/` folder
- 🧩 **FFmpeg embedded** — No external setup
- 💡 Simple, clean, and beginner-friendly interface

---

## 🧊 How to Use

1. 🔽 Download `downbaDOWNLOADER.exe` from [Releases](#)
2. 📂 Place it anywhere (Desktop, Downloads, etc.)
3. 📋 Paste a YouTube video/playlist URL
4. 🎯 Select:
   - **Video or Audio**
   - **Quality or Format**
5. 💾 Click **Download**
6. ✅ Your file(s) will appear inside the `output/video` or `output/audio` folders automatically

---

## 🗂️ Output Folder Structure

📁 output/
├── 📁 video/ ← downloaded MP4 files
└── 📁 audio/ ← downloaded MP3/WAV/M4A/OPUS files

yaml
Copy
Edit

---

## 🛠️ How This EXE Was Built (Dev Notes)

If you're a developer or curious how this works:

```bash
pyinstaller --onefile ^
  --add-data "ffmpeg\\ffmpeg.exe;ffmpeg" ^
  --add-data "ffmpeg\\ffprobe.exe;ffmpeg" ^
  downbaDOWNLOADER.py
FFmpeg binaries are bundled inside the EXE via --add-data.

## 🙋 FAQ

**Q:** **Does it require internet?**  
**A:** **Yep** — it needs an active connection to fetch video/audio from YouTube.

**Q:** **Do I need to install Python or FFmpeg?**  
**A:** **Nah.** Everything you need is baked right into the `.exe`.

**Q:** **I got a SmartScreen warning — is this safe?**  
**A:** **Totally.** Windows flags unsigned apps by default. Just hit **"More info" → "Run anyway"** and you're good.

---

## 👤 Credits

**Made with 💚 by d0wnbad.hu**  
**_"When downloading ain't a crime, it's a vibe."_**

---

## 📄 License

🆓 **Free for personal use only**  
🚫 **Not for resale or third-party store redistribution**  
📁 **Respect the code, respect the craft.**












