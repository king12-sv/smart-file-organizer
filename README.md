# Smart File Organizer

## About the Project
This is a simple Python project I made to organize files in any folder. It checks the files in the folder and sorts them into subfolders based on their file extensions (like images, documents, etc.).

## Features
- Easy-to-use GUI with `tkinter`
- Automatically sorts files by extension
- Creates folders for each file type
- Keeps a log of all moved files
- Undo button to move files back
- Handles name conflicts and permission issues

## How to Use
1. Run the file `main.py`
2. Click **Select Folder** and choose the folder you want to organize
3. Click **Organize Files**
4. If needed, click **Undo Last Action** to reverse the move

## Requirements
- Python 3
- No extra packages needed (just `tkinter`, which comes with Python)

## Example Before and After

**Before:**
📂MyFolder
├── photo.jpg
├── document.pdf
├── notes.txt  

**After:**
📂MyFolder
├── 📂jpg
│ └── photo.jpg
├── 📂pdf
│ └── document.pdf
├── 📂txt
│ └── notes.txt 

## Files Included
- `main.py` → Main script for the organizer
- `README.md` → This file
- `file_log.json` → Log file (created after organizing)
