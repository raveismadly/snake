

from setuptools import setup, find_packages

setup(
    name="karaoke_creator",
    version="0.1.0",
    description="Automatic karaoke creation tool using Demucs and Whisper",
    author="Your Name",
    packages=find_packages(),
    py_modules=['cli_karaoke', 'gui_karaoke'],
    install_requires=[
        "demucs==4.0.1",
        "pydub==0.25.1",
        "moviepy==1.0.3",
        "whisper==1.1.10",
        "Pillow",
        "ffmpeg-python"
    ],
    entry_points={
        'console_scripts': [
            'karaoke-creator=cli_karaoke:main',
        ],
    },
)

