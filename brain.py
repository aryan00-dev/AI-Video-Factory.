import requests
import json

def get_script(topic, gemini_key):
    # Gemini API URL updated to the working Flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"Write a short, funny 2-line Hindi voiceover script about '{topic}' for an Instagram reel. Also, write a 1-line English prompt to generate a highly detailed, realistic, cinematic 4k image matching the topic. Format output EXACTLY like this:\nHINDI_SCRIPT: [Hindi text]\nIMAGE_PROMPT: [English prompt]"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # Super Loudspeaker: Agar Gemini error dega toh exact reason print karega
        if 'candidates' not in data:
            print(f"❌ Gemini API ERROR RESPONSE: {data}")
            return None, None
            
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        
        hindi_script = ""
        image_prompt = ""
        
        for line in text_response.split('\n'):
            if line.startswith("HINDI_SCRIPT:"):
                hindi_script = line.replace("HINDI_SCRIPT:", "").strip()
            elif line.startswith("IMAGE_PROMPT:"):
                image_prompt = line.replace("IMAGE_PROMPT:", "").strip()
                
        return hindi_script, image_prompt
        
    except Exception as e:
        print(f"❌ Brain Engine System Error: {e}")
        return None, None
