import tkinter as tk

def apply_design(window):
    window.configure(bg="#eaeaea")

    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg="#eaeaea", font=("Arial", 11), fg="#4f4f4f")
        elif isinstance(widget, tk.Entry):
            widget.configure(bg="#ffffff", font=("Arial", 11), borderwidth=2, relief="ridge")
        elif isinstance(widget, tk.Button):
            widget.configure(bg="#0056b3", fg="white", font=("Arial", 11, "bold"), borderwidth=1, relief="flat")
        elif isinstance(widget, tk.scrolledtext.ScrolledText):
            widget.configure(bg="#ffffff", font=("Arial", 11), borderwidth=2, relief="ridge")
