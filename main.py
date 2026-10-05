#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import json

from locale_storage import LOCALIZATION

class TOSNApp(tk.Tk):
    def __init__(self):
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.config_dir = os.path.dirname(sys.executable)
        else:
            self.config_dir = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(self.config_dir, "tosn_config.json")

        self.lang = self.load_saved_language()
        self.text = LOCALIZATION[self.lang]

        self.geometry("950x570")

        self.bg_color = "#1a1a1a"
        self.text_color = "#f0f0f0"
        self.panel_bg = "#2d2d2d"
        self.btn_bg = "#3e3e3e"
        self.btn_hover = "#007acc"

        self.current_file = None
        self.buttons = {}

        self.create_interface()
        self.update_ui_text()
        self.bind_hotkeys()
        self.check_arguments()

    def load_saved_language(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    saved_lang = config.get("language", "en")
                    if saved_lang in LOCALIZATION:
                        return saved_lang
            except Exception:
                pass
        return "en"

    def save_current_language(self):
        try:
            config = {"language": self.lang}
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def check_arguments(self):
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                self.load_file(file_path)

    def bind_hotkeys(self):
        self.bind("<Control-n>", lambda event: self.new_file())
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-S>", lambda event: self.save_as_file())
        self.bind("<Control-l>", lambda event: self.show_language_menu())

    def create_interface(self):
        self.configure(bg=self.bg_color)

        self.top_bar = tk.Frame(self, bg=self.panel_bg, padx=10, pady=5)
        self.top_bar.pack(fill="x", side="top")

        self.buttons["new"] = self.create_button(self.text["btn_new"], self.new_file)
        self.buttons["open"] = self.create_button(self.text["btn_open"], self.open_file)
        self.buttons["save"] = self.create_button(self.text["btn_save"], self.save_file)
        self.buttons["save_as"] = self.create_button(self.text["btn_save_as"], self.save_as_file)
        self.buttons["about"] = self.create_button(self.text["btn_about"], self.show_about)

        self.lang_btn = self.create_button(self.text["btn_lang"], self.show_language_menu)

        self.textbox = tk.Text(
            self,
            font=("Consolas", 14),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground="white",
            relief="flat",
            bd=10,
            undo=True
        )
        self.textbox.pack(fill="both", expand=True)

        self.status_bar = tk.Label(
            self,
            text="",
            bg="#007acc",
            fg="white",
            font=("Consolas", 11, "bold"),
            height=2
        )
        self.status_bar.pack(fill="x", side="bottom")

    def create_button(self, text, command):
        btn = tk.Button(
            self.top_bar,
            text=text,
            command=command,
            bg=self.btn_bg,
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            activebackground=self.btn_hover,
            activeforeground="white",
            cursor="hand2"
        )
        btn.pack(side="left", padx=4)
        return btn

    def show_language_menu(self):
        menu = tk.Menu(self, tearoff=0, bg=self.panel_bg, fg="white", activebackground=self.btn_hover)
        menu.add_command(label="English", command=lambda: self.change_language("en"))
        menu.add_command(label="Русский", command=lambda: self.change_language("ru"))
        menu.add_command(label="Español", command=lambda: self.change_language("es"))
        menu.add_command(label="Français", command=lambda: self.change_language("fr"))
        menu.add_command(label="Deutsch", command=lambda: self.change_language("de"))
        menu.add_command(label="中文", command=lambda: self.change_language("zh"))
        x = self.lang_btn.winfo_rootx()
        y = self.lang_btn.winfo_rooty() + self.lang_btn.winfo_height()
        menu.post(x, y)

    def change_language(self, lang_code):
        self.lang = lang_code
        self.text = LOCALIZATION[lang_code]
        self.save_current_language()
        self.update_ui_text()

    def update_ui_text(self):
        self.title(self.text["title"])
        self.buttons["new"].configure(text=self.text["btn_new"])
        self.buttons["open"].configure(text=self.text["btn_open"])
        self.buttons["save"].configure(text=self.text["btn_save"])
        self.buttons["save_as"].configure(text=self.text["btn_save_as"])
        self.buttons["about"].configure(text=self.text["btn_about"])
        self.lang_btn.configure(text=self.text["btn_lang"])

        self.my_formats = [
            (f"{self.text['f_tosn']} (*.tosn)", "*.tosn"),
            (f"{self.text['f_py']} (*.py)", "*.py"),
            (f"{self.text['f_html']} (*.html)", "*.html"),
            (f"{self.text['f_txt']} (*.txt)", "*.txt"),
            (f"{self.text['f_json']} (*.json)", "*.json"),
            (f"{self.text['f_all']} (*.*)", "*.*")
        ]

        if self.current_file:
            self.status_bar.configure(text=f"{self.text['status_opened']}{os.path.basename(self.current_file)}")
        else:
            self.status_bar.configure(text=self.text["status_ready"])

    def load_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.textbox.delete("1.0", tk.END)
                self.textbox.insert("1.0", file.read())
            self.current_file = file_path
            self.status_bar.configure(text=f"{self.text['status_opened']}{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror(self.text["msg_err_title"], f"{self.text['msg_err_text']}{e}")

    def new_file(self):
        if messagebox.askyesno(self.text["msg_new_title"], self.text["msg_new_text"]):
            self.textbox.delete("1.0", tk.END)
            self.current_file = None
            self.status_bar.configure(text=self.text["status_new"])

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=self.my_formats)
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.textbox.get("1.0", tk.END).strip())
            self.status_bar.configure(text=f"{self.text['status_saved']}{os.path.basename(self.current_file)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tosn",
            filetypes=self.my_formats
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.textbox.get("1.0", tk.END).strip())
            self.current_file = file_path
            self.status_bar.configure(text=f"{self.text['status_saved']}{os.path.basename(file_path)}")

    def show_about(self):
        messagebox.showinfo(self.text["about_title"], self.text["about_text"])

if __name__ == "__main__":
    app = TOSNApp()
    app.mainloop()
