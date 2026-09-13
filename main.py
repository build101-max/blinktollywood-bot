import os, random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

STARS = ["Allu Arjun", "Prabhas", "Jr NTR", "Ram Charan", "Mahesh Babu", "Pawan Kalyan", "Vijay Deverakonda", "Nani", "Ram Pothineni", "Chiranjeevi", "Rashmika Mandanna", "Sreeleela", "Pooja Hegde", "Samantha", "Keerthy Suresh", "Mrunal Thakur", "Anushka Shetty", "Kajal Aggarwal", "Shruti Haasan", "Krithi Shetty"]

def find_free_clip(star):
    try:
        import yt_dlp
        query = f"{star} airport look latest"
        ydl_opts = {'quiet': True, 'skip_download': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if result and 'entries' in result:
                return result['entries'][0].get('url')
    except: pass
    return None

def download_clip(url, out="/tmp/raw.mp4"):
    try:
        import yt_dlp
        ydl_opts = {'outtmpl': out, 'format': 'mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return out
    except: return None

def make_video(input_video, star_name, output="/tmp/blink_final.mp4"):
    clip = VideoFileClip(input_video).subclip(0, 15)
    clip = clip.resize(height=1920)
    w,h = clip.size
    clip = clip.crop(x1=w//2-540, width=1080, height=1920)
    watermark = TextClip("BLINKTOLLYWOOD", fontsize=42, color='white', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=3)
    watermark = watermark.set_position(('right','bottom')).set_duration(clip.duration).margin(right=25, bottom=90, opacity=0)
    final = CompositeVideoClip([clip, watermark])
    final.write_videofile(output, codec='libx264', audio_codec='aac', fps=30)
    title = f"{star_name} Latest Airport Look | BlinkTollywood"
    desc = f"One Word For {star_name}? Comment below!\n\nFollow BlinkTollywood\n\n#{star_name.replace(' ','')} blinktollywood"
    return output, title, desc

def post_to_youtube(video_path, title, description):
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    client_id = os.environ.get('YT_CLIENT_ID')
    client_secret = os.environ.get('YT_CLIENT_SECRET')
    refresh_token = os.environ.get('YT_REFRESH_TOKEN')
    if not all([client_id, client_secret, refresh_token]): return False
    creds = Credentials(None, refresh_token=refresh_token, token_uri='https://oauth2.googleapis.com/token', client_id=client_id, client_secret=client_secret, scopes=['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": description, "tags": ["Tollywood", "BlinkTollywood"], "categoryId": "24"}, "status": {"privacyStatus": "public"}}, media_body=video_path)
    response = request.execute()
    print(f"Posted: https://youtu.be/{response['id']}")
    return True

def main():
    star = random.choice(STARS)
    print(f"Star: {star}")
    url = find_free_clip(star)
    if not url: return
    raw = download_clip(url, "/tmp/raw.mp4")
    if not raw: return
    final, title, desc = make_video(raw, star)
    post_to_youtube(final, title, desc)

if __name__ == "__main__":
    main()
