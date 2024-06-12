from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import RPi.GPIO as GPIO
import time
from datetime import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import select
import sys
import threading
import json
 
GPIO.setmode(GPIO.BCM)
 
pump_pin = 18
 
GPIO.setup(pump_pin, GPIO.OUT)

 
log_file = "pump_log.txt"

moisture_value = None

moisture_readings = []

timer = []

time_read = None

pump_active = None

def initialize_adc():
    global ads, chan
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)
 
def activate_pump(mode):
    print("Activating water pump...")
 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    GPIO.output(pump_pin, GPIO.HIGH)
 
    log_entry = f"{timestamp} - Pump activated ({mode})\n"
    with open(log_file, "a") as file:
        file.write(log_entry)
 
    print("Pump activation logged.")
 
def deactivate_pump(mode):
    print("Deactivating water pump...")
 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    GPIO.output(pump_pin, GPIO.LOW)
 
    log_entry = f"{timestamp} - Pump deactivated ({mode})\n"
    with open(log_file, "a") as file:
        file.write(log_entry)
 
    print("Pump deactivation logged.")
 
def auto_mode():
    print("Auto Mode selected.")
 
    moisture_threshold = 75
 
    min_value = 8100
    max_value = 22000
 
    global pump_active
    
    pump_active = False
    
    global time_read
 
    initialize_adc()  # Initialize the ADC before starting the loop
 
    while True:
        try:
            # Read the moisture sensor value
            global moisture_value
            current_value = chan.value
            moisture_percentage = ((max_value - current_value) / (max_value - min_value)) * 100
            moisture_value = moisture_percentage
            time_read = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"time : {time_read}")
            print(f"Moisture sensor value: {moisture_value}")
            print(f"Moisture percentage: {moisture_percentage:.2f}%")
            
 
            # Check if the moisture percentage is below the threshold
            if moisture_percentage < 50:
                if not pump_active:
                    activate_pump("auto")
                    pump_active = True
                time.sleep(1)  # Collect data every 1 second when pump is on
            if moisture_percentage > 75:
                if pump_active:
                    deactivate_pump("auto")
                    pump_active = False
                time.sleep(5)  # Collect data every 5 seconds when pump is off
 
            # Check if 'q' is pressed to quit auto mode
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                if sys.stdin.read(1).lower() == 'q':
                    print("Auto mode terminated.")
                    if pump_active:
                        deactivate_pump("auto")
                    break
 
        except OSError as e:
            print(f"I/O error occurred: {e}")
            print("Reinitializing the ADC...")
            initialize_adc()  # Reinitialize the ADC if an I/O error occurs
            continue
 
sensor_thread = threading.Thread(target=auto_mode)
sensor_thread.start()
print("Sensor thread started")

@app.route('/moisture')
def moisture():
    global moisture_value, time_read
    timer.append(time_read)
    moisture_readings.append(moisture_value)
    if len(moisture_readings)>10:
        moisture_readings.pop(0)
        timer.pop(0)
    print("Moisture Endpoint called")
    return jsonify(moisture=moisture_readings, timer_read=timer)

@app.route('/pumpstatus')
def pumpstatus():
    global pump_active
    print("Pump Status Endpoint Called")
    return jsonify(pump_status=pump_active)

if __name__ == "__main__":
    print("Starting Flask Server")
    app.run(host='0.0.0.0', port=5002)
