

from flask import Flask, request, render_template_string, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>Karaoke Creator</title>
  </head>
  <body>
    <h1>Karaoke Creator</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="audio_file" accept=".mp3,.wav"><br>
      <button type="submit">Create Karaoke</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return "No file part", 400

    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file", 400

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
        return f"Karaoke created successfully!<br><a href='/'>Create another karaoke</a>"
    except subprocess.CalledProcessError as e:
        return f"Failed to create karaoke:<br>{e.output}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
