import os, requests, re

def get_script(context, key):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    # Direct instruction for viral script
    instruction = (
        f"Context: {context}. Write a viral Instagram reel script. "
        "Return EXACTLY 2 lines. Line 1: Funny/Emotional Hindi dialogue. "
        "Line 2: Descriptive English prompt for 3D Pixar-style video."
    )
    
    payload = {
        "model": "meta/llama3-70b-instruct",
        "messages": [{"role": "user", "content": instruction}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content'].strip().split('\n')
        dialogue = re.sub(r'^(Line \d+: |Dialogue: )', '', content[0])
        prompt = re.sub(r'^(Line \d+: |Prompt: )', '', content[1])
        return dialogue, prompt
    else:
        print(f"Brain Engine Error: {response.status_code}")
        return None, None
