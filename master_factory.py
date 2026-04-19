import os
import random
import requests
from gtts import gTTS
from moviepy.editor import *
import urllib.request

# Keys
HF_KEY = os.environ.get("HUGGINGFACE_KEY")

# 1. Random Vibe Generator (Aesthetics)
THEMES = [
    {"name": "Hacker", "bg": (10, 15, 10), "power_color": "yellow", "normal_color": "white"},
    {"name": "Synthwave", "bg": (20, 5, 20), "power_color": "cyan", "normal_color": "white"},
    {"name": "Alert", "bg": (15, 5, 5), "power_color": "red", "normal_color": "white"},
    {"name": "Clean Tech", "bg": (5, 10, 20), "power_color": "green", "normal_color": "white"}
]
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt"]

def get_free_hf_voice(text, filename="audio.mp3"):
    print("[+] Voice Engine: Calling Hugging Face Open-Source Model...")
    # HF Inference API Endpoint (Free TTS fallback)
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("[+] Voice Engine: Real AI Voice Generated via HF!")
            return True
    except Exception as e:
        print(f"[-] HF Server Busy. Error: {e}")
    
    print("[!] Fail-Safe Active: Using gTTS Backup...")
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save(filename)
    return True

def build_video():
    print("[SYSTEM] Final Master Editor Initiated...")
    
    # Read viral script
    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script = f.read().strip()
    except:
        script = "Agar tum abhi bhi ChatGPT use kar rahe ho, toh tum bohot peeche ho. Yeh naya secret free AI website khatarnak hai."
        
    # Generate Voice
    get_free_hf_voice(script, "audio.mp3")
    audio_clip = AudioFileClip("audio.mp3")
    total_duration = audio_clip.duration

    # Select Theme
    theme = random.choice(THEMES)
    print(f"[+] Vibe Generator: Selected '{theme['name']}' Theme")
    
    # Deep Dark Aesthetic Background (Color Grading)
    bg_clip = ColorClip(size=(1080, 1920), color=theme["bg"], duration=total_duration)

    # Typography Math Engine (Sync & Bounce)
    words = script.split()
    time_per_word = total_duration / len(words)
    text_clips = []
    current_time = 0.0
    
    for word in words:
        clean_word = "".join(e for e in word if e.isalnum()).lower()
        
        # Word Importance Logic
        if len(clean_word) > 5 or clean_word in POWER_WORDS:
            color = theme["power_color"]
            font_size = 140
        else:
            color = theme["normal_color"]
            font_size = 90
            
        # Creating Bouncy Text Clip
        txt_clip = (TextClip(word, fontsize=font_size, color=color, font='Arial-Bold', method='caption', size=(900, None))
                    .set_position('center')
                    .set_start(current_time)
                    .set_duration(time_per_word)
                    .crossfadein(0.05)) # Smooth Pop-up effect
                    
        text_clips.append(txt_clip)
        current_time += time_per_word

    # Final Render
    print("[+] Assembling Video Elements...")
    final_video = CompositeVideoClip([bg_clip] + text_clips).set_audio(audio_clip)
    
    output_name = "final_tech_viral_video.mp4"
    final_video.write_videofile(output_name, fps=30, codec="libx264", audio_codec="aac")
    print(f"[SUCCESS] Video Rendered: {output_name}")

if __name__ == "__main__":
    build_video()
