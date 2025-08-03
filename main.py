import os
import shutil
import time
import json
from tkinter import filedialog, messagebox, Tk, Button, Label
from datetime import datetime


class Logger:
    def __init__(self, log_file='file_log.json'):
        self.log_file = log_file
        self.log_data = []

    def log(self, source, destination):
        entry = {
            'source': source,
            'destination': destination,
            'timestamp': datetime.now().isoformat()
        }
        self.log_data.append(entry)
        self._save_log()

    def _save_log(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.log_data, f, indent=4)

    def load_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.log_data = json.load(f)

    def get_last_actions(self):
        return reversed(self.log_data)


class UndoManager:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.logger.load_log()

    def undo(self):
        for entry in self.logger.get_last_actions():
            try:
                shutil.move(entry['destination'], entry['source'])
                print(f"Moved back {entry['destination']} -> {entry['source']}")
            except Exception as e:
                print(f"Undo failed: {e}")
        os.remove(self.logger.log_file)  # Clear log after undo


class FileOrganizer:
    def __init__(self, folder_path, logger: Logger):
        self.folder_path = folder_path
        self.logger = logger

    def organize(self):
        for filename in os.listdir(self.folder_path):
            source_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(source_path):
                ext = os.path.splitext(filename)[1][1:] or "no_extension"
                dest_folder = os.path.join(self.folder_path, ext)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, filename)

                # Avoid name conflicts
                if os.path.exists(dest_path):
                    base, extn = os.path.splitext(filename)
                    dest_path = os.path.join(dest_folder, f"{base}_{int(time.time())}{extn}")

                try:
                    shutil.move(source_path, dest_path)
                    self.logger.log(source_path, dest_path)
                    print(f"Moved: {filename} -> {dest_path}")
                except PermissionError:
                    print(f"Permission denied for file: {filename}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")


class FileOrganizerGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Smart File Organizer")
        self.window.geometry("400x200")
        self.folder_path = ""
        self.logger = Logger()

        self.label = Label(self.window, text="Select a folder to organize")
        self.label.pack(pady=10)

        self.select_button = Button(self.window, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.organize_button = Button(self.window, text="Organize Files", command=self.organize_files)
        self.organize_button.pack(pady=5)

        self.undo_button = Button(self.window, text="Undo Last Action", command=self.undo_last)
        self.undo_button.pack(pady=5)

        self.quit_button = Button(self.window, text="Quit", command=self.window.quit)
        self.quit_button.pack(pady=5)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.label.config(text=f"Selected: {self.folder_path}")

    def organize_files(self):
        if not self.folder_path:
            messagebox.showerror("Error", "No folder selected.")
            return
        organizer = FileOrganizer(self.folder_path, self.logger)
        organizer.organize()
        messagebox.showinfo("Done", "Files organized successfully.")

    def undo_last(self):
        undo_manager = UndoManager(self.logger)
        undo_manager.undo()
        messagebox.showinfo("Undo", "Undo completed.")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = FileOrganizerGUI()
    gui.run()
