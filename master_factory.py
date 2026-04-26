import os
import random
import glob
import re 
import urllib.parse 
import requests
import PIL.Image

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

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
        if req.status_code == 200 and 'html' not in req.headers.get('Content-Type', '').lower() and 'text' not in req.headers.get('Content-Type', '').lower():
            with open(filename, 'wb') as f: f.write(req.content)
            return True
    except: pass
    return False

def get_vault_asset(pattern):
    files = glob.glob(pattern)
    if files:
        selected = random.choice(files)
        print(f"[+] Vault Engine selected: {selected}")
        return selected
    return None

def fetch_and_record_website():
    print("[+] Deep Scan: Scanning Local Vault & Recording Stealth Screen...")
    assets = {'meme': None, 'bgm': None, 'pop': None, 'type_sfx': False, 'reveal_sfx': False, 'recording': False}
    
    assets['meme'] = get_vault_asset("assets/*.png") or get_vault_asset("assets/*.jpeg") or get_vault_asset("assets/*.jpg")
    assets['bgm'] = get_vault_asset("assets/bgm*.mp3")
    assets['pop'] = get_vault_asset("assets/pop*.mp3")

    if assets['meme']:
        try:
            img = PIL.Image.open(assets['meme']).convert("RGBA")
            img.save("temp_meme.png", format="PNG") 
            assets['meme'] = "temp_meme.png"
        except Exception as e:
            print(f"[-] Image Lock Warning: {e}")

    type_sfx_url = "https://upload.wikimedia.org/wikipedia/commons/2/23/Keyboard_Type.ogg"
    reveal_sfx_url = "https://upload.wikimedia.org/wikipedia/commons/a/aa/A_major_tech_stinger.ogg"
    assets['type_sfx'] = download_audio(type_sfx_url, 'live_type.ogg')
    assets['reveal_sfx'] = download_audio(reveal_sfx_url, 'live_reveal.ogg')

    try:
        with open("current_script.txt", "r", encoding="utf-8") as f:
            script_text = f.read()
        
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"Read this Hindi tech script. Identify the main AI tool being promoted. Return ONLY its official name. Return absolutely nothing else. Script: {script_text}"
        
        tool_name = "AI Tool official" 
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant"
            )
            extracted_output = res.choices[0].message.content.strip()
            tool_name = re.sub(r'[^a-zA-Z0-9\s-]', '', extracted_output).strip()
        except: pass
            
        query = urllib.parse.quote(f"{tool_name} AI tool official website")
        tool_url = f"https://duckduckgo.com/?q={query}"
                
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                record_video_dir="./", 
                record_video_size={"width": 1280, "height": 720}, 
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()
            try:
                page.goto(tool_url, wait_until="domcontentloaded", timeout=15000)
            except: pass 
            
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 400) 
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 200)
            page.wait_for_timeout(1000)
            
            video_path = page.video.path()
            context.close() 
            browser.close()
            os.rename(video_path, 'live_web_recording.mp4')
            assets['recording'] = True
    except Exception as e:
        print(f"[-] Stealth Recording Failed: {e}")
        exit(1)
    return assets

def get_voice(text, filename="audio.mp3"):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
    use_fallback = True
    try:
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        res = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if res.status_code == 200 and ('audio' in res.headers.get('Content-Type', '').lower() or 'mpeg' in res.headers.get('Content-Type', '').lower() or 'flac' in res.headers.get('Content-Type', '').lower()):
            with open(filename, 'wb') as f: f.write(res.content)
            use_fallback = False
    except: pass
    
    if use_fallback:
        gTTS(text=text, lang='hi', slow=False).save(filename)

def build_video():
    assets = fetch_and_record_website()
    with open("current_script.txt", "r", encoding="utf-8") as f:
        script = f.read().strip()
        
    get_voice(script, "audio.mp3")
    voice_clip = AudioFileClip("audio.mp3")
    total_duration = voice_clip.duration
    audio_elements = [voice_clip]
    
    base_pop_sfx = None
    if assets['pop']:
        try:
            base_pop_sfx = AudioFileClip(assets['pop']).volumex(0.8)
        except: pass

    base_type_sfx = None
    if assets['type_sfx']:
        try:
            base_type_sfx = AudioFileClip("live_type.ogg").volumex(1.0).loop()
        except: pass

    visual_elements = []

    CANVAS_SIZE = (1080, 1920)
    REF_FRAME_H = 1300 
    REF_FRAME_Y_START = (CANVAS_SIZE[1] - REF_FRAME_H) // 2 
    WEB_CARD_W = 1060 
    WEB_CARD_H = int(WEB_CARD_W * (9/16)) 

    visual_elements.append(ColorClip(size=CANVAS_SIZE, color=(0, 0, 0)).set_duration(total_duration))

    REVEAL_TIME = 2.8 

    for i in range(int(total_duration // 3.5) + 2):
        c = BG_COLORS[i % len(BG_COLORS)]
        start_time = max(REVEAL_TIME, i * 3.5)
        duration = 3.5
        if start_time + duration > total_duration:
            duration = total_duration - start_time
        if duration <= 0: continue
        
        color_clip = ColorClip(size=(CANVAS_SIZE[0], REF_FRAME_H), color=c)
        def box_slide(t):
            if t < 0.3: return ('center', int(REF_FRAME_Y_START + 500 * (0.3 - t)/0.3))
            return ('center', REF_FRAME_Y_START)

        visual_elements.append(color_clip.set_duration(duration).set_start(start_time).set_position(box_slide))

    if assets['recording']:
        x_card_p = (CANVAS_SIZE[0] - WEB_CARD_W) // 2
        y_card_p_target = REF_FRAME_Y_START + 80 
        
        def card_reveal(t):
            if t < 0.4: return (x_card_p, int(y_card_p_target + 600 * (0.4 - t)/0.4))
            return (x_card_p, y_card_p_target)
        
        shadow_clip = ColorClip(size=(WEB_CARD_W, WEB_CARD_H), color=(0,0,0)).set_opacity(0.4).set_duration(total_duration-REVEAL_TIME).set_start(REVEAL_TIME)
        web_clip_static = (VideoFileClip("live_web_recording.mp4").volumex(0).loop(duration=total_duration-REVEAL_TIME).resize(width=WEB_CARD_W, height=WEB_CARD_H))
                   
        visual_elements.extend([
            shadow_clip.set_position(lambda t: (card_reveal(t)[0]+20, card_reveal(t)[1]+20)),
            web_clip_static.set_duration(total_duration-REVEAL_TIME).set_start(REVEAL_TIME).set_position(card_reveal)
        ])
        
        if assets['reveal_sfx']:
            try:
                audio_elements.append(AudioFileClip("live_reveal.ogg").volumex(1.0).set_start(REVEAL_TIME))
            except: pass

    if assets['meme']:
        try:
            meme_w_hook = 550
            y_p_meme_hook = CANVAS_SIZE[1] // 2 + 100
            meme_x_center_hook = (CANVAS_SIZE[0] - meme_w_hook) // 2
            
            meme_clip = (ImageClip(assets['meme'], has_mask=True)
                         .resize(width=meme_w_hook)
                         .set_position((meme_x_center_hook, y_p_meme_hook))
                         .set_start(0).set_duration(REVEAL_TIME + 0.3)
                         .crossfadeout(0.3))
            visual_elements.append(meme_clip)
        except: pass

    words = script.split()
    time_per_word = total_duration / len(words)
    current_time = 0.0
    text_y_pos_final = REF_FRAME_Y_START + 80 + WEB_CARD_H + 160 
    
    for word in words:
        clean = "".join(e for e in word if e.isalnum()).lower()
        color, f_size = ("yellow", 145) if (len(clean) > 5 or clean in POWER_WORDS) else ("white", 115)
        
        if current_time < REVEAL_TIME:
            txt_position = ('center', CANVAS_SIZE[1] // 2 - 150)
            txt_static = (TextClip(word, fontsize=f_size + 20, color=color, stroke_color='black', stroke_width=6, font='DejaVuSans-Bold', method='caption', size=(1000, None)))
            if base_type_sfx: audio_elements.append(base_type_sfx.set_start(current_time).set_duration(time_per_word))
        else:
            txt_position = ('center', text_y_pos_final)
            txt_static = (TextClip(word, fontsize=f_size, color=color, stroke_color='black', stroke_width=6, font='DejaVuSans-Bold', method='caption', size=(920, None)))
            if base_pop_sfx: audio_elements.append(base_pop_sfx.set_start(current_time))
        
        def bouncy_ease(t):
            t_ease = 0.2
            if t < t_ease:
                return int(txt_static.size[0] * (0.4 + (0.9 * t/t_ease)))
            elif t < 0.3:
                remaining = (t - t_ease) / 0.1
                return int(txt_static.size[0] * (1.3 - (0.3 * remaining)))
            else:
                return int(txt_static.size[0])
        
        visual_elements.append(txt_static.resize(lambda t: bouncy_ease(t) / txt_static.size[0]).set_position(txt_position).set_start(current_time).set_duration(time_per_word))
        current_time += time_per_word
        
    if assets['bgm']:
        try:
            audio_elements.append(audio_loop(AudioFileClip(assets['bgm']).volumex(0.38), duration=total_duration))
        except: pass

    final_audio = CompositeAudioClip(audio_elements)
    final_video = CompositeVideoClip(visual_elements).set_audio(final_audio)
    
    final_video.write_videofile("temp_video.mp4", fps=30, codec="libx264", audio_codec="aac")
    os.system("ffmpeg -y -i temp_video.mp4 -filter_complex \"[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]\" -map \"[v]\" -map \"[a]\" final_tech_viral_video.mp4")

if __name__ == "__main__":
    build_video()
