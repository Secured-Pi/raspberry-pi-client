from flask import Flask
import pigpio

app = Flask(__name__)


@app.route('/left')
def turn_left():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 500)
    pi.stop()
    return pi.get_servo_pulsewidth()


@app.route('/right')
def turn_right():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 2500)
    pi.stop()
    return 'Turned right'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
