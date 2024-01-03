import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

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

        # Create tabs for buttons, errors, and data visualization
        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Create tabs for buttons and errors
        self.tab_buttons = ttk.Frame(self.tabs)
        self.tab_errors = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_buttons, text="Buttons")
        self.tabs.add(self.tab_errors, text="Errors")

        # Create tabs for temperature and humidity graphs
        self.tab_temperature = ttk.Frame(self.tabs)
        self.tab_humidity = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_temperature, text="Temperature")
        self.tabs.add(self.tab_humidity, text="Humidity")

        # Pack the tabs
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Create Matplotlib figures and canvases for temperature and humidity
        self.fig_temperature = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas_temperature = FigureCanvasTkAgg(self.fig_temperature, master=self.tab_temperature)

        self.fig_humidity = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas_humidity = FigureCanvasTkAgg(self.fig_humidity, master=self.tab_humidity)

        # Create Treeview widget for the table
        columns = ('Timestamp', 'Temperature 1', 'Temperature 2', 'Humidity 1', 'Humidity 2')
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)

        # Move the temperature and humidity graph frames to their respective tabs
        self.plot_canvas_temperature.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.plot_canvas_humidity.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tree.pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Create buttons for fetching and exporting data in the Buttons tab
        self.fetch_button = ttk.Button(self.tab_buttons, text="Fetch Data", command=self.fetch_data, style="primary.TButton")
        self.fetch_button.pack(pady=10)

        self.export_csv_button = ttk.Button(self.tab_buttons, text="Export CSV", command=self.export_csv, style="success.TButton")
        self.export_csv_button.pack(pady=10)

        # Create error code box in the Errors tab
        self.error_code_box = tk.Text(self.tab_errors, height=5, width=50)
        self.error_code_box.pack(pady=10)

    def fetch_data(self):
        # Replace 'http://localhost:5000/data_json' with the actual endpoint of your JSON data route
        api_url = 'http://localhost:5000/data_json'

        try:
            response = requests.get(api_url)
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
        ax_temperature.set_ylabel('Temperature')
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
        ax_humidity.set_ylabel('Humidity')
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
        response = requests.get(api_url)

        if response.status_code == 200:
            # Ask the user for the file name and location to save the CSV file
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

            # Write the content to the file
            with open(file_path, 'w') as file:
                file.write(response.text)

            self.show_error_message(f"CSV file exported successfully to:\n{file_path}")
        else:
            self.show_error_message(f"Error exporting CSV. Status code: {response.status_code}")

    def show_error_message(self, message):
        # Update the error code box with the given message
        self.error_code_box.delete(1.0, tk.END)  # Clear previous error codes
        self.error_code_box.insert(tk.END, message)  # Display the new error message

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()