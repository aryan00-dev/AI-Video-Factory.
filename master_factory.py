import os
import random
import requests
from gtts import gTTS
from moviepy.editor import *

HF_KEY = os.environ.get("HUGGINGFACE_KEY")

THEMES = [
    {"name": "Hacker", "bg": (10, 15, 10), "power": "yellow", "normal": "white"},
    {"name": "Synthwave", "bg": (20, 5, 20), "power": "cyan", "normal": "white"},
    {"name": "Alert", "bg": (15, 5, 5), "power": "red", "normal": "white"}
]
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko"]

def fetch_live_meme():
    try:
        res = requests.get("https://api.imgflip.com/get_memes").json()
        meme = random.choice(res['data']['memes'][:20])
        with open('live_meme.png', 'wb') as f:
            f.write(requests.get(meme['url']).content)
        return True
    except: return False

def fetch_live_audio():
    bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
    pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
    try:
        with open('live_bgm.ogg', 'wb') as f: f.write(requests.get(bgm_url).content)
        with open('live_pop.ogg', 'wb') as f: f.write(requests.get(pop_url).content)
        return True
    except: return False

def get_voice(text, filename="audio.mp3"):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    try:
        res = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(res.content)
            return
    except: pass
    gTTS(text=text, lang='hi', slow=False).save(filename)

def build_video():
    has_meme = fetch_live_meme()
    has_audio = fetch_live_audio()
    
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    
    audio_elements = [voice_clip]
    if has_audio:
        bgm_clip = AudioFileClip("live_bgm.ogg").volumex(0.1).set_duration(total_duration)
        audio_elements.append(bgm_clip)

    theme = random.choice(THEMES)
    bg_clip = ColorClip(size=(1080, 1920), color=theme["bg"], duration=total_duration)
    visual_elements = [bg_clip]
    
    if has_meme:
        meme_clip = (ImageClip("live_meme.png")
                     .set_duration(2.5)
                     .resize(width=700)
                     .set_position(('center', 'bottom'))
                     .crossfadein(0.2).crossfadeout(0.2))
        visual_elements.append(meme_clip)

    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        if len(clean) > 5 or clean in POWER_WORDS:
            color, size = theme["power"], 145
            if has_audio:
                pop_sfx = AudioFileClip("live_pop.ogg").volumex(0.5).set_start(current_time)
                audio_elements.append(pop_sfx)
        else:
            color, size = theme["normal"], 90
            
        txt = (TextClip(word, fontsize=size, color=color, font='Arial-Bold', method='caption', size=(900, None))
               .set_position(('center', 'center'))
               .set_start(current_time)
               .set_duration(time_per_word))
               
        visual_elements.append(txt)
        current_time += time_per_word

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)
    final_video.write_videofile("final_tech_viral_video.mp4", fps=30, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    build_video()
