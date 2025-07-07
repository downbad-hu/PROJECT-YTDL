import os
import sys
import threading
from tkinter import *
from tkinter import ttk, messagebox
import yt_dlp
import subprocess

# Detect base path for PyInstaller onefile bundles
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

ffmpeg_path = os.path.join(base_path, "ffmpeg", "ffmpeg.exe")
ffprobe_path = os.path.join(base_path, "ffmpeg", "ffprobe.exe")

# Output folders
output_base = os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else base_path, "output")
output_video = os.path.join(output_base, "video")
output_audio = os.path.join(output_base, "audio")
os.makedirs(output_video, exist_ok=True)
os.makedirs(output_audio, exist_ok=True)

def download():
    url = url_entry.get().strip()
    dtype = type_combo.get()
    quality = quality_combo.get()
    audio_format = audio_format_combo.get()
    bitrate = bitrate_combo.get()

    if not url:
        messagebox.showerror("Error", "Enter a valid YouTube URL")
        return

    download_button.config(state=DISABLED)
    status_label.config(text="🔽 Downloading...", fg="green")
    progress_bar.start()

    def run():
        try:
            print(f"[INFO] Download started with URL: {url}")
            print(f"[INFO] ffmpeg: {ffmpeg_path}")
            print(f"[INFO] ffprobe: {ffprobe_path}")
            print(f"[DEBUG] Exists? ffmpeg: {os.path.exists(ffmpeg_path)}, ffprobe: {os.path.exists(ffprobe_path)}")

            ydl_opts = {
                'ffmpeg_location': os.path.dirname(ffmpeg_path),
                'noplaylist': False,
                'verbose': True,
            }

            if dtype == "Video":
                ydl_opts.update({
                    'format': f'bestvideo[height<={quality}]+bestaudio/best',
                    'outtmpl': os.path.join(output_video, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                })
            else:
                ydl_opts.update({
                    'format': 'bestaudio',
                    'outtmpl': os.path.join(output_audio, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format,
                        'preferredquality': bitrate,
                    }],
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    count = len(info['entries'])
                    status_label.config(text=f"📃 Playlist detected: {count} items", fg="purple")
                ydl.download([url])

            status_label.config(text="✅ Download complete!", fg="blue")
            output_path = output_video if dtype == "Video" else output_audio
            subprocess.Popen(f'explorer "{output_path}"')

        except Exception as e:
            print("[EXCEPTION]", e)
            status_label.config(text="❌ Error: " + str(e), fg="red")
        finally:
            progress_bar.stop()
            download_button.config(state=NORMAL)

    threading.Thread(target=run).start()

def toggle_dark_mode():
    dark = dark_var.get()
    bg = "#1e1e1e" if dark else "SystemButtonFace"
    fg = "#ffffff" if dark else "black"
    entry_bg = "#2b2b2b" if dark else "white"
    entry_fg = "#ffffff" if dark else "black"

    widgets = [url_entry, type_combo, quality_combo, audio_format_combo, bitrate_combo, download_button]
    for widget in widgets:
        try:
            widget.configure(bg=entry_bg, fg=entry_fg)
        except:
            pass

    for child in root.winfo_children():
        if isinstance(child, (Label, Checkbutton)):
            child.configure(bg=bg, fg=fg)
        elif isinstance(child, Frame):
            child.configure(bg=bg)

    status_label.configure(bg=bg, fg=fg)
    root.configure(bg=bg)

def update_fields(*args):
    if type_combo.get() == "Video":
        quality_combo.config(state="normal")
        audio_format_combo.config(state="disabled")
        bitrate_combo.config(state="disabled")
    else:
        quality_combo.config(state="disabled")
        audio_format_combo.config(state="normal")
        bitrate_combo.config(state="normal")

# GUI Setup
root = Tk()
root.title("YouTube Downloader GUI - FINAL")
root.geometry("500x470")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("default")

Label(root, text="YouTube URL:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
url_entry = Entry(root, width=60)
url_entry.pack()

Label(root, text="Download Type:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
type_combo = ttk.Combobox(root, values=["Video", "Audio"])
type_combo.current(0)
type_combo.pack()
type_combo.bind("<<ComboboxSelected>>", update_fields)

Label(root, text="Video Quality (Max):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
quality_combo = ttk.Combobox(root, values=["2160", "1440", "1080", "720", "480", "360"])
quality_combo.current(0)
quality_combo.pack()

Label(root, text="Audio Format:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
audio_format_combo = ttk.Combobox(root, values=["mp3", "m4a", "opus", "wav"])
audio_format_combo.current(3)
audio_format_combo.pack()

Label(root, text="Audio Bitrate (kbps):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 2))
bitrate_combo = ttk.Combobox(root, values=["128", "192", "256", "320"])
bitrate_combo.current(3)
bitrate_combo.pack()

download_button = Button(root, text="⬇️ Download", command=download, bg="green", fg="white", font=("Segoe UI", 10, "bold"))
download_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=400)
progress_bar.pack(pady=5)

status_label = Label(root, text="", font=("Segoe UI", 10))
status_label.pack()

dark_var = BooleanVar()
Checkbutton(root, text="🌙 Dark Mode", variable=dark_var, command=toggle_dark_mode).pack(pady=(10, 0))

Label(root, text="by d0wnbad.hu", font=("Courier New", 10, "italic"), fg="gray").pack(side="bottom", pady=10)

update_fields()

try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Fatal Error", str(e))
    if not hasattr(sys, 'frozen'):
        raise
