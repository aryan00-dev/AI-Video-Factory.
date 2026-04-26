import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_script():
    print("[+] Brain Active: Generating 60-Word Viral Script via Groq Llama-3...")
    
    if not GROQ_API_KEY:
        print("[-] Absolute Error: GROQ_API_KEY not found in environment!")
        exit(1)

    client = Groq(api_key=GROQ_API_KEY)
    
    # Advanced System Prompt for highest retention
    prompt = """
    Write a 50-60 word highly engaging Hindi tech script for an Instagram Reel about a crazy, free, and secret AI tool (e.g., Luma Dream Machine, Qwen, Midjourney, etc). 
    Rules:
    1. Start exactly with the word "Ruko!". 
    2. Use words like "khatarnak", "secret", "dimaag kharab", "free". 
    3. Do not include emojis, hashtags, or bracketed text. Write pure spoken text only.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192", # Lightning fast model
            temperature=0.8
        )
        script = chat_completion.choices[0].message.content.strip()
        
        with open("current_script.txt", "w", encoding="utf-8") as f:
            f.write(script)
            
        print("[SUCCESS] Viral Script Ready.")
        print(f"Script Preview: {script[:50]}...")
    except Exception as e:
        print(f"[-] Groq Script Engine Failed: {e}")
        exit(1)

if __name__ == "__main__":
    generate_script()
