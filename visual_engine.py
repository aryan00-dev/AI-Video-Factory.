import fal_client, requests

def make_video(prompt):
    print("Generating 3D Video via Fal.ai (Luma)...")
    try:
        handler = fal_client.submit(
            "fal-ai/luma-dream-machine",
            arguments={"prompt": prompt, "aspect_ratio": "9:16"}
        )
        url = handler.get()['video']['url']
        vid_data = requests.get(url).content
        with open("temp_video.mp4", "wb") as f:
            f.write(vid_data)
        return "temp_video.mp4"
    except Exception as e:
        print(f"Visual Engine Error: {e}")
        return None

