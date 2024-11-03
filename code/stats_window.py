import tkinter as tk
from tkinter import Toplevel

class StatisticsWindow:
    def __init__(self):
        self.stats_window = None
        self.active_label = None
        self.inactive_label = None

    def show_stats_window(self):
        if self.stats_window is None or not self.stats_window.winfo_exists():
            self.stats_window = Toplevel()
            self.stats_window.title("Port Statistics")
            self.stats_window.geometry("300x150")
            self.stats_window.configure(bg="#eaeaea")
            self.active_label = tk.Label(self.stats_window, text="Active Ports: 0", font=("Arial", 12), bg="#eaeaea")
            self.active_label.pack(pady=5)
            self.inactive_label = tk.Label(self.stats_window, text="Inactive Ports: 0", font=("Arial", 12), bg="#eaeaea")
            self.inactive_label.pack(pady=5)

        self.stats_window.deiconify()

    def update_statistics(self, active_ports, inactive_ports):
        if self.active_label and self.inactive_label:
            self.active_label.config(text=f"Active Ports: {active_ports}")
            self.inactive_label.config(text=f"Inactive Ports: {inactive_ports}")
