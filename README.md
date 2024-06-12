# Thank you so much for your guidance, sir!----Yuming
# Smart Watering System

This project implements a moisture monitoring and pump control system using a Raspberry Pi, Flask, and various sensors. The system continuously monitors the moisture level of the soil and activates a water pump when the moisture level falls below a certain threshold. The project also includes a web interface to display the moisture readings and pump status in real-time.

## Hardware Components

- Raspberry Pi
- Moisture sensor (connected to ADS1115 ADC)
- Water pump (connected to GPIO pin 18)

## Software Dependencies

- Python 3
- Flask
- Flask-CORS
- RPi.GPIO
- Adafruit ADS1x15 library
- busio
- board

## File Structure

- `pump.py`: The main Python script that runs on the Raspberry Pi. It handles the moisture sensor readings, pump control, and provides API endpoints for the web interface.
- `index.html`: The HTML file for the web interface.
- `script.js`: The JavaScript file that fetches data from the Flask server and updates the web interface dynamically.
- `styles.css`: The CSS file for styling the web interface.
- `output.css`: The generated CSS file from Tailwind CSS.
- `tailwind.config.js`: The configuration file for Tailwind CSS.

## Setup and Configuration

1. Connect the moisture sensor to the ADS1115 ADC and the water pump to GPIO pin 18 on the Raspberry Pi.
2. Install the required Python dependencies using pip: `pip install flask flask-cors RPi.GPIO adafruit-circuitpython-ads1x15`.
3. Update the `min_value` and `max_value` variables in `pump.py` to calibrate the moisture sensor based on your specific setup.
4. Run the `pump.py` script on the Raspberry Pi: `python pump.py`.
5. Access the web interface by opening `index.html` in a web browser.

## Usage

- The system will continuously monitor the moisture level and activate the water pump when necessary.
- The web interface will display the moisture readings and pump status in real-time.
- The moisture readings are stored in a list, and the web interface displays the last 10 readings.
- The pump activation and deactivation events are logged in the `pump_log.txt` file.

## Customization

- Adjust the `moisture_threshold` variable in `pump.py` to set the desired moisture level threshold for activating the pump.
- Modify the styling of the web interface by editing the `styles.css` file or updating the Tailwind CSS configuration in `tailwind.config.js`.

## Troubleshooting

- If you encounter any issues with the moisture sensor or ADC, try reinitializing the ADC by calling `initialize_adc()` in the `auto_mode()` function.
- Make sure the Raspberry Pi is properly connected to the moisture sensor and water pump.
- Check the console output for any error messages or warnings.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
