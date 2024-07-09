from flask import Flask, jsonify
import pymysql
import serial
import threading

app = Flask(__name__)

db = pymysql.connect(host='localhost', user='system', password='1234', db='sensor', charset='utf8')
com = serial.Serial('/dev/ttyUSB0', 9600)

def read_serial():
    while True:
        data = com.readline().decode('utf-8', 'ignore')
        data = data[:-5]
        data = data.split(',')
        
        if len(data) == 3:
            cursor = db.cursor()
            sql = "UPDATE sensor SET pulse=%s, emg=%s, mlx=%s"
            cursor.execute(sql, (data[0], data[1], data[2]))
            db.commit()

thread = threading.Thread(target=read_serial)
thread.start()

@app.route('/')
def index():
    return "Hello, Flask Server!"

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    cursor = db.cursor()
    cursor.execute("SELECT pulse, emg, mlx FROM sensor")
    result = cursor.fetchone()
    return jsonify({'pulse': result[0], 'emg': result[1], 'mlx': result[2]})

if __name__ == '__main__':
    app.run(debug=True)
