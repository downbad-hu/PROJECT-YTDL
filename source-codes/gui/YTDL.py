import os
import sys
import threading
from tkinter import *
from tkinter import ttk, messagebox
import yt_dlp

# Determine output folder
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

def download_single(url, dtype, quality, audio_format, bitrate):
    if dtype == "Video":
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': False,
        }
    else:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': bitrate,
            }],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download():
    urls_raw = url_text.get("1.0", END).strip()
    urls = [u.strip() for u in urls_raw.replace(",", "\n").splitlines() if u.strip()]
    dtype = type_combo.get()
    quality = quality_combo.get()
    audio_format = audio_format_combo.get()
    bitrate = bitrate_combo.get()

    if not urls:
        messagebox.showerror("Error", "Please enter at least one valid YouTube URL")
        return

    download_button.config(state=DISABLED)
    status_label.config(text="🔽 Downloading...", foreground="green")
    progress_bar.start()

    def run():
        success = 0
        for url in urls:
            try:
                download_single(url, dtype, quality, audio_format, bitrate)
                success += 1
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}")
        progress_bar.stop()
        download_button.config(state=NORMAL)
        if success == len(urls):
            status_label.config(text="✅ All downloads complete!", foreground="blue")
        elif success == 0:
            status_label.config(text="❌ All downloads failed!", foreground="red")
        else:
            status_label.config(text=f"⚠️ {success} of {len(urls)} downloads completed", foreground="orange")

    threading.Thread(target=run).start()

# GUI Setup
root = Tk()
root.title("YouTube Downloader GUI - by downbad.hu")
root.geometry("520x540")
root.resizable(False, False)

style = ttk.Style(root)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))

Label(root, text="YouTube URLs (one per line or comma-separated):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
url_text = Text(root, height=5, width=62, wrap=WORD)
url_text.pack()

Label(root, text="Download Type:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
type_combo = ttk.Combobox(root, values=["Video", "Audio"], state="readonly")
type_combo.current(0)
type_combo.pack()

Label(root, text="Video Quality (max):", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
quality_combo = ttk.Combobox(root, values=["2160", "1440", "1080", "720", "480", "360"], state="readonly")
quality_combo.current(0)
quality_combo.pack()

Label(root, text="Audio Format (for Audio):", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
audio_format_combo = ttk.Combobox(root, values=["mp3", "m4a", "opus", "wav"], state="readonly")
audio_format_combo.current(0)
audio_format_combo.pack()

Label(root, text="Audio Bitrate (kbps):", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
bitrate_combo = ttk.Combobox(root, values=["128", "192", "256", "320"], state="readonly")
bitrate_combo.current(3)
bitrate_combo.pack()

download_button = Button(root, text="⬇️ Start Download", command=download, bg="green", fg="white", font=("Segoe UI", 10, "bold"))
download_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=400)
progress_bar.pack(pady=5)

status_label = Label(root, text="", font=("Segoe UI", 10))
status_label.pack()

# Watermark
Label(root, text="by downbad.hu", font=("Courier New", 10, "italic"), fg="gray").pack(side="bottom", pady=10)

root.mainloop()
