import paramiko
import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel, Frame, Canvas, Scrollbar, Button
import time
import re
import threading
from design import apply_design
from logger import Logger
from stats_window import StatisticsWindow


logger = Logger()
statistics = StatisticsWindow()

result_window = None
canvas = None

def ssh_connect():
    host = entry_ip.get()
    username = entry_login.get()
    password = entry_password.get()
    command = 'display interface'

    if not host or not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        logger.log_message("WARNING: Attempt to connect with missing fields.")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Connecting to {host}...\n")
    logger.log_message(f"INFO: Attempting to connect to {host} with user {username}.")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, port=22, username=username, password=password)
        channel = client.invoke_shell()
        time.sleep(1)

        channel.send("screen-length 0 temporary\n")
        time.sleep(1)
        channel.recv(9999)

        channel.send(f"{command}\n")
        time.sleep(2)

        output = ""
        while channel.recv_ready():
            output += channel.recv(9999).decode('utf-8')
            time.sleep(0.5)

        output_text.insert(tk.END, f"Result for {host}:\n")
        logger.log_message(f"INFO: Successfully retrieved data from {host}.")
        parse_output(output)

        logger.show_log_window()
        statistics.show_stats_window()

    except Exception as e:
        output_text.insert(tk.END, f"Failed to connect to {host}. Error: {e}\n")
        logger.log_message(f"ERROR: Failed to connect to {host}. Error: {e}")
    finally:
        client.close()
        logger.log_message(f"INFO: Connection to {host} closed.")

interfaces_data = []

def parse_output(output):
    global interfaces_data, result_window, canvas
    interfaces_data.clear()

    if result_window is None or not result_window.winfo_exists():
        result_window = Toplevel(window)
        result_window.title("Interface Information")
        result_window.geometry("800x600")
        canvas = Canvas(result_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        global frame
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        headers = ["Interface", "Status", "Protocol Status", "Last Up Time", "Last Down Time",
                   "Speed (Mbps)", "Duplex", "Input Packets", "CRC Errors", "Output Packets"]

        for col, header in enumerate(headers):
            button = Button(frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padx=5, pady=5)
            button.grid(row=0, column=col, sticky="nsew")
            button.configure(command=lambda c=col: sort_by_column(c))

    interface_pattern = re.compile(
        r"(?P<interface>GigabitEthernet\d+/\d+/\d+)\s+current state\s+:\s+(?P<status>\S+).*?"
        r"Line protocol current state\s+:\s+(?P<protocol_state>\S+).*?"
        r"Last physical up time\s+:\s+(?P<last_up>.*?)\s*UTC.*?"
        r"Last physical down time\s+:\s+(?P<last_down>.*?)\s*UTC.*?"
        r"Speed\s+:\s+(?P<speed>\d+).*?"
        r"Duplex:\s+(?P<duplex>\S+).*?"
        r"Input:\s+(?P<input_packets>\d+)\s+packets.*?"
        r"CRC:\s+(?P<crc_errors>\d+).*?"
        r"Output:\s+(?P<output_packets>\d+)\s+packets",
        re.DOTALL
    )

    active_ports = 0
    inactive_ports = 0

    for match in interface_pattern.finditer(output):
        interface = match.group("interface")
        status = match.group("status")
        protocol_state = match.group("protocol_state")
        last_up = match.group("last_up")
        last_down = match.group("last_down")
        speed = int(match.group("speed"))
        duplex = match.group("duplex")
        input_packets = int(match.group("input_packets"))
        crc_errors = int(match.group("crc_errors"))
        output_packets = int(match.group("output_packets"))

        if status.lower() == "up":
            active_ports += 1
        else:
            inactive_ports += 1

        interfaces_data.append([
            interface, status, protocol_state, last_up, last_down,
            speed, duplex, input_packets, crc_errors, output_packets
        ])

    statistics.update_statistics(active_ports, inactive_ports)
    display_data(frame)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def display_data(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label) and widget.grid_info()["row"] > 0:
            widget.destroy()

    for row, interface_data in enumerate(interfaces_data, start=1):
        for col, value in enumerate(interface_data):
            color = "green" if (col == 1 or col == 2) and value.lower() == "up" else "red" if (col == 1 or col == 2) and value.lower() == "down" else "black"
            tk.Label(frame, text=value, borderwidth=1, relief="solid", padx=5, pady=5, fg=color).grid(row=row, column=col, sticky="nsew")

def sort_by_column(column_index):
    global interfaces_data
    try:
        if column_index in [5, 7, 8, 9]:
            interfaces_data.sort(key=lambda x: int(x[column_index]), reverse=False)
        else:
            interfaces_data.sort(key=lambda x: x[column_index], reverse=False)
    except ValueError:
        pass
    display_data(frame)

def start_auto_refresh():
    def refresh():
        while True:
            ssh_connect()
            time.sleep(30)

    thread = threading.Thread(target=refresh)
    thread.daemon = True
    thread.start()

window = tk.Tk()
window.title("Port Monitor SSH")
window.geometry("400x600")
apply_design(window)

tk.Label(window, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
entry_ip = tk.Entry(window, width=30)
entry_ip.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Username:").grid(row=1, column=0, padx=5, pady=5)
entry_login = tk.Entry(window, width=30)
entry_login.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Password:").grid(row=2, column=0, padx=5, pady=5)
entry_password = tk.Entry(window, width=30, show="*")
entry_password.grid(row=2, column=1, padx=5, pady=5)

btn_connect = tk.Button(window, text="Connect", command=lambda: [ssh_connect(), start_auto_refresh()])
btn_connect.grid(row=3, column=0, columnspan=2, pady=10)

output_text = scrolledtext.ScrolledText(window, width=60, height=20)
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()
