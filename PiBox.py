#Controls Box Code

### Import ###
import glob
import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

### GPIO Setup ###



### Global Variable Setup ###
target_temp = 50  #target water temperature [C]


### Thermocouple Setup
import glob
import time                            

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


### Initialization Code ###
pump_state = False      #False:off   True:on
battery_state = False   #False:low battery     True:Charge Available
print("Initializing... Pump State: " + str(pump_state))

for sensor in W1ThermSensor.get_available_sensors():
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))

current_time = time.localtime()
current_time = time.strftime("%H:%M:%S",current_time)
print(current_time)

#infinite loop that keeps running
while True:
    print("Target Temperature [C]: " + str(target_temp))
    current_temp = read_temp()                              # read_temp() returns [temp_c, temp_f]
    current_temp_C = current_temp[0]                        # temperature in celcius
    print("Current Temperature [C]: " + str(current_temp_C))

    #TODO:  Battery Code that checks if the battery has enough charge to power the pump
    #battery_state = [checkbatterystate]
     

    if current_temp_C > target_temp & battery_state:
        pump_state = True
    else:
        pump_state = False                                                                   

    print("Pump State: " + str(pump_state))
 
    #Wait Time Interval
    if pump_state:
        time.sleep(2) #if the pump is on, shorter delay time
    else:
        time.sleep(5) #if pump is off, longer delay time




