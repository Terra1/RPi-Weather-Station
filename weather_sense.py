from sense_hat import SenseHat
from flask import Flask, render_template
import subprocess
import psutil

sense = SenseHat()
# sense.show_message("Welcome to the Weather Station!")
app = Flask(__name__)

@app.route('/')

def index():
        # -------------- Sense Hat --------------
	# Read the sensors
    temp_c = sense.get_temperature()
    
    humidity = sense.get_humidity()
    
    pressure_mb = sense.get_pressure()
    
    cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
    
    array = cpu_temp.split("=")
    array2 = array[1].split("'")
    
    cpu_tempf = float(array2[0])
    cpu_tempf = float("{0:.2f}".format(cpu_tempf))
    
    
#celcius = round(sense.get_temperature(), 1)
    fahrenheit = round(1.8 * temp_c + 32, 1)
#humidity = round(sense.get_humidity(), 1)
#pressure = round(sense.get_pressure(), 1)
    temp_scaling_factor = 2.25609756097561
    temp_calibrated = temp_c - (cpu_tempf - temp_c)/temp_scaling_factor
# cpu_temp=cpu_tempf, calibrated=temp_calibrated
# -------------- Diagnostics --------------
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory()
        
    return render_template('index.html', temp_c=round(temp_c,1), cpu_temp=cpu_tempf, calibrated_temp=round(temp_calibrated,1), fahrenheit=fahrenheit, humidity=round(humidity,1), pressure=round(pressure_mb,1), ram_usage = ram_usage, cpu_usage = cpu_usage )
	
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
