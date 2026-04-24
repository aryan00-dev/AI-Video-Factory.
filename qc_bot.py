import os
from moviepy.editor import VideoFileClip

def quality_control():
    print("[SYSTEM] QC Bot Initiated...")
    video_file = "final_tech_viral_video.mp4"
    
    if not os.path.exists(video_file):
        print("[-] QC FAIL: Video file missing!")
        exit(1)
        
    clip = VideoFileClip(video_file)
    duration = clip.duration
    size_mb = os.path.getsize(video_file) / (1024 * 1024)
    
    print(f"[INFO] Video Duration: {duration:.2f} seconds")
    
    if duration < 25 or duration > 35:
        print("[-] QC FAIL: Video length is strictly outside the 25-35 seconds Golden Window!")
        exit(1)
        
    if size_mb < 0.5:
        print("[-] QC FAIL: Video file too small.")
        exit(1)
        
    print("[+] QC PASS: Video is mathematically perfect and INSTA_READY! ✅")

if __name__ == "__main__":
    quality_control()
