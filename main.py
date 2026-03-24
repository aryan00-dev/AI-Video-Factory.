import os
import requests
import random
import re
from gtts import gTTS

# --- Phase 4 Fix: Super Filter ---
# Chabi ke andar se har tarah ke hidden space aur Enter (\n, \r) ko kaat dega
raw_key = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_KEY = raw_key.replace('\n', '').replace('\r', '').replace(' ', '').strip()

# ==========================================================
# --- ALAG DIMAG MODYULE (The AI Director) ---
# Yahan hum trendy aur viral topics ki lists banayenge
# ==========================================================
def get_viral_context():
    print("AI Director: Choosing a trendy topic...")

    # Categories aur unke trendy topics
    topic_pool = {
        "Health & Anatomy": [
            "Pet ka Tezāb (Acid) aur spicy Samosa ki argument",
            "Dil (Heart) aur Dimag (Brain) ki ladai lifestyle ko lekar",
            "Hair Fall aur Toot-te baalon ka dukh",
            "Pimple appearing before a date",
            "Liver talking about last night's party (alcohol)",
            "Lungs trying to breathe in heavy pollution"
        ],
        "Trending Comedy (Food/Objects)": [
            "Jalebi and Burger comparing their sweetness/spiciness",
            "A Tea (Chai) cup gets jealous of Coffee",
            "A Mobile screen arguing with its owner over usage time",
            "Maggi trying to cook in exactly 2 minutes (and failing)"
        ]
    }

    # Ludo ke dice ki tarah randomly ek category chuno
    chosen_category = random.choice(list(topic_pool.keys()))
    # Phir us category mein se ek topic chuno
    chosen_topic = random.choice(topic_pool[chosen_category])

    print(f"Chosen Category: {chosen_category} | Topic: {chosen_topic}")
    return f"Category: {chosen_category}, Specific Topic: {chosen_topic}"
# ==========================================================


# --- Updated Step 1: Generating Story based on Trendy Topic ---
def generate_story_and_prompt():
    print("Step 1: Asking Llama-3 for a Viral Script...")

    if not NVIDIA_API_KEY:
        print("Error: NVIDIA_API_KEY missing.")
        return None, None

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    # Naye dimag se context lo
    viral_context = get_viral_context()

    # System prompt ko aur strict banaya hai strict format ke liye
    system_instruction = (
        "You are a top viral video creator for Instagram. "
        "Return EXACTLY two lines, no extra text:\n"
        "Line 1: One funny/emotional Hindi dialogue (Latin script like Hinglish) for the character.\n"
        "Line 2: One descriptive English prompt for a 3D video generator (Pixar style) depicting this scene."
    )

    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Write a script about: {viral_context}"}
        ],
        "temperature": 0.7, # Creatvity ke liye
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            full_response = response.json()['choices'][0]['message']['content'].strip()
            print("Llama Raw Response:\n", full_response)

            # Response parsing: 2 lines nikalna
            lines = [line.strip() for line in full_response.split('\n') if line.strip()]

            if len(lines) >= 2:
                # Regular expression se agar Line 1: wagaira likha aaye toh kaat do
                dialogue = re.sub(r'^(Line \d+: |Dialogue: |Hindi: )', '', lines[0])
                video_prompt = re.sub(r'^(Line \d+: |Prompt: |English: )', '', lines[1])
                print(f"Parsed Dialogue: {dialogue}")
                print(f"Parsed Prompt: {video_prompt}")
                return dialogue, video_prompt
            else:
                print("Error: Llama structure unexpected.")
                return None, None
        else:
            print(f"Error in API: {response.text}")
            return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None


# --- Step 2: Generating Audio (TTS) ---
def generate_audio(text):
    print("Step 2: Generating Audio (TTS)...")
    try:
        # Hindi aawaz ke liye lang='hi'
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save("audio.mp3")
        print("Audio saved as audio.mp3")
    except Exception as e:
        print(f"Error in TTS: {e}")

# --- Step 3: Video Generation (Simulation still for testing) ---
def generate_video(prompt):
    print("Step 3: Simulating Video Generation...")
    # Creating a 5-second blank video as placeholder using FFmpeg
    os.system("ffmpeg -y -f lavfi -i color=c=red:s=1280x720:d=5 -c:v libx264 temp_video.mp4")
    print("temp_video.mp4 created.")
    return "temp_video.mp4"

# --- Step 4: Merging Audio and Video using FFmpeg ---
def merge_audio_video(video_file, audio_file):
    print("Step 4: Merging Audio and Video...")
    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -shortest final_video.mp4"
    os.system(command)
    print("Factory Output Ready: final_video.mp4")


# --- Main Engine Loop ---
if __name__ == "__main__":
    if not NVIDIA_API_KEY:
        print("Error: NVIDIA_API_KEY not found. Please set the secret.")
        exit(1)
        
    dialogue, prompt = generate_story_and_prompt()
    
    if dialogue and prompt:
        generate_audio(dialogue)
        vid_file = generate_video(prompt)
        merge_audio_video(vid_file, "audio.mp3")
        print("Automation cycle complete!")
