def find_free_clip(star):
    try:
        import yt_dlp
        query = f"{star} airport look latest short"
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'], # bypasses bot check
                }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if result and 'entries' in result and result['entries']:
                return result['entries'][0].get('url')
    except Exception as e:
        print(f"Search error: {e}")
    return None

def download_clip(url, out="/tmp/raw.mp4"):
    try:
        import yt_dlp
        ydl_opts = {
            'outtmpl': out,
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return out
    except Exception as e:
        print(f"Download error: {e}")
        return None

def main():
    star = random.choice(STARS)
    print(f"Testing upload only - Star: {star}")
    # Create 10 sec dummy video with text for test
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
    bg = ColorClip(size=(1080,1920), color=(0,0,0), duration=10)
    txt = TextClip(f"BLINKTOLLYWOOD\n{star}\nTest Upload", fontsize=60, color='white', font='DejaVu-Sans-Bold').set_duration(10).set_position('center')
    video = CompositeVideoClip([bg, txt])
    video.write_videofile("/tmp/blink_final.mp4", fps=24, codec='libx264')

    title = f"{star} Latest Look | BlinkTollywood Test"
    desc = f"Testing BlinkTollywood bot #blinktollywood"
    post_to_youtube("/tmp/blink_final.mp4", title, desc)
