import tkinter as tk
from tkinter import scrolledtext, Toplevel
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_window = None
        self.log_text = None

    def show_log_window(self):
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = Toplevel()
            self.log_window.title("Log Output")
            self.log_window.geometry("600x400")
            self.log_window.configure(bg="#eaeaea")
            self.log_text = scrolledtext.ScrolledText(self.log_window, width=80, height=20, bg="#f9f9f9", fg="#333333")
            self.log_text.pack(fill=tk.BOTH, expand=True)

        self.log_window.deiconify()

    def log_message(self, message):
        if self.log_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {message}"
            self.log_text.insert(tk.END, log_entry + "\n")
            self.log_text.see(tk.END)
