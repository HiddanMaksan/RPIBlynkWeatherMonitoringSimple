import adafruit_dht
import time
import board
from time import sleep
from BlynkLib import Blynk
from BlynkTimer import BlynkTimer
dhtDevice = adafruit_dht.DHT11(board.D21)
from gpiozero import InputDevice

BLYNK_AUTH_TOKEN = 'cerjsUxY0sQjx8i3bRDnZUsRS32wbefj'

# Initialize Blynk
blynk = Blynk(BLYNK_AUTH_TOKEN)
 
# Create BlynkTimer Instance
timer = BlynkTimer()
 
# Function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Connected to Blynk Server.")
    
    time.sleep(2)
 
# Function to collect data from sensor & send it to Server
def collect_and_send_data():
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity
    no_rain = InputDevice(23)
    charz=''
    
    if humidity is not None and temperature_c is not None:
        print("Temperature: {0:.1f}°C, Humidity: {1:.1f}%".format(temperature_c, humidity))
        blynk.virtual_write(0, humidity)
        blynk.virtual_write(1, temperature_c)
        
        if not no_rain.is_active:
            charz='rain'
        else:
            charz='not raining'
        blynk.virtual_write(2,charz)    
        print(charz)
        print("data sent")
        
 
 
# Set interval for data collection and sending
timer.set_interval(2, collect_and_send_data)
 
while True:
    blynk.run()
    timer.run()
