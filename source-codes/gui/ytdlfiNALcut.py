import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp import YoutubeDL

# Determine output folder next to exe or script
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

def update_status(message, color="black"):
    status_label.config(text=message, foreground=color)
    root.update_idletasks()

def run_download(url, mode, format_choice, quality):
    try:
        update_status("⬇️ Downloading...", "green")

        if mode == "Video":
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
                    'preferredcodec': format_choice,
                    'preferredquality': quality,
                }],
            }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        update_status(f"✅ Download complete!\nSaved to: {output_dir}", "blue")
    except Exception as e:
        update_status(f"❌ Error: {e}", "red")
    finally:
        start_btn.config(state=tk.NORMAL)

def start_download():
    url = url_entry.get().strip()
    mode = mode_var.get()
    format_choice = format_var.get()
    quality = quality_var.get()

    if not url:
        messagebox.showerror("Missing URL", "Please enter a valid YouTube video or playlist URL.")
        return

    start_btn.config(state=tk.DISABLED)
    threading.Thread(target=run_download, args=(url, mode, format_choice, quality)).start()

def on_mode_change(event=None):
    mode = mode_var.get()
    if mode == "Audio":
        quality_dropdown['values'] = ["320", "256", "192", "128"]
        quality_var.set("320")
    else:
        quality_dropdown['values'] = ["2160", "1440", "1080", "720", "480", "360"]
        quality_var.set("2160")

# GUI Setup
root = tk.Tk()
root.title("🎬 YouTube Downloader GUI")
root.geometry("520x350")
root.resizable(False, False)

# --- UI Elements ---
padding_opts = {'padx': 10, 'pady': 6, 'anchor': 'w'}

tk.Label(root, text="🔗 YouTube URL:").pack(**padding_opts)
url_entry = tk.Entry(root, width=64)
url_entry.pack(padx=10)

tk.Label(root, text="⬇️ Download Type:").pack(**padding_opts)
mode_var = tk.StringVar(value="Video")
mode_dropdown = ttk.Combobox(root, textvariable=mode_var, values=["Video", "Audio"], state="readonly")
mode_dropdown.pack(padx=10)
mode_dropdown.bind("<<ComboboxSelected>>", on_mode_change)

tk.Label(root, text="🎚 Quality:").pack(**padding_opts)
quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(root, textvariable=quality_var, state="readonly")
quality_dropdown.pack(padx=10)

tk.Label(root, text="🎼 Audio Format (only for Audio):").pack(**padding_opts)
format_var = tk.StringVar(value="mp3")
ttk.Combobox(root, textvariable=format_var, values=["mp3", "m4a", "opus", "wav"], state="readonly").pack(padx=10)

start_btn = tk.Button(root, text="⬇️ Start Download", command=start_download, bg="green", fg="white")
start_btn.pack(pady=12)

status_label = tk.Label(root, text="Idle...", fg="gray")
status_label.pack()

# Initialize dropdown values
on_mode_change()

# Run the app
root.mainloop()
