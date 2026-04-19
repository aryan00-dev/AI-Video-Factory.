import os
import time
import requests
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import *
import urllib.request

# API Keys
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

def create_video():
    print("[SYSTEM] Master Factory Initiated...")
    
    # 1. Read Topic
    try:
        with open("current_topic.txt", "r") as f:
            topic = f.read().strip()
    except:
        topic = "A smartphone roasting a classic Nokia 3310"
    
    print(f"[+] Topic Loaded: {topic}")

    # 2. Gemini Viral Script (Hindi/Hinglish)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Write a fast-paced, highly engaging 20-second short video script roasting on the topic: '{topic}'. Use Hinglish. Make it punchy. Only give the spoken text, no brackets or visual instructions. Max 40 words."
    response = model.generate_content(prompt)
    script_text = response.text.strip().replace('*', '').replace('"', '')
    print(f"[+] Script Generated: {script_text}")

    # 3. Voice Engine (gTTS)
    print("[+] Generating Audio...")
    tts = gTTS(text=script_text, lang='hi', slow=False)
    tts.save("audio.mp3")
    
    # Load Audio in MoviePy
    audio_clip = AudioFileClip("audio.mp3")
    duration = audio_clip.duration

    # 4. Background Engine (Fail-safe solid dark aesthetic)
    print("[+] Generating Samachar Style Background...")
    # Using a solid dark grey/black background for typography pop
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 15), duration=duration)

    # 5. Kinetic Typography Engine (Math-based Sync for 100% Fail-Proof Render)
    print("[+] Generating Typography overlays...")
    words = script_text.split()
    time_per_word = duration / len(words)
    
    text_clips = []
    current_time = 0.0
    
    for i, word in enumerate(words):
        # Samachar Style Logic: Emphasize big words with Red, normal words with White
        if len(word) > 5 or i % 4 == 0:
            txt_color = 'yellow'
            fontsize = 110
        else:
            txt_color = 'white'
            fontsize = 90
            
        txt_clip = (TextClip(word, fontsize=fontsize, color=txt_color, font='Arial-Bold', method='caption', size=(900, None))
                    .set_position('center')
                    .set_start(current_time)
                    .set_duration(time_per_word))
        
        text_clips.append(txt_clip)
        current_time += time_per_word

    # 6. Final Assembly (Merging everything)
    print("[+] Assembling Final Video...")
    final_video = CompositeVideoClip([bg_clip] + text_clips)
    final_video = final_video.set_audio(audio_clip)
    
    # 7. Render Output
    output_filename = "final_viral_video.mp4"
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    
    print(f"[SUCCESS] Video successfully generated and saved as {output_filename}")

if __name__ == "__main__":
    create_video()
