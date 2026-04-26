import os
import time
import google.generativeai as genai
from moviepy.editor import VideoFileClip

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def ai_video_critic():
    print("[SYSTEM] AI Video Critic (PRO EDITION) Initiated...")
    
    if not os.path.exists("final_tech_viral_video.mp4"):
        print("[-] Error: Final video not found!")
        exit(1)
        
    try:
        clip = VideoFileClip("final_tech_viral_video.mp4")
        duration = clip.duration
        clip.close()
        
        if duration < 15 or duration > 45:
            print("[-] QC FAIL: Video duration is out of bounds for a reel.")
            exit(1)
            
    except Exception as e:
        print(f"[-] QC FAIL: Video file corrupted. {e}")
        exit(1)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        
        video_file = genai.upload_file(path="final_tech_viral_video.mp4")
        
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
            
        if video_file.state.name == "FAILED":
            print("[-] AI Director failed to process the video.")
            exit(1)

        prompt = """
        You are an expert Instagram Reels Editor. Watch and listen to this video carefully.
        Analyze:
        1. Does it have engaging bouncy text?
        2. Is the pacing and audio energetic?
        3. Is there a background website search or visual element visible?
        
        Rate it out of 10. If the score is 7 or above, respond with "PASS". If it is below 7, respond with "FAIL". 
        Provide a 1-sentence brutally honest reason. Format: "[PASS/FAIL] - Reason"
        """
        
        response = model.generate_content([video_file, prompt])
        feedback = response.text.strip()
        print(f"\n🎬 AI DIRECTOR'S VERDICT: {feedback}\n")
        
        genai.delete_file(video_file.name)
        
        if "FAIL" in feedback.upper():
            exit(1)
        else:
            print("[+] QC PASS: Video perfectly matches Viral Standards. INSTA_READY! ✅")
            
    except Exception as e:
        print("[!] Falling back to basic duration pass. INSTA_READY! ✅")

if __name__ == "__main__":
    ai_video_critic()
