import requests
import json

def get_script(topic, gemini_key):
    headers = {'Content-Type': 'application/json'}
    
    working_model = "models/gemini-1.5-flash"
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        list_resp = requests.get(list_url).json()
        
        if 'models' in list_resp:
            for m in list_resp['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    working_model = m['name']
                    break
        print(f"🔍 Smart Engine ne yeh model select kiya: {working_model}")
    except Exception as e:
        print(f"⚠️ Auto-detect error, default chalega.")

    url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={gemini_key}"
    
    # Naya Viral Prompt: 30-40 Seconds & Object Conversation/Roast Format
    prompt = f"""Write a highly engaging and funny Hindi voiceover script for an Instagram reel. 
Length: Must be enough for a 30 to 40 seconds voiceover (approximately 70 to 80 words).
Format: It MUST be a funny concept where two everyday things are talking, complaining, or roasting each other (For example: Aloo roasting a Samosa, a Math Book complaining to a Student, or Hair crying about a comb/oil). 
Topic: Make it about '{topic}'. 
Important: Since a single AI voice will read this, DO NOT write speaker names (like Aloo: or Book:). Write it as a continuous funny story, monologue, or dramatic narration.
Also, write a 1-line English prompt to generate a funny, highly detailed, cinematic 4k image showing these two objects.

Format output EXACTLY like this:
HINDI_SCRIPT: [Insert the continuous Hindi dialogue here]
IMAGE_PROMPT: [Insert the English image prompt here]"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'candidates' not in data:
            print(f"❌ Gemini API ERROR RESPONSE: {data}")
            return None, None
            
        text_response = data['candidates'][0]['content']['parts'][0]['text']
        print(f"📝 RAW AI RESPONSE:\n{text_response}\n-------------------")
        
        hindi_script = ""
        image_prompt = ""
        
        for line in text_response.split('\n'):
            clean_line = line.replace('**', '').strip()
            if "HINDI_SCRIPT:" in clean_line:
                hindi_script = clean_line.split("HINDI_SCRIPT:")[-1].strip()
            elif "IMAGE_PROMPT:" in clean_line:
                image_prompt = clean_line.split("IMAGE_PROMPT:")[-1].strip()
                
        if not hindi_script or not image_prompt:
             print("❌ ERROR: Format mismatch. Text theek se nahi nikla.")
                
        return hindi_script, image_prompt
        
    except Exception as e:
        print(f"❌ Brain Engine System Error: {e}")
        return None, None
