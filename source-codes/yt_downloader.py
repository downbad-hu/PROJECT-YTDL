import os
import sys
import yt_dlp

def get_output_dir():
    """Return the output folder path next to the .exe or script."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    output = os.path.join(base_path, "output")
    os.makedirs(output, exist_ok=True)
    return output

output_dir = get_output_dir()

def list_formats(url):
    """List available formats for the given YouTube URL."""
    ydl_opts = {
        'listformats': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        return formats

def download_video(url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print("🎬 YouTube Downloader")
    url = input("🔗 Enter YouTube video or playlist URL: ").strip()

    choice = input("⬇️ Download as (v)ideo or (a)udio? ").strip().lower()

    if choice == 'v':
        print("\n🔍 Checking available formats...\n")
        formats = list_formats(url)

        # Filter formats with resolution and video
        filtered_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height')]
        filtered_formats.sort(key=lambda x: x['height'], reverse=True)

        print("🔍 Available formats (up to 4K):\n")
        for f in filtered_formats:
            res = f.get('format_note') or f.get('height')
            print(f"[{f['format_id']}] - {res} - {f['ext']} - {f.get('filesize_approx') or f.get('filesize') or 'Unknown size'}")

        format_id = input("\n🎞 Enter the format ID to download (e.g., 137, 299, 315): ").strip()
        if format_id:
            download_video(url, format_id)
        else:
            print("❌ No format selected.")

    elif choice == 'a':
        download_audio(url)
    else:
        print("❌ Invalid option selected.")

    print(f"\n✅ Download complete! Check the folder:\n{output_dir}")

if __name__ == "__main__":
    main()
