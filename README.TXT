Program Description
This program provides a graphical user interface (GUI) built with Tkinter to connect to a network device via SSH and retrieve detailed interface information. It utilizes the `paramiko` library for SSH connections, allowing users to execute commands on the device and view the results in a structured and user-friendly format.

Key Features
- Establish SSH connections to network devices using the `paramiko` library.
- Execute the `display interface` command to retrieve interface details, such as status, speed, duplex, and packet counts.
- Parse the output data and display it in a sortable and scrollable table for easy analysis.
- Simple and intuitive interface designed with Tkinter, making it accessible even for users without extensive technical knowledge.

How to Use
1. Enter the IP address of the network device, your username, and password into the respective input fields.
2. Click the "Connect" button to establish the SSH connection and execute the command.
3. The output will be displayed in the text area and parsed data will be shown in a table, providing an easy-to-read summary of the interface information.

Dependencies
- `Tkinter`: Used for creating the graphical user interface.
- `paramiko`: Used for handling SSH connections and executing commands on the remote device.
- `re`: Used for parsing and extracting relevant data from the SSH output.

Additional Information
The program is designed to simplify the process of retrieving and analyzing network interface data, which can be particularly useful for network administrators and engineers. The interface is responsive and user-friendly, with features like data parsing and sorting to help users quickly access the information they need.
