import os
import random
import requests
from gtts import gTTS
from moviepy.editor import *
from moviepy.audio.fx.all import audio_loop
from playwright.sync_api import sync_playwright
from duckduckgo_search import DDGS

HF_KEY = os.environ.get("HUGGINGFACE_KEY")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
POWER_WORDS = ["ai", "free", "khatarnak", "secret", "hack", "website", "illegal", "viral", "chatgpt", "ruko", "tool", "crazy"]

# PREMIUM FLAT REEL COLORS
BG_COLORS = [(220, 200, 255), (15, 45, 30), (245, 245, 235), (15, 25, 50)]

def fetch_and_record_website():
    print("[+] Deep Scan: Fetching Assets & Recording 16:9 Screen...")
    assets = {'meme': False, 'audio': False, 'recording': False}
    
    # Meme Hook
    try:
        res = requests.get("https://api.imgflip.com/get_memes", timeout=10).json()
        meme = random.choice(res['data']['memes'][:20])
        req = requests.get(meme['url'], headers=HEADERS, timeout=10)
        if len(req.content) > 1000:
            with open('live_meme.png', 'wb') as f: f.write(req.content)
            assets['meme'] = True
    except: pass

    # Audio Assets
    try:
        bgm_url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/A_minor_tech_loop.ogg"
        pop_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Bloop.ogg"
        bgm_req = requests.get(bgm_url, headers=HEADERS, timeout=10)
        pop_req = requests.get(pop_url, headers=HEADERS, timeout=10)
        if len(bgm_req.content) > 5000:
            with open('live_bgm.ogg', 'wb') as f: f.write(bgm_req.content)
            with open('live_pop.ogg', 'wb') as f: f.write(pop_req.content)
            assets['audio'] = True
    except: pass

    # 16:9 Screen Recording (Playwright)
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

def build_video():
    assets = fetch_and_record_website()
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    audio_elements = [voice_clip]
    valid_audio = False
    
    if assets['audio']:
        try:
            base_bgm = AudioFileClip("live_bgm.ogg").volumex(0.12)
            bgm_clip = audio_loop(base_bgm, duration=total_duration)
            base_pop_sfx = AudioFileClip("live_pop.ogg").volumex(0.6)
            audio_elements.append(bgm_clip)
            valid_audio = True
        except: pass

    visual_elements = []

    # 1. THE BLACK BOX FRAME (Letterbox)
    base_black = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(total_duration)
    visual_elements.append(base_black)

    # 2. THE COLOR CARD AREA (Middle Section)
    color_box_height = 1250 
    y_color_start = (1920 - color_box_height) // 2
    for i in range(int(total_duration // 3.5) + 2):
        c = BG_COLORS[i % len(BG_COLORS)]
        start_time = i * 3.5
        color_clip = (ColorClip(size=(1080, color_box_height), color=c)
                      .set_duration(3.5).set_start(start_time).set_position(('center', y_color_start)))
        visual_elements.append(color_clip)

    # 3. 16:9 VIDEO CARD
    if assets['recording']:
        card_w, card_h = 980, 551 # 16:9 Ratio
        x_p, y_p = (1080 - card_w) // 2, y_color_start + 80
        shadow = ColorClip(size=(card_w, card_h), color=(0,0,0)).set_opacity(0.4).set_position((x_p + 20, y_p + 20)).set_duration(total_duration)
        web_clip = (VideoFileClip("live_web_recording.mp4").volumex(0).loop(duration=total_duration)
                   .resize(width=card_w, height=card_h).set_position((x_p, y_p)).set_duration(total_duration))
        visual_elements.extend([shadow, web_clip])

    # 4. MEME SLIDE HOOK
    if assets['meme']:
        try:
            meme_clip = (ImageClip("live_meme.png").resize(width=550)
                         .set_position(lambda t: ('center', int(min(y_p + card_h - 50, 1920 - 1200*t))))
                         .set_start(0).set_duration(2.8).crossfadeout(0.2))
            visual_elements.append(meme_clip)
        except: pass

    # 5. VIRAL BOUNCE TYPOGRAPHY
    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    text_y_pos = y_p + card_h + 160 
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        color, f_size = ("yellow", 145) if (len(clean) > 5 or clean in POWER_WORDS) else ("white", 115)
        
        if valid_audio and color == "yellow":
            audio_elements.append(base_pop_sfx.set_start(current_time))

        txt_s = TextClip(word, fontsize=f_size, color=color, stroke_color='black', stroke_width=6, font='DejaVuSans-Bold', method='caption', size=(920, None))
        
        # Hyper-Snappy Bounce (0.2s)
        def bouncy_logic(t):
            if t < 0.1: return 0.4 + (0.9 * (t / 0.1)) # 0.4 to 1.3
            elif t < 0.2: return 1.3 - (0.3 * ((t-0.1) / 0.1)) # 1.3 to 1.0
            else: return 1.0

        txt = (txt_s.resize(bouncy_logic).set_position(('center', text_y_pos)).set_start(current_time).set_duration(time_per_word))
        visual_elements.append(txt)
        current_time += time_per_word

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)
    
    print("[+] Rendering 30 FPS Masterpiece...")
    final_video.write_videofile("temp_video.mp4", fps=30, codec="libx264", audio_codec="aac")

    # 1.25x HIGH ENERGY INJECTION
    os.system("ffmpeg -y -i temp_video.mp4 -filter_complex \"[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]\" -map \"[v]\" -map \"[a]\" final_tech_viral_video.mp4")
    print("[SUCCESS] Deep Re-checked Code Executed!")

if __name__ == "__main__":
    build_video()
