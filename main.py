import os, random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

STARS = ["Allu Arjun", "Prabhas", "Jr NTR", "Ram Charan", "Mahesh Babu", "Pawan Kalyan", "Vijay Deverakonda", "Nani", "Rashmika Mandanna", "Sreeleela", "Pooja Hegde", "Samantha", "Kajal Aggarwal"]

def post_to_youtube(video_path, title, description):
    client_id = os.environ.get('YT_CLIENT_ID')
    client_secret = os.environ.get('YT_CLIENT_SECRET')
    refresh_token = os.environ.get('YT_REFRESH_TOKEN')
    print(f"Checking creds... ID:{bool(client_id)} SECRET:{bool(client_secret)} REFRESH:{bool(refresh_token)}")
    creds = Credentials(None, refresh_token=refresh_token, token_uri='https://oauth2.googleapis.com/token', client_id=client_id, client_secret=client_secret, scopes=['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": description, "tags": ["Tollywood", "BlinkTollywood"], "categoryId": "24"}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=video_path
    )
    response = request.execute()
    print(f"✅ POSTED: https://youtu.be/{response['id']}")
    return True

def main():
    star = random.choice(STARS)
    print(f"Testing YouTube upload - Star: {star}")
    bg = ColorClip(size=(1080,1920), color=(10,10,10), duration=8)
    txt1 = TextClip("BLINKTOLLYWOOD", fontsize=70, color='white', font='DejaVu-Sans-Bold', stroke_color='yellow', stroke_width=3).set_duration(8).set_position(('center', 700))
    txt2 = TextClip(star, fontsize=55, color='yellow', font='DejaVu-Sans-Bold').set_duration(8).set_position(('center', 900))
    txt3 = TextClip("Tollywood Updates Every 2 Hours", fontsize=30, color='white').set_duration(8).set_position(('center', 1100))
    video = CompositeVideoClip([bg, txt1, txt2, txt3])
    video.write_videofile("/tmp/blink_final.mp4", fps=24, codec='libx264', audio_codec='aac')
    title = f"{star} Latest Look | BlinkTollywood"
    desc = f"One Word For {star}? Comment!\n\nFollow BlinkTollywood for Tollywood news\n\n#blinktollywood #{star.replace(' ','')}"
    post_to_youtube("/tmp/blink_final.mp4", title, desc)

if __name__ == "__main__":
    main()
