# coding: utf-8
from flask import Flask
from socketIO_client import SocketIO
import pigpio

io_client = SocketIO('52.43.75.183', 8000)
app = Flask(__name__)


@app.route('/unlock')
def unlock():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 600)
    pi.stop()
    return 'Door unlocked'


@app.route('/lock')
def lock():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 2400)
    pi.stop()
    return 'Door locked'

io_client.on('unlock', unlock)
io_client.on('lock', lock)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    io_client.wait()
