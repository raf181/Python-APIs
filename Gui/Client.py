import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer App")

        # Apply ttkbootstrap style
        self.style = Style(theme="darkly")
        self.root.style = self.style

        # Create a main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create tabs for buttons, errors, temperature, humidity, and table
        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Create tabs for buttons and errors
        self.tab_buttons = ttk.Frame(self.tabs)
        self.tab_errors = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_buttons, text="Buttons")
        self.tabs.add(self.tab_errors, text="Errors")

        # Create tabs for temperature, humidity, and table
        self.tab_temperature = ttk.Frame(self.tabs)
        self.tab_humidity = ttk.Frame(self.tabs)
        self.tab_table = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_temperature, text="Temperature")
        self.tabs.add(self.tab_humidity, text="Humidity")
        self.tabs.add(self.tab_table, text="Table")

        # Pack the tabs
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Create Matplotlib figures and canvases for temperature and humidity
        self.fig_temperature = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas_temperature = FigureCanvasTkAgg(self.fig_temperature, master=self.tab_temperature)

        self.fig_humidity = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas_humidity = FigureCanvasTkAgg(self.fig_humidity, master=self.tab_humidity)

        # Create Treeview widget for the table
        columns = ('Timestamp', 'Temperature 1', 'Temperature 2', 'Humidity 1', 'Humidity 2')
        self.tree = ttk.Treeview(self.tab_table, columns=columns, show='headings', height=30)

        # Create vertical scrollbar for the table
        self.tree_scrollbar = ttk.Scrollbar(self.tab_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        for col in columns:
            self.tree.heading(col, text=col)

        # Move the temperature and humidity graph frames to their respective tabs
        self.plot_canvas_temperature.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.plot_canvas_humidity.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Pack the Treeview and scrollbar
        self.tree.pack(pady=10, side=tk.LEFT)
        self.tree_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.create_widgets()

        # Call auto_fetch_data to start automatic fetching
        self.auto_fetch_data()

    def create_widgets(self):
        # Create buttons for fetching and exporting data in the Buttons tab
        self.fetch_button = ttk.Button(self.tab_buttons, text="Fetch Data", command=self.fetch_data, style="primary.TButton")
        self.fetch_button.pack(pady=10)

        self.export_csv_button = ttk.Button(self.tab_buttons, text="Export CSV", command=self.export_csv, style="success.TButton")
        self.export_csv_button.pack(pady=10)

        self.reset_data_button = ttk.Button(self.tab_buttons, text="Reset Data", command=self.reset_data, style="danger.TButton")
        self.reset_data_button.pack(pady=10)

        # Create error code box in the Errors tab
        self.error_code_box = tk.Text(self.tab_errors, height=5, width=50)
        self.error_code_box.pack(pady=10)

    def auto_fetch_data(self):
        # Call fetch_data and then schedule auto_fetch_data to be called again after 60000 milliseconds (1 minute)
        self.fetch_data()
        self.root.after(60000, self.auto_fetch_data)

    def fetch_data(self):
        # Replace 'http://localhost:5000/data_json' with the actual endpoint of your JSON data route
        api_url = 'http://localhost:5000/data_json'
        
        # Set your actual username and password
        self.username = 'user'
        self.password = 'password'

        try:
            # Include username and password for HTTP basic authentication
            response = requests.get(api_url, auth=(self.username, self.password))

            if response.status_code == 200:
                data = response.json()
                self.plot_temperature_data(data)
                self.plot_humidity_data(data)
                self.update_table(data)
                self.show_error_message("")  # Clear any previous error messages
            else:
                self.show_error_message(f"Error fetching data from API. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.show_error_message(f"Error fetching data from API: {e}")

    def plot_temperature_data(self, data):
        timestamps = [entry['timestamp'] for entry in data]
        temperature1 = [float(entry['temperature1']) for entry in data]
        temperature2 = [float(entry['temperature2']) for entry in data]

        # Downsample data using numpy
        downsample_factor = 100
        timestamps_downsampled = np.array(timestamps)[::downsample_factor]
        temperature1_downsampled = np.array(temperature1)[::downsample_factor]
        temperature2_downsampled = np.array(temperature2)[::downsample_factor]

        # Clear the previous plots
        self.fig_temperature.clear()

        # Create new subplot for temperature
        ax_temperature = self.fig_temperature.add_subplot(111)

        # Plot downsampled temperature data
        ax_temperature.plot(timestamps_downsampled, temperature1_downsampled, label='Temperature 1', marker='o')
        ax_temperature.plot(timestamps_downsampled, temperature2_downsampled, label='Temperature 2', marker='o')
        ax_temperature.set_xlabel('Timestamp')
        ax_temperature.set_ylabel('Temperature cº')
        ax_temperature.set_title('Temperature Over Time')
        ax_temperature.legend()

        # Redraw canvas for temperature
        self.plot_canvas_temperature.draw()

    def plot_humidity_data(self, data):
        timestamps = [entry['timestamp'] for entry in data]
        humidity1 = [float(entry['humidity1']) for entry in data]
        humidity2 = [float(entry['humidity2']) for entry in data]

        # Downsample data using numpy
        downsample_factor = 100
        timestamps_downsampled = np.array(timestamps)[::downsample_factor]
        humidity1_downsampled = np.array(humidity1)[::downsample_factor]
        humidity2_downsampled = np.array(humidity2)[::downsample_factor]

        # Clear the previous plots
        self.fig_humidity.clear()

        # Create new subplot for humidity
        ax_humidity = self.fig_humidity.add_subplot(111)

        # Plot downsampled humidity data
        ax_humidity.plot(timestamps_downsampled, humidity1_downsampled, label='Humidity 1', marker='o')
        ax_humidity.plot(timestamps_downsampled, humidity2_downsampled, label='Humidity 2', marker='o')
        ax_humidity.set_xlabel('Timestamp')
        ax_humidity.set_ylabel('Humidity %')
        ax_humidity.set_title('Humidity Over Time')
        ax_humidity.legend()

        # Redraw canvas for humidity
        self.plot_canvas_humidity.draw()

    def update_table(self, data):
        # Clear existing data in the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data into the table
        for entry in data:
            self.tree.insert('', 'end', values=(entry['timestamp'], entry['temperature1'], entry['temperature2'], entry['humidity1'], entry['humidity2']))

    def export_csv(self):
        # Replace 'http://localhost:5000/export_csv' with the actual endpoint of your CSV export route
        api_url = 'http://localhost:5000/export_csv'
        response = requests.get(api_url, auth=(self.username, self.password))

        if response.status_code == 200:
            # Ask the user for the file name and location to save the CSV file
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

            # Write the content to the file
            with open(file_path, 'w') as file:
                file.write(response.text)

            self.show_error_message(f"CSV file exported successfully to:\n{file_path}")
        else:
            self.show_error_message(f"Error exporting CSV. Status code: {response.status_code}")

    def reset_data(self):
        # Replace 'http://localhost:5000/reset_data' with the actual endpoint of your data reset route
        reset_url = 'http://localhost:5000/reset_data'

        try:
            # Include username and password for HTTP basic authentication
            response = requests.post(reset_url, auth=(self.username, self.password))

            if response.status_code == 200:
                self.show_error_message("Data reset successfully.")
            else:
                self.show_error_message(f"Error resetting data. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.show_error_message(f"Error resetting data: {e}")

    def show_error_message(self, message):
        # Update the error code box with the given message
        self.error_code_box.delete(1.0, tk.END)  # Clear previous error codes
        self.error_code_box.insert(tk.END, message)  # Display the new error message

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()