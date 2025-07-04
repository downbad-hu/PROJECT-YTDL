import os
import sys
import yt_dlp
import threading
import time
from colorama import init, Fore, Style

init(autoreset=True)

# Detect output path (same folder as .exe or script)
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

# Animation
class SmoothProgress:
    def __init__(self):
        self.running = False
        self.last_update = 0
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def animate(self):
        bar = ""
        while self.running:
            if time.time() - self.last_update >= 0.2:
                bar += "-"
                print(Fore.GREEN + bar, end="\r")
                self.last_update = time.time()
            time.sleep(0.05)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\n")

# Show available formats
def show_formats(url):
    print("\n🔍 Checking available formats...\n")
    ydl_opts = {'listformats': True, 'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Download video
def download_video(url, quality):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': False,
    }
    progress = SmoothProgress()
    progress.start()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    progress.stop()

# Download audio
def download_audio(url, audio_format, bitrate):
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
    progress = SmoothProgress()
    progress.start()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    progress.stop()

def main():
    print("\n🎬 YouTube Downloader (Video/Audio, up to 4K, Playlists supported)")
    url = input("🔗 Enter YouTube video or playlist URL: ").strip()

    show_formats(url)

    choice = input("\n⬇️ Download as (v)ideo or (a)udio? ").strip().lower()

    if choice == 'v':
        print("\n🎞 Choose maximum video resolution:")
        print(" 1. 2160 (4K)\n 2. 1440\n 3. 1080\n 4. 720\n 5. 480\n 6. 360")
        res_map = {'1': '2160', '2': '1440', '3': '1080', '4': '720', '5': '480', '6': '360'}
        res_choice = input("🔢 Select resolution [1-6, default 2160]: ").strip() or '1'
        quality = res_map.get(res_choice, '2160')
        download_video(url, quality)

    elif choice == 'a':
        print("\n🎧 Choose audio format:")
        print(" 1. mp3\n 2. m4a\n 3. opus\n 4. wav")
        format_map = {'1': 'mp3', '2': 'm4a', '3': 'opus', '4': 'wav'}
        format_choice = input("🎼 Select audio format [1-4, default mp3]: ").strip() or '1'
        audio_format = format_map.get(format_choice, 'mp3')

        print("\n🎚 Choose audio bitrate (kbps):")
        print(" 1. 128\n 2. 192\n 3. 256\n 4. 320")
        bitrate_map = {'1': '128', '2': '192', '3': '256', '4': '320'}
        bitrate_choice = input("🎛 Select bitrate [1-4, default 192]: ").strip() or '2'
        bitrate = bitrate_map.get(bitrate_choice, '192')

        download_audio(url, audio_format, bitrate)

    else:
        print("❌ Invalid choice.")

    print(f"\n✅ Download complete! Files saved to: {output_dir}")
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
