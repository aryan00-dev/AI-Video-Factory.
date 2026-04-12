import requests

def make_image(prompt, hf_key):
    # Naya Router URL + Duniya ka sabse latest FLUX model (100% Free & Active)
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {hf_key}"}
    
    # FLUX ko extra lamba prompt nahi chahiye hota, yeh bohot smart hai
    payload = {"inputs": prompt + ", cinematic lighting, highly detailed, 4k resolution"}
    
    try:
        print("📸 Hugging Face (FLUX Engine) ko photo banane ka order ja raha hai...")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            with open("temp_image.png", "wb") as f:
                f.write(response.content)
            print("✅ 4K Photo successfully ban gayi: temp_image.png")
            return "temp_image.png"
        elif response.status_code == 503:
            print("⏳ Server par model load ho raha hai... 1-2 minute baad GitHub Actions mein dobara 'Run workflow' dabana.")
            return None
        else:
            print(f"❌ Visual Engine Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Visual Engine Crash: {e}")
        return None
