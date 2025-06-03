
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

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

    # Run the CLI karaoke application
    try:
        result = subprocess.run(
            ["python", "cli_karaoke.py", input_file],
            check=True,
            capture_output=True,
            text=True
        )
        messagebox.showinfo("Success", "Karaoke created successfully!")
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to create karaoke:\n{e.output}"
        if hasattr(e, 'stderr') and e.stderr:
            error_msg += f"\n\nError details:\n{e.stderr}"
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("Karaoke Creator")

# Create and place widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Select an audio file:")
label.pack(side=tk.LEFT)

entry_file = tk.Entry(frame, width=50)
entry_file.pack(side=tk.LEFT)

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

create_button = tk.Button(root, text="Create Karaoke", command=run_karaoke)
create_button.pack(pady=10)

# Run the application
root.mainloop()
