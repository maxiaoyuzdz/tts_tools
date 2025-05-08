import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
    if file_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(tk.END, file_path)

def select_params_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        params_entry.delete(0, tk.END)
        params_entry.insert(tk.END, file_path)

def run_processing():
    video_file = video_entry.get()
    params_file = params_entry.get()

    if not video_file or not params_file:
        messagebox.showerror("Error", "Both fields must be filled.")
        return

    try:
        subprocess.run(["replace_video_s_audio.exe", video_file, params_file], check=True)
        messagebox.showinfo("Success", "Processing completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Video Audio Replacer")

# Video File Selection
tk.Label(root, text="Select Video (.mp4):").grid(row=0, column=0, padx=10, pady=5)
video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_video_file).grid(row=0, column=2, padx=10, pady=5)

# Params File Selection
tk.Label(root, text="Select Params File (.txt):").grid(row=1, column=0, padx=10, pady=5)
params_entry = tk.Entry(root, width=50)
params_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_params_file).grid(row=1, column=2, padx=10, pady=5)

# Run Button
tk.Button(root, text="Run", command=run_processing, width=20).grid(row=2, column=1, pady=20)

# Start the GUI loop
root.mainloop()