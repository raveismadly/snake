
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import moviepy.editor as mp
import demucs.separate
import whisper

class KaraokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Karaoke Creator")

        self.create_widgets()

    def create_widgets(self):
        self.install_button = tk.Button(self.root, text="Install Dependencies", command=self.install_dependencies)
        self.install_button.pack(pady=10)

        self.select_file_button = tk.Button(self.root, text="Select Audio File", command=self.select_audio_file)
        self.select_file_button.pack(pady=10)

        self.process_button = tk.Button(self.root, text="Create Karaoke", command=self.create_karaoke, state=tk.DISABLED)
        self.process_button.pack(pady=10)

        self.selected_file_label = tk.Label(self.root, text="No file selected")
        self.selected_file_label.pack(pady=10)

    def install_dependencies(self):
        try:
            subprocess.check_call([sys.executable, "setup.py"])
            messagebox.showinfo("Success", "Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install dependencies")

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.selected_file = file_path
            self.selected_file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.process_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Warning", "No file selected")

    def create_karaoke(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "No file selected")
            return

        try:
            # Separate vocals and instruments
            self.separate_audio()

            # Transcribe lyrics using Whisper
            transcript = self.transcribe_vocals()

            # Create karaoke video
            self.create_video(transcript)

            messagebox.showinfo("Success", "Karaoke created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create karaoke: {str(e)}")

    def separate_audio(self):
        print("Separating vocals and instruments...")
        # Create output directory
        output_dir = f"separated/{os.path.splitext(os.path.basename(self.selected_file))[0]}"
        os.makedirs(output_dir, exist_ok=True)

        # Use Demucs to separate audio
        demucs.separate.main([
            '--two-stems=vocals',
            '--output', output_dir,
            self.selected_file
        ])

        # Rename files to match expected format
        vocals_path = os.path.join(output_dir, 'vocals.wav')
        accompaniment_path = os.path.join(output_dir, 'no_vocals.wav')

        if not os.path.exists(vocals_path):
            raise FileNotFoundError(f"Vocals file not found at {vocals_path}")

        if os.path.exists(accompaniment_path):
            # Rename to match expected format
            os.rename(accompaniment_path, os.path.join(output_dir, 'accompaniment.wav'))

    def transcribe_vocals(self):
        print("Transcribing vocals...")
        model = whisper.load_model("base")
        result = model.transcribe("separated/{}/vocals.wav".format(os.path.splitext(os.path.basename(self.selected_file))[0]))

        return result["text"]

    def create_video(self, lyrics):
        print("Creating karaoke video...")
        # Load instrumental audio
        instrumental_path = "separated/{}/accompaniment.wav".format(os.path.splitext(os.path.basename(self.selected_file))[0])
        audio = AudioSegment.from_wav(instrumental_path)

        # Create a video with the lyrics
        image = mp.ImageClip("lyrics_background.png")
        video = image.set_duration(audio.duration_seconds)
        audio_clip = mp.AudioFileClip(instrumental_path)

        # Add text to video
        txt_clip = (mp.TextClip(lyrics, fontsize=24, color='white')
                    .set_pos('center')
                    .set_duration(audio.duration_seconds))

        final = mp.CompositeVideoClip([video, txt_clip], size=video.size)
        final = final.set_audio(audio_clip)

        output_path = f"karaoke_{os.path.basename(self.selected_file)}.mp4"
        final.write_videofile(output_path, codec='libx264', fps=24)

        print(f"Karaoke video saved to {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KaraokeApp(root)
    root.mainloop()
