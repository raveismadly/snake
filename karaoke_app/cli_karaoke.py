

import os
import sys
import argparse
from pydub import AudioSegment
import moviepy.editor as mp
import demucs.separate
import whisper

# Import os again to ensure it's available in all scopes
import os as os_imported

def separate_audio(input_file):
    print("Separating vocals and instruments...")
    # Create output directory
    output_dir = f"separated/{os_imported.path.splitext(os_imported.path.basename(input_file))[0]}"
    os_imported.makedirs(output_dir, exist_ok=True)

    # Use Demucs to separate audio
    demucs.separate.main([
        '--two-stems', 'vocals',
        '-o', output_dir,
        input_file
    ])

    # Find the correct path to the separated files
    demucs_output_dir = os_imported.path.join(output_dir, 'htdemucs')
    vocals_path = os_imported.path.join(demucs_output_dir, 'vocals.wav')

    if not os_imported.path.exists(vocals_path):
        # Try to find the vocals in the expected directory structure
        found = False
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if 'vocals' in file.lower() and file.endswith('.wav'):
                    vocals_path = os_imported.path.join(root, file)
                    found = True
                    break
            if found:
                break

        if not os_imported.path.exists(vocals_path):
            raise FileNotFoundError("Could not find vocals file")

    # Find accompaniment
    accompaniment_path = os_imported.path.join(demucs_output_dir, 'no_vocals.wav')
    if not os_imported.path.exists(accompaniment_path):
        # Try to find the accompaniment in the expected directory structure
        found = False
        for root, dirs, files in os_imported.walk(output_dir):
            for file in files:
                if 'no_vocals' in file.lower() and file.endswith('.wav'):
                    accompaniment_path = os_imported.path.join(root, file)
                    found = True
                    break
            if found:
                break

        if not os_imported.path.exists(accompaniment_path):
            raise FileNotFoundError("Could not find accompaniment file")

    # Copy files to output_dir for easier access
    os_imported.rename(vocals_path, os_imported.path.join(output_dir, 'vocals.wav'))
    os_imported.rename(accompaniment_path, os_imported.path.join(output_dir, 'accompaniment.wav'))

    return output_dir

def transcribe_vocals(output_dir):
    print("Transcribing vocals...")
    import whisper

    # Load the model
    model = whisper.load_model("base")

    # Transcribe the audio file
    audio_path = os_imported.path.join(output_dir, 'vocals.wav')
    result = model.transcribe(audio_path)

    return result["text"]

def create_video(lyrics, output_dir, input_file):
    print("Creating karaoke video...")
    # Load instrumental audio
    instrumental_path = os_imported.path.join(output_dir, 'accompaniment.wav')
    audio = AudioSegment.from_wav(instrumental_path)

    # Create a video with the lyrics
    try:
        import moviepy.video.io.ImageSequenceClip
        from PIL import Image

        # Use the background image for lyrics
        background_path = "lyrics_background.png"

        if not os_imported.path.exists(background_path):
            # Create a simple background image
            img = Image.new('RGB', (1280, 720), color='black')
            img.save(background_path)
        else:
            img = Image.open(background_path)

        # Draw the text on the image
        from PIL import ImageDraw, ImageFont

        try:
            # Try to use a font that supports Russian
            from PIL import ImageFont
            try:
                # Try to use a system font that supports Cyrillic
                import os
                if os_imported.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
                    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            draw = ImageDraw.Draw(img)
            w, h = draw.textbbox((0, 0), lyrics, font=font)[2:4]
            draw.text(((1280-w)/2, (720-h)/2), lyrics, fill="white", font=font)

            # Save the image
            img_path = "lyrics_image.png"
            img.save(img_path)

            # Create a video from the image
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip([img_path], fps=1)
            clip = clip.set_duration(audio.duration_seconds)

            # Add audio
            audio_clip = mp.AudioFileClip(instrumental_path)
            final = clip.set_audio(audio_clip)


            # Use a better filename for the output
            input_filename = os_imported.path.basename(input_file)
            output_filename = f"karaoke_{os_imported.path.splitext(input_filename)[0]}.mp4"

            output_path = output_filename
            final.write_videofile(output_path, codec='libx264', fps=1)

            print(f"Karaoke video saved to {output_path}")
        except Exception as e:
            print(f"Error creating image: {str(e)}")
            raise

    except Exception as e:
        print(f"Error creating video: {str(e)}")
        raise

def main(input_file):
    try:
        # Separate vocals and instruments
        output_dir = separate_audio(input_file)

        # Transcribe lyrics using Whisper
        transcript = transcribe_vocals(output_dir)

        # Create karaoke video
        create_video(transcript, output_dir, args.input_file)

        print("Karaoke created successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Karaoke Creator")
    parser.add_argument("input_file", help="Input audio file (MP3 or WAV)")
    args = parser.parse_args()

    try:
        main(args.input_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

