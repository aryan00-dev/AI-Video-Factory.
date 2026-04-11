import os
from brain import get_script
from voice_engine import make_audio
from visual_engine import make_video

# Super Filter: Hidden spaces aur enters (\n, \r) ko apne aap hata dega
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY", "").replace('\n', '').replace('\r', '').replace(' ', '').strip()
FAL_KEY = os.environ.get("FAL_KEY", "").replace('\n', '').replace('\r', '').replace(' ', '').strip()

def start_factory():
    print("🚀 AI Video Factory chalu ho rahi hai...")
    
    # Topic decide karna
    topic = "Pet ka acid aur spicy samosa ki funny ladai"

    # 1. Brain Engine (NVIDIA Llama-3)
    print("Step 1: Script likhi ja rahi hai...")
    hindi_text, video_prompt = get_script(topic, NVIDIA_KEY)
    if not hindi_text: 
        print("❌ Script nahi bani. Code ruk gaya.")
        return

    # 2. Voice Engine (gTTS)
    print(f"Step 2: Aawaz ban rahi hai is dialogue par: {hindi_text}")
    audio_file = make_audio(hindi_text)

    # 3. Visual Engine (Fal.ai / Luma)
    print("Step 3: 3D Video ban rahi hai (isme 1-2 minute lagenge)...")
    video_file = make_video(video_prompt)
    if not video_file: 
        print("❌ Video nahi bani. Code ruk gaya.")
        return

    # 4. Final Editor (FFmpeg)
    print("Step 4: Final Editing (Audio aur Video ko joda ja raha hai)...")
    os.system(f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4")
    print("🔥 Factory Success! final_video.mp4 taiyar hai.")

if __name__ == "__main__":
    # Security Check: Code shuru hone se pehle check karega ki dono chabiyan mili ya nahi
    if not NVIDIA_KEY or not FAL_KEY:
        print("❌ ERROR: API Keys GitHub Secrets mein theek se nahi mili. GitHub Settings check karo!")
    else:
        start_factory()
