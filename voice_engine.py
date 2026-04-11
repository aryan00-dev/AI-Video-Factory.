from gtts import gTTS

def make_audio(text, filename="audio.mp3"):
    print("Generating Hindi Voiceover...")
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename

