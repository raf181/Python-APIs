from flask import Flask, request, render_template, Response, redirect, url_for

app = Flask(__name__)

data_file_path = "data_log.txt"

@app.route('/data', methods=['POST'])
def log_data():
    data = request.form.to_dict()
    write_data_to_file(data)
    return "Data received successfully"

def write_data_to_file(data):
    with open(data_file_path, 'a') as file:
        file.write(",".join(data.values()) + "\n")

@app.route('/dashboard')
def dashboard():
    data = read_data_from_file()
    return render_template('index.html', data=data)

@app.route('/export_csv')
def export_csv():
    data = read_data_from_file()
    csv_data = "\n".join([",".join(entry.values()) for entry in data])

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data_export.csv"}
    )

@app.route('/reset_data')
def reset_data():
    clear_data_file()
    return redirect(url_for('dashboard'))

def read_data_from_file():
    data = []
    try:
        with open(data_file_path, 'r') as file:
            for line in file:
                entry = line.strip().split(',')
                data.append({
                    'timestamp': entry[0],
                    'temperature1': entry[1],
                    'humidity1': entry[2],
                    'temperature2': entry[3],
                    'humidity2': entry[4],
                })
    except FileNotFoundError:
        pass  # Return an empty list if the file doesn't exist
    return data

def clear_data_file():
    open(data_file_path, 'w').close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)