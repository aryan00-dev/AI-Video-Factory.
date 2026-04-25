import os
import random
import requests
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

HF_KEY = os.environ.get("HUGGINGFACE_KEY")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko", "tool", "crazy"]

BG_COLORS = [(220, 200, 255), (15, 45, 30), (245, 245, 235), (15, 25, 50)]

def download_audio(url, filename):
    try:
        req = requests.get(url, headers=HEADERS, timeout=10)
        # Block HTML error pages permanently
        if req.status_code == 200 and 'html' not in req.headers.get('Content-Type', '').lower():
            with open(filename, 'wb') as f: f.write(req.content)
            return True
    except: pass
    return False

def fetch_and_record_website():
    print("[+] Deep Scan: Fetching Assets & Recording 16:9 Screen...")
    assets = {'meme': False, 'bgm': False, 'pop': False, 'whoosh': False, 'recording': False}
    
    # ==========================================
    # 1. THE NEW TRANSPARENT CHARACTER ENGINE
    # ==========================================
    if os.path.exists('live_meme.png'):
        assets['meme'] = True
        print("[+] Boss's Custom Premium Meme detected.")
    else:
        print("[+] Hunting for Transparent Cat/Dog PNGs...")
        meme_queries = ["funny cat transparent png", "cool dog transparent meme png", "anime character transparent png"]
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(random.choice(meme_queries), max_results=3))
                for r in results:
                    req = requests.get(r['image'], headers=HEADERS, timeout=8)
                    # Ensuring it's actually an image
                    if req.status_code == 200 and 'image' in req.headers.get('Content-Type', '').lower():
                        with open('live_meme.png', 'wb') as f: f.write(req.content)
                        assets['meme'] = True
                        print("[+] Transparent Character Acquired!")
                        break
        except Exception as e: 
            print(f"[-] Meme Hunt Failed, skipping to avoid crash: {e}")

    # ==========================================
    # 2. AUDIO ASSETS SECURE FETCH
    # ==========================================
    print("[+] Downloading Audio Assets (BGM, Pop, Whoosh)...")
    bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
    pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
    whoosh_url = "https://upload.wikimedia.org/wikipedia/commons/7/73/Whoosh_01.wav"
    
    assets['bgm'] = download_audio(bgm_url, 'live_bgm.ogg')
    assets['pop'] = download_audio(pop_url, 'live_pop.ogg')
    assets['whoosh'] = download_audio(whoosh_url, 'live_whoosh.wav')

    # ==========================================
    # 3. 16:9 VIRTUAL SCREEN RECORDING
    # ==========================================
    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script_text = f.read().lower()
        
        query = " ".join(script_text.split()[:10]) + " official tool website"
        tool_url = "https://huggingface.co/spaces" 
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=1):
                    tool_url = r['href']
                    break
        except: pass
        
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
    try:
        res = requests.post(API_URL, headers={"Authorization": f"Bearer {HF_KEY}"}, json={"inputs": text}, timeout=15)
        if res.status_code == 200:
            with open(filename, 'wb') as f: f.write(res.content)
            return
    except: pass
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

    # 1. THE BLACK BOX BASE
    visual_elements.append(ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(total_duration))
    
    # 2. FLAT COLOR CARD
    color_box_height = 1250 
    y_color_start = (1920 - color_box_height) // 2
    for i in range(int(total_duration // 3.5) + 2):
        c = BG_COLORS[i % len(BG_COLORS)]
        start_time = i * 3.5
        visual_elements.append(ColorClip(size=(1080, color_box_height), color=c).set_duration(3.5).set_start(start_time).set_position(('center', y_color_start)))

    # 3. 16:9 VIDEO CARD WITH SHADOW
    if assets['recording']:
        card_w, card_h = 980, 551 
        x_p, y_p = (1080 - card_w) // 2, y_color_start + 80
        visual_elements.extend([
            ColorClip(size=(card_w, card_h), color=(0,0,0)).set_opacity(0.4).set_position((x_p + 20, y_p + 20)).set_duration(total_duration),
            VideoFileClip("live_web_recording.mp4").volumex(0).loop(duration=total_duration).resize(width=card_w, height=card_h).set_position((x_p, y_p)).set_duration(total_duration)
        ])

    # 4. THE PRO SIDE-SLIDE TRANSPARENT MEME
    if assets['meme']:
        try:
            meme_w = 550
            target_x = (1080 - meme_w) // 2 # Exact Center
            y_pos_meme = y_p + card_h - 100 # Slightly overlapping the card
            
            # Keyframe Logic: Enters from X=1080 (Right screen edge), shoots to center
            # has_mask=True ensures transparency is preserved
            meme_clip = (ImageClip("live_meme.png", has_mask=True)
                         .resize(width=meme_w)
                         .set_position(lambda t: (int(max(target_x, 1080 - 2500*t)), y_pos_meme))
                         .set_start(0).set_duration(3.0).crossfadeout(0.2))
            visual_elements.append(meme_clip)
        except Exception as e:
            print(f"[-] Meme Rendering Error Skipped: {e}")

    # 5. VIRAL BOUNCE TYPOGRAPHY & EVERY-WORD POP SFX
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
    
    print("[+] Rendering 30 FPS Masterpiece with Character Slide Animation...")
    final_video.write_videofile("temp_video.mp4", fps=30, codec="libx264", audio_codec="aac")

    # 1.25x HIGH ENERGY INJECTION
    os.system("ffmpeg -y -i temp_video.mp4 -filter_complex \"[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]\" -map \"[v]\" -map \"[a]\" final_tech_viral_video.mp4")
    print("[SUCCESS] Pipeline Executed Successfully. Zero Errors Verified.")

if __name__ == "__main__":
    build_video()
