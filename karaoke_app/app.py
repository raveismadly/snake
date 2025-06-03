

from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', success_message=None, error_message=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return render_template('index.html', error_message="No file part")

    file = request.files['audio_file']
    if file.filename == '':
        return render_template('index.html', error_message="No selected file")

    # Save the uploaded file
    input_path = os.path.join('/app', file.filename)
    file.save(input_path)

    # Run the karaoke creation process
    try:
        result = subprocess.run(
            ["python", "cli_karaoke.py", input_path],
            check=True,
            capture_output=True,
            text=True
        )
        return render_template('index.html', success_message="Karaoke created successfully!")
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to create karaoke: {e.output}"
        return render_template('index.html', error_message=error_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

