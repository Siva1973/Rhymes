from moviepy.editor import *
from gtts import gTTS
from pydub import AudioSegment
import os

# ------------------ CONFIG ------------------
LYRICS = """
Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.

When the blazing sun is gone,
When he nothing shines upon,
Then you show your little light,
Twinkle, twinkle, all the night.

Then the traveler in the dark
Thanks you for your tiny spark,
He could not see which way to go,
If you did not twinkle so.
""" * 5  # Repeat to make it ~3 mins

BACKGROUND_MUSIC = "background_music.mp3"  # Place a royalty-free music file in the same folder
OUTPUT_FILE = "baby_rhyme_video.mp4"
LANG = "en"
DURATION = 180  # seconds
# --------------------------------------------

def create_speech(lyrics, filename="lyrics.mp3"):
    tts = gTTS(lyrics, lang=LANG)
    tts.save(filename)
    return filename

def mix_audio(voice_file, music_file, output_file="mixed_audio.mp3", music_volume_dB=-10):
    voice = AudioSegment.from_file(voice_file)
    music = AudioSegment.from_file(music_file).apply_gain(music_volume_dB)

    # Loop background to match voice length
    bg_music = music * (len(voice) // len(music) + 1)
    bg_music = bg_music[:len(voice)]

    mixed = voice.overlay(bg_music)
    mixed.export(output_file, format="mp3")
    return output_file

def create_video(audio_file, lyrics, output_file):
    # Create text clips for each stanza
    clips = []
    lines = lyrics.strip().split('\n\n')
    stanza_duration = DURATION / len(lines)

    for i, stanza in enumerate(lines):
        txt = TextClip(stanza, fontsize=40, color='white', size=(1280, 720), method='caption')
        txt = txt.set_duration(stanza_duration).set_position('center')
        bg = ColorClip(size=(1280, 720), color=(30, 144, 255)).set_duration(stanza_duration)
        clip = CompositeVideoClip([bg, txt])
        clips.append(clip)

    video = concatenate_videoclips(clips)
    audio = AudioFileClip(audio_file)
    final = video.set_audio(audio)
    final.write_videofile(output_file, fps=24)

# -------- Main Logic --------
if not os.path.isfile(BACKGROUND_MUSIC):
    raise FileNotFoundError(f"Background music file '{BACKGROUND_MUSIC}' not found!")

print("Creating speech...")
speech_file = create_speech(LYRICS)

print("Mixing audio...")
mixed_audio_file = mix_audio(speech_file, BACKGROUND_MUSIC)

print("Creating video...")
create_video(mixed_audio_file, LYRICS, OUTPUT_FILE)

print(f"✅ Video created: {OUTPUT_FILE}")
