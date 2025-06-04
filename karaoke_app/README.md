
# Karaoke Creator

This application automatically creates karaoke videos from audio files by:
- Using Demucs to separate vocals and instruments
- Using Whisper to transcribe the vocals
- Creating a karaoke video with synchronized lyrics

The application supports Russian and other languages, and works on macOS.

## Requirements

- Python 3.9 or higher (recommended: Python 3.10)
- Demucs
- Pydub
- MoviePy
- Whisper
- FFmpeg (for video creation)
- ImageMagick (for image handling)

For macOS, you can install the required dependencies with:
```bash
# Install FFmpeg and ImageMagick using Homebrew
brew install ffmpeg imagemagick

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install wheel (required for some dependencies)
pip install wheel

# Install Python dependencies
pip install -r requirements.txt
```
Note: Tkinter is included in the standard Python installation on macOS, but if you encounter issues with the GUI application, you can install it using:
```bash
brew install python-tk
```

If you encounter issues with the `moviepy` library, try reinstalling it:
```bash
pip uninstall moviepy
pip install moviepy==1.0.3
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/raveismadly/snake.git
   cd karaoke_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application using Python 3.9 or higher:
   ```bash
   python3 cli_karaoke.py path/to/your/audiofile.mp3
   ```

## Usage

1. Prepare an audio file (MP3 or WAV).
2. Run the command-line application with your audio file as input (using Python 3.9 or higher):
   ```bash
   python3 cli_karaoke.py path/to/your/audiofile.mp3
   ```

The output will be saved as `karaoke_{filename}.mp4` in the same directory.

## GUI Application

The application also includes a simple graphical user interface (GUI) that can be used to create karaoke videos.

To run the GUI application (requires a graphical interface and Python 3.9 or higher):
```bash
python3 gui_karaoke.py
```

## License

This project is licensed under the MIT License.
