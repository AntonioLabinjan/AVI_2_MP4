import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def convert_avi_to_mp4(avi_file_path, output_name=None):
    directory = os.path.dirname(avi_file_path)

    if output_name is None:
        base_name = os.path.splitext(os.path.basename(avi_file_path))[0]
        output_name = base_name + '.mp4'

    output_path = os.path.join(directory, output_name)

    command = f'ffmpeg -i "{avi_file_path}" -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 "{output_path}"'

    os.system(command)

    return output_path

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVI to MP4 Converter")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # File path
        self.file_path = None

        # UI Elements
        self.label = tk.Label(root, text="Select an AVI file to convert", font=("Arial", 12))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file, width=20)
        self.select_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to MP4", command=self.start_conversion, width=20, state=tk.DISABLED)
        self.convert_button.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

        self.status_label = tk.Label(root, text="", font=("Arial", 10))
        self.status_label.pack()

    def select_file(self):
        filetypes = (('AVI files', '*.avi'), ('All files', '*.*'))
        filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)

        if filename:
            self.file_path = filename
            self.label.config(text=os.path.basename(self.file_path))
            self.convert_button.config(state=tk.NORMAL)
            self.status_label.config(text="Ready to convert")

    def start_conversion(self):
        if self.file_path:
            self.convert_button.config(state=tk.DISABLED)
            self.status_label.config(text="Converting...")
            threading.Thread(target=self.convert_video).start()

    def convert_video(self):
        self.progress["value"] = 0
        self.root.update_idletasks()

        # Start fake progress simulation
        for i in range(0, 90, 5):
            self.progress["value"] = i
            self.root.update_idletasks()
            time.sleep(0.2)  # Adjust speed as needed

        # Actual conversion
        output_path = convert_avi_to_mp4(self.file_path)

        # Complete the progress bar after conversion
        self.progress["value"] = 100
        self.root.update_idletasks()

        self.status_label.config(text="Conversion Completed!")

        # Show message box
        messagebox.showinfo("Done", f"Video converted successfully:\n{output_path}")

        # Reset
        self.label.config(text="Select an AVI file to convert")
        self.convert_button.config(state=tk.DISABLED)
        self.progress["value"] = 0
        self.status_label.config(text="")

if __name__ == "__main__":
    import time
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
