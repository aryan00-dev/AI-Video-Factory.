import os
import google.generativeai as genai
from duckduckgo_search import DDGS
import feedparser

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[-] Error: GEMINI_API_KEY missing!")
    exit(1)

genai.configure(api_key=API_KEY)

def get_latest_news():
    news_data = ""
    print("[+] Radar Active: Scanning RSS Feeds & Open Web...")
    try:
        feed = feedparser.parse("https://techcrunch.com/category/artificial-intelligence/feed/")
        for entry in feed.entries[:2]:
            news_data += f"- {entry.title}\n"
    except: pass

    try:
        with DDGS() as ddgs:
            results = ddgs.text("new open source AI tools", max_results=2)
            for r in results:
                news_data += f"- {r['title']}\n"
    except: pass
    return news_data

def generate_viral_script(news_data):
    print("[+] Brain Active: Applying Dark Psychology...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Tum ek expert AI Tech Video creator ho.
    News: {news_data}
    Ek 20-second ki Hinglish short video script likho.
    RULES:
    1. Hook humesha FOMO se start ho (e.g., "Agar tum abhi bhi ChatGPT use kar rahe ho...").
    2. Tool ka naam aur "Free" nature highlight karo.
    3. Max 45 words. Sirf spoken text do.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace('*', '').replace('"', '')
    except:
        return "Agar tum abhi bhi purane tools use kar rahe ho, toh tum bohot peeche ho. Yeh naya free AI tool khatarnak hai."

if __name__ == "__main__":
    news = get_latest_news()
    script = generate_viral_script(news)
    with open("current_script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print(f"[SUCCESS] Viral Script Ready: {script}")

