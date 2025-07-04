import os
import sys
import threading
from tkinter import *
from tkinter import ttk, messagebox
import yt_dlp

# Determine output folder next to the script or exe
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

def download():
    urls = url_text.get("1.0", END).strip().splitlines()
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
        try:
            for url in urls:
                url = url.strip()
                if not url:
                    continue

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

            status_label.config(text="✅ All downloads complete!", foreground="blue")
        except Exception as e:
            status_label.config(text="❌ Failed: " + str(e), foreground="red")
        finally:
            progress_bar.stop()
            download_button.config(state=NORMAL)

    threading.Thread(target=run).start()

def toggle_dark_mode():
    if dark_mode_var.get():
        root.configure(bg="#1e1e1e")
        for widget in root.winfo_children():
            widget.configure(bg="#1e1e1e", fg="white")
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TButton", background="#1e1e1e", foreground="white")
        style.configure("TCombobox", fieldbackground="#1e1e1e", background="#1e1e1e", foreground="white")
        url_text.configure(bg="#2b2b2b", fg="white", insertbackground="white")
    else:
        root.configure(bg="SystemButtonFace")
        for widget in root.winfo_children():
            widget.configure(bg="SystemButtonFace", fg="black")
        style.configure("TLabel", background="SystemButtonFace", foreground="black")
        style.configure("TButton", background="SystemButtonFace", foreground="black")
        style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")
        url_text.configure(bg="white", fg="black", insertbackground="black")

# GUI Setup
root = Tk()
root.title("YouTube Downloader GUI - FINAL by DANT3")
root.geometry("520x520")
root.resizable(False, False)

style = ttk.Style(root)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))

Label(root, text="YouTube URL(s):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
url_text = Text(root, width=60, height=4)
url_text.pack()
url_text.insert(END, "Paste or drop YouTube URL(s) here...\n(Supports multiple lines)")

Label(root, text="Download Type:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
type_combo = ttk.Combobox(root, values=["Video", "Audio"])
type_combo.current(0)
type_combo.pack()

Label(root, text="Quality (for Video):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
quality_combo = ttk.Combobox(root, values=["2160", "1440", "1080", "720", "480", "360"])
quality_combo.current(0)
quality_combo.pack()

Label(root, text="Audio Format (only for Audio):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
audio_format_combo = ttk.Combobox(root, values=["mp3", "m4a", "opus", "wav"])
audio_format_combo.current(0)
audio_format_combo.pack()

Label(root, text="Audio Bitrate (kbps):", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
bitrate_combo = ttk.Combobox(root, values=["128", "192", "256", "320"])
bitrate_combo.current(3)
bitrate_combo.pack()

download_button = Button(root, text="⬇️ Download", command=download, bg="green", fg="white", font=("Segoe UI", 10, "bold"))
download_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=400)
progress_bar.pack(pady=5)

status_label = Label(root, text="", font=("Segoe UI", 10))
status_label.pack()

dark_mode_var = BooleanVar()
Checkbutton(root, text="🌙 Dark Mode", variable=dark_mode_var, command=toggle_dark_mode).pack()

Label(root, text="by DANT3", font=("Courier New", 10, "italic"), fg="gray").pack(side="bottom", pady=8)

root.mainloop()
