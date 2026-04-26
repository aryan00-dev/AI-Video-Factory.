import os
import random
import requests
import re 
import PIL.Image

# ==========================================
# THE PILLOW 10.0 CRASH FIX (MONKEY PATCH)
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
# ==========================================

from gtts import gTTS
from moviepy.editor import *
from moviepy.audio.fx.all import audio_loop
from playwright.sync_api import sync_playwright
from duckduckgo_search import DDGS
from groq import Groq 

HF_KEY = os.environ.get("HUGGINGFACE_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko", "tool", "crazy", "dimaag"]

BG_COLORS = [(220, 200, 255), (15, 45, 30), (245, 245, 235), (15, 25, 50)]

def download_audio(url, filename):
    try:
        req = requests.get(url, headers=HEADERS, timeout=10)
        # STRICT CHECK: Reject HTML or Text garbage
        if req.status_code == 200 and 'html' not in req.headers.get('Content-Type', '').lower() and 'text' not in req.headers.get('Content-Type', '').lower():
            with open(filename, 'wb') as f: f.write(req.content)
            return True
    except: pass
    return False

def fetch_and_record_website():
    print("[+] Deep Scan: Fetching Assets & Recording 16:9 Screen...")
    assets = {'meme': False, 'bgm': False, 'pop': False, 'whoosh': False, 'recording': False}
    
    # 1. MEME ENGINE (With Fake PNG Shield)
    if os.path.exists('live_meme.png'):
        assets['meme'] = True
        print("[+] Boss's Custom Premium Meme detected.")
    else:
        print("[+] Hunting for Transparent PNG...")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images("funny cat transparent png", max_results=2))
                for r in results:
                    req = requests.get(r['image'], headers=HEADERS, timeout=8)
                    if req.status_code == 200 and 'image' in req.headers.get('Content-Type', '').lower():
                        with open('live_meme.png', 'wb') as f: f.write(req.content)
                        assets['meme'] = True
                        break
        except: pass
        
        if not assets['meme']:
            try:
                fallback_png = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/500px-SNice.svg.png"
                req = requests.get(fallback_png, headers=HEADERS)
                if req.status_code == 200:
                    with open('live_meme.png', 'wb') as f: f.write(req.content)
                    assets['meme'] = True
            except: pass

    # THE FAKE PNG BOMB SHIELD: Forcing strict RGBA transparent format
    if assets['meme']:
        try:
            img = PIL.Image.open('live_meme.png')
            img = img.convert("RGBA")
            img.save('live_meme.png', format="PNG")
        except Exception as e:
            print(f"[-] Image Lock Warning: {e}")

    # 2. AUDIO ASSETS
    print("[+] Downloading Audio Assets...")
    bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
    pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
    whoosh_url = "https://upload.wikimedia.org/wikipedia/commons/7/73/Whoosh_01.wav"
    
    assets['bgm'] = download_audio(bgm_url, 'live_bgm.ogg')
    assets['pop'] = download_audio(pop_url, 'live_pop.ogg')
    assets['whoosh'] = download_audio(whoosh_url, 'live_whoosh.wav')

    # 3. AI-POWERED EXACT URL FINDER (WITH REGEX SHIELD)
    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script_text = f.read()
        
        print("[+] Asking Groq AI for exact tool URL...")
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"Read this Hindi tech script. Identify the main AI tool being promoted. Return ONLY its official website URL (e.g. https://qwen.ai). Return absolutely nothing else. Script: {script_text}"
        
        tool_url = "https://www.google.com" 
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192"
            )
            raw_ai_output = res.choices[0].message.content.strip()
            
            url_match = re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_ai_output)
            if url_match:
                tool_url = url_match.group(0)
            else:
                tool_url = f"https://www.google.com/search?q={raw_ai_output}"
                
        except Exception as e:
            print(f"[-] AI Extractor Failed: {e}")
            
        print(f"[+] Recording Exact Target: {tool_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(record_video_dir="./", record_video_size={"width": 1280, "height": 720}, viewport={"width": 1280, "height": 720})
            page = context.new_page()
            try:
                page.goto(tool_url, wait_until="load", timeout=15000)
            except: pass 
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, -200)
            page.wait_for_timeout(1000)
            video_path = page.video.path()
            context.close() 
            browser.close()
            os.rename(video_path, 'live_web_recording.mp4')
            assets['recording'] = True
    except Exception as e:
        print(f"[-] Recording Failed: {e}")
        exit(1)
    return assets

def get_voice(text, filename="audio.mp3"):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    use_fallback = True
    try:
        res = requests.post(API_URL, headers={"Authorization": f"Bearer {HF_KEY}"}, json={"inputs": text}, timeout=15)
        # THE AUDIO CRASH FIX: Only process if it's an actual audio stream
        if res.status_code == 200 and ('audio' in res.headers.get('Content-Type', '').lower() or 'mpeg' in res.headers.get('Content-Type', '').lower() or 'flac' in res.headers.get('Content-Type', '').lower()):
            with open(filename, 'wb') as f: f.write(res.content)
            use_fallback = False
    except: pass
    
    if use_fallback:
        print("[-] HF API Audio failed/returned text. Engaging gTTS Fallback.")
        gTTS(text=text, lang='hi', slow=False).save(filename)

# ==========================================
# THE VISUAL MASTERPIECE EDITOR
# ==========================================
def build_video():
    assets = fetch_and_record_website()
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    audio_elements = [voice_clip]
    
    if assets['bgm']:
        try:
            base_bgm = AudioFileClip("live_bgm.ogg").volumex(0.35)
            audio_elements.append(audio_loop(base_bgm, duration=total_duration))
        except: pass

    if assets['whoosh']:
        try:
            audio_elements.append(AudioFileClip("live_whoosh.wav").volumex(1.0).set_start(0.0))
        except: pass

    base_pop_sfx = None
    if assets['pop']:
        try:
            base_pop_sfx = AudioFileClip("live_pop.ogg").volumex(0.8)
        except: pass

    visual_elements = []

    visual_elements.append(ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(total_duration))
    
    color_box_height = 1250 
    y_color_start = (1920 - color_box_height) // 2
    for i in range(int(total_duration // 3.5) + 2):
        c = BG_COLORS[i % len(BG_COLORS)]
        start_time = i * 3.5
        visual_elements.append(ColorClip(size=(1080, color_box_height), color=c).set_duration(3.5).set_start(start_time).set_position(('center', y_color_start)))

    if assets['recording']:
        card_w, card_h = 980, 551 
        x_p, y_p = (1080 - card_w) // 2, y_color_start + 80
        visual_elements.extend([
            ColorClip(size=(card_w, card_h), color=(0,0,0)).set_opacity(0.4).set_position((x_p + 20, y_p + 20)).set_duration(total_duration),
            VideoFileClip("live_web_recording.mp4").volumex(0).loop(duration=total_duration).resize(width=card_w, height=card_h).set_position((x_p, y_p)).set_duration(total_duration)
        ])

    if assets['meme']:
        try:
            meme_w = 400
            target_x = (1080 - meme_w) // 2 
            y_pos_meme = y_p + card_h - 100 
            
            meme_clip = (ImageClip("live_meme.png", has_mask=True)
                         .resize(width=meme_w)
                         .set_position(lambda t: (int(max(target_x, 1080 - 2500*t)), y_pos_meme))
                         .set_start(0).set_duration(3.0).crossfadeout(0.2))
            visual_elements.append(meme_clip)
        except Exception as e:
            print(f"[-] Meme Skipped: {e}")

    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    text_y_pos = y_p + card_h + 160 
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        color, f_size = ("yellow", 145) if (len(clean) > 5 or clean in POWER_WORDS) else ("white", 115)
        
        if base_pop_sfx is not None:
            audio_elements.append(base_pop_sfx.set_start(current_time))

        txt_s = TextClip(word, fontsize=f_size, color=color, stroke_color='black', stroke_width=6, font='DejaVuSans-Bold', method='caption', size=(920, None))
        
        def bouncy_logic(t):
            if t < 0.1: return 0.4 + (0.9 * (t / 0.1)) 
            elif t < 0.2: return 1.3 - (0.3 * ((t-0.1) / 0.1)) 
            else: return 1.0

        visual_elements.append(txt_s.resize(bouncy_logic).set_position(('center', text_y_pos)).set_start(current_time).set_duration(time_per_word))
        current_time += time_per_word

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)
    
    print("[+] Rendering 30 FPS Masterpiece...")
    final_video.write_videofile("temp_video.mp4", fps=30, codec="libx264", audio_codec="aac")

    os.system("ffmpeg -y -i temp_video.mp4 -filter_complex \"[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]\" -map \"[v]\" -map \"[a]\" final_tech_viral_video.mp4")
    print("[SUCCESS] Deep Checked Pipeline Executed Perfectly.")

if __name__ == "__main__":
    build_video()
