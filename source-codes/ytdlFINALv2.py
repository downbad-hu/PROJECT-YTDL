import os
import sys
import yt_dlp
from time import sleep
from tqdm import tqdm
import threading

# Define output path next to the .exe or .py file
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_path, "output")
os.makedirs(output_dir, exist_ok=True)

# Animation during download (simple progress bar)
def animate_download():
    with tqdm(total=100, bar_format="{l_bar}{bar} [Downloading...]", colour='green') as pbar:
        while not stop_anim.is_set():
            pbar.update(1)
            if pbar.n >= 100:
                pbar.n = 0
                pbar.last_print_n = 0
                pbar.refresh()
            sleep(0.05)

def show_formats(url):
    print("\n🔍 Checking available formats...\n")
    ydl_opts = {'listformats': True, 'quiet': False, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_video(url, quality):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': False,
        'progress_hooks': [progress_hook]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, audio_format, bitrate):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': bitrate,
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Hook to stop animation after download completes
def progress_hook(d):
    if d['status'] == 'finished':
        stop_anim.set()

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

        print("\n⬇️ Downloading video...")
        animation_thread = threading.Thread(target=animate_download)
        animation_thread.start()
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

        print("\n⬇️ Downloading audio...")
        animation_thread = threading.Thread(target=animate_download)
        animation_thread.start()
        download_audio(url, audio_format, bitrate)

    else:
        print("❌ Invalid choice.")
        return

    animation_thread.join()
    print(f"\n✅ Download complete! Files saved in: {output_dir}")
    input("\n🔚 Press Enter to exit...")

if __name__ == '__main__':
    stop_anim = threading.Event()
    main()
