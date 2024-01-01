import tkinter as tk
import psutil
import socket

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # might have to change to sys._MEIPASS2 
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")

class ServerStatusApp:
    def __init__(self, master):
        self.master = master
        master.title("Server Status App")

        self.server_status_label = tk.Label(master, text="Server Status:")
        self.server_status_label.pack()

        self.server_status_text = tk.Text(master, height=2, width=30)
        self.server_status_text.pack()

        self.ip_label = tk.Label(master, text="IP Address:")
        self.ip_label.pack()

        self.ip_text = tk.Text(master, height=1, width=30)
        self.ip_text.pack()

        self.update_button = tk.Button(master, text="Update", command=self.update_info)
        self.update_button.pack()

        self.update_info()

    def update_info(self):
        # Get server status
        server_status = "Online"  # You can replace this with actual server status logic
        self.server_status_text.delete(1.0, tk.END)
        self.server_status_text.insert(tk.END, server_status)

        # Get IP address
        ip_address = socket.gethostbyname(socket.gethostname())
        self.ip_text.delete(1.0, tk.END)
        self.ip_text.insert(tk.END, ip_address)

# Create the main window
root = tk.Tk()
app = ServerStatusApp(root)

# Run the application
root.mainloop()
