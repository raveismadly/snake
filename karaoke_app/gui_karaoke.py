


import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

# Check Python version
if sys.version_info < (3, 9):
    print("This script requires Python 3.9 or higher")
    sys.exit(1)

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav"), ("All files", "*.*")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def run_karaoke():
    input_file = entry_file.get()
    if not input_file or not os.path.exists(input_file):
        messagebox.showerror("Error", "Please select a valid audio file")
        return

    try:
        subprocess.run(
            ["python", "cli_karaoke.py", input_file],
            check=True,
            capture_output=True,
            text=True
        )
        messagebox.showinfo("Success", "Karaoke created successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create karaoke:\n{e.output}")

# Create the main window
root = tk.Tk()
root.title("Karaoke Creator")

# Create and place widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Select an audio file:")
label.grid(row=0, column=0, padx=5, pady=5)

entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=0, column=1, padx=5, pady=5)

browse_btn = tk.Button(frame, text="Browse", command=browse_file)
browse_btn.grid(row=0, column=2, padx=5, pady=5)

create_btn = tk.Button(frame, text="Create Karaoke", command=run_karaoke)
create_btn.grid(row=1, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()

