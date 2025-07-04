import os
import sys
import yt_dlp
import threading
import time

# Create output directory next to the executable or script
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

# Spinner animation during download
class Spinner:
    def __init__(self, message="Downloading"):
        self.stop_running = False
        self.message = message

    def start(self):
        def animate():
            for c in '|/-\\':
                if self.stop_running:
                    break
                print(f'\r{self.message}... {c}', end='', flush=True)
                time.sleep(0.1)
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while not self.stop_running:
            for c in '|/-\\':
                if self.stop_running:
                    break
                print(f'\r{self.message}... {c}', end='', flush=True)
                time.sleep(0.1)

    def stop(self):
        self.stop_running = True
        self.thread.join()
        print('\r✅ Download finished!       ')

# Show formats
def show_formats(url):
    print("\n🔍 Checking available formats...\n")
    ydl_opts = {'listformats': True, 'quiet': False, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Download video with specified quality
def download_video(url, quality):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': False,
        'quiet': True
    }
    spinner = Spinner("🎬 Downloading video")
    spinner.start()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    spinner.stop()

# Download audio with format + bitrate
def download_audio(url, audio_format, bitrate):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': bitrate,
        }],
    }
    spinner = Spinner("🎧 Downloading audio")
    spinner.start()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    spinner.stop()

# Main UI
def main():
    print("\n🎬 YouTube Downloader (Video/Audio, up to 4K, Playlist Supported)")
    url = input("🔗 Enter YouTube video or playlist URL: ").strip()

    show_formats(url)

    choice = input("\n⬇️ Download as (v)ideo or (a)udio? ").strip().lower()

    if choice == 'v':
        print("\n🎞 Choose max resolution:")
        print(" 1. 2160 (4K)\n 2. 1440\n 3. 1080\n 4. 720\n 5. 480\n 6. 360")
        res_map = {'1': '2160', '2': '1440', '3': '1080', '4': '720', '5': '480', '6': '360'}
        res_choice = input("🔢 Select [1-6, default 2160]: ").strip() or '1'
        quality = res_map.get(res_choice, '2160')
        download_video(url, quality)

    elif choice == 'a':
        print("\n🎧 Choose audio format:")
        print(" 1. mp3\n 2. m4a\n 3. opus\n 4. wav")
        format_map = {'1': 'mp3', '2': 'm4a', '3': 'opus', '4': 'wav'}
        format_choice = input("🎼 Format [1-4, default mp3]: ").strip() or '1'
        audio_format = format_map.get(format_choice, 'mp3')

        print("\n🎚 Choose bitrate (kbps):")
        print(" 1. 128\n 2. 192\n 3. 256\n 4. 320")
        bitrate_map = {'1': '128', '2': '192', '3': '256', '4': '320'}
        bitrate_choice = input("🎛 Bitrate [1-4, default 192]: ").strip() or '2'
        bitrate = bitrate_map.get(bitrate_choice, '192')

        download_audio(url, audio_format, bitrate)

    else:
        print("❌ Invalid choice.")

    print(f"\n📁 Files saved in: {output_dir}")
    input("\n🔚 Press Enter to exit...")

if __name__ == '__main__':
    main()
