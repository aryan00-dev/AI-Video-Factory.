import os
import random
import requests
import urllib.request
from gtts import gTTS
from moviepy.editor import *

HF_KEY = os.environ.get("HUGGINGFACE_KEY")

THEMES = [
    {"name": "Hacker", "bg": (10, 15, 10), "power": "yellow", "normal": "white"},
    {"name": "Synthwave", "bg": (20, 5, 20), "power": "cyan", "normal": "white"},
    {"name": "Alert", "bg": (15, 5, 5), "power": "red", "normal": "white"}
]
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt"]

def get_voice(text, filename="audio.mp3"):
    print("[+] Calling Hugging Face Open-Source Voice...")
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    try:
        res = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(res.content)
            return
    except: pass
    print("[!] Fallback: Using gTTS...")
    gTTS(text=text, lang='hi', slow=False).save(filename)

def get_bgm(filename="bgm.mp3"):
    print("[+] Fetching Free BGM...")
    try:
        # Public domain safe loop
        url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
        urllib.request.urlretrieve(url, filename)
        return True
    except:
        print("[-] BGM Fetch failed. Proceeding without BGM.")
        return False

def build_video():
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    
    if get_bgm("bgm.mp3"):
        bgm_clip = AudioFileClip("bgm.mp3").volumex(0.1).set_duration(voice_clip.duration)
        final_audio = CompositeAudioClip([voice_clip, bgm_clip])
    else:
        final_audio = voice_clip

    theme = random.choice(THEMES)
    bg_clip = ColorClip(size=(1080, 1920), color=theme["bg"], duration=final_audio.duration)

    words = script.split()
    time_per_word = final_audio.duration / len(words)
    text_clips = []
    current_time = 0.0
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        if len(clean) > 5 or clean in POWER_WORDS:
            color, size = theme["power"], 140
        else:
            color, size = theme["normal"], 90
            
        txt = (TextClip(word, fontsize=size, color=color, font='Arial-Bold', method='caption', size=(900, None))
               .set_position('center')
               .set_start(current_time)
               .set_duration(time_per_word)
               .crossfadein(0.05))
        text_clips.append(txt)
        current_time += time_per_word

    final_video = CompositeVideoClip([bg_clip] + text_clips).set_audio(final_audio)
    final_video.write_videofile("final_tech_viral_video.mp4", fps=24, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    build_video()
