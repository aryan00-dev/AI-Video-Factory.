import os
from brain import get_script
from voice_engine import make_audio
from visual_engine import make_image

# Super Filter: Chabiyon mein space error ko rokne ke liye
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").replace('\n', '').replace('\r', '').replace(' ', '').strip()
HF_KEY = os.environ.get("HUGGINGFACE_KEY", "").replace('\n', '').replace('\r', '').replace(' ', '').strip()

def start_factory():
    print("🚀 AI Video Factory (100% Free Edition) chalu ho rahi hai...")
    
    # Topic (Aage chalkar isko manager.py control karega)
    topic = "Hacker aur AI ki khatarnak ladai"
    
    # Step 1: Brain (Gemini)
    print("Step 1: Gemini se script aur prompt likhwaya ja raha hai...")
    hindi_text, image_prompt = get_script(topic, GEMINI_KEY)
    if not hindi_text or not image_prompt: return
    print(f"📝 Script: {hindi_text}")

    # Step 2: Voice (gTTS)
    print("Step 2: Aawaz ban rahi hai...")
    audio_file = make_audio(hindi_text) # audio.mp3 return karega

    # Step 3: Visuals (Hugging Face)
    print("Step 3: 4K Photo ban rahi hai...")
    image_file = make_image(image_prompt, HF_KEY)
    if not image_file: return

    # Step 4: The Zoom Magic (FFmpeg)
    print("Step 4: Final Editing (Zoom Effect aur Audio jodi ja rahi hai)...")
    # FFmpeg ki command jo photo ko dheere-dheere zoom karegi
    ffmpeg_command = f"ffmpeg -y -loop 1 -i {image_file} -i {audio_file} -vf \"zoompan=z='min(zoom+0.0015,1.5)':d=500\" -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest final_video.mp4"
    os.system(ffmpeg_command)
    
    print("🔥 Factory Success! Tumhara 'Brahmastra' video final_video.mp4 taiyar hai.")

if __name__ == "__main__":
    # Security Check
    if not GEMINI_KEY or not HF_KEY:
        print("❌ ERROR: Gemini ya Hugging Face ki chabi nahi mili!")
    else:
        start_factory()
