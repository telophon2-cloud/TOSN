# TOSN - The Open Source Notepad

A simple, lightweight, and modern text editor designed in a dark terminal style. It is build on Python and Tkinter, making it fast and easy to use for everyone—from kids to developers.

Developed under the **VladisApps** copyright.

## ✨ Features
* **Multi-Format Support:** Easily save your files in standard extensions like `.txt`, `.py`, `.html`, `.json`, or use the signature **`.tosn`** format.
* **Multi-Language UI:** Built-in language switcher supporting English, Русский, Español, Français, Deutsch, and 中文.
* **Persistent Settings:** TOSN automatically remembers your selected language for the next launch.
* **Pro Hotkeys:** Speed up your workflow with built-in shortcuts:
  * `Ctrl + N` - New File
  * `Ctrl + O` - Open File
  * `Ctrl + S` - Save File
  * `Ctrl + Shift + S` - Save As...
  * `Ctrl + L` - Open Language Menu

## 🚀 How to Run (From Source)

1. Clone this repository to your local machine.
2. Make sure you have both `tosn.py` and `locale_storage.py` in the same directory.
3. Run the main file using terminal:
   ```bash
   python3 tosn.py
   ```

## 📦 How to Build Standalone Binary

You can compile TOSN into a single executable file using `PyInstaller`. Run the following command in your project folder:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed tosn.py
```
After the build is complete, you will find your standalone app inside the `dist/` directory.

## 📄 License
This project is open-source and developed by **VladisApps**. All rights reserved © 2026.
