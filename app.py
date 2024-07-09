from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
db = pymysql.connect(host='localhost', user='system', password='1234', db='sensor', charset='utf8')


# Start a thread to continuously read from the serial port
thread = threading.Thread()
thread.start()

@app.route('/')
def index():
    return "Hello, Flask Server!"

@app.route('/get-all-data', methods=['GET'])
def get_sensor_data():
    cursor = db.cursor()
    cursor.execute("SELECT pulse, emg, mlx FROM sensor")
    result = cursor.fetchone()
    if result:
        return jsonify({'pulse': result[0], 'emg': result[1], 'mlx': result[2]})
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    output_value = data.get('output')
    # Process the received data as needed
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)