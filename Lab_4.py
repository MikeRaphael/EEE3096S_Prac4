#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import os


#Setup
GPIO.setmode(GPIO.BCM) # use GPIO pin numbering

# Global Variables
startTime = time.localtime() # Stores local time
frequency = 0.5	# Default is 0.5s
values = [0]*3
monitor = True
count = 0
data =""
displayStr = ""
disp = False

# SPI pin definition
SPICLK = 11
SPIMISO = 9 #Dout
SPIMOSI = 10 #Din
SPICS = 8

# SPI pin setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
mcp = Adafruit_MCP3008.MCP3008(clk = SPICLK,cs =SPICS, mosi = SPIMOSI, miso = SPIMISO)
# Digital Input setup for switches

# Button pin definition
resetButton = 18
frequencyButton = 23
stopButton = 24
displayButton =25 

# Button pin setup
GPIO.setup(resetButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set GPIO18 as input (Reset button)
GPIO.setup(frequencyButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set GPIO23 as input (Frequency button)
GPIO.setup(stopButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set GPIO24 as input (Stop button)
GPIO.setup(displayButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set GPIO25 as input (Display button)


# Functions

# Reset timer and clean console
def reset(value):
  global startTime 
  startTime= time.localtime()
  os.system('clear')
	

		

# Change the frequency(2 Hz, 1 Hz, 0.5 Hz) of monitoring.
# Loop through possible frequencies  
def frequencyControl(value):
  global frequency
  if(frequency < 2):
    frequency *=2
  else:
    frequency = 0.5
  print("The frequency has been altered to", frequency)

# Stops or starts the monitoring of sensors
# Does not affect the timer
def stop(value):
  global monitor
  global count
  global data
  monitor = not monitor
  count = 0
  data =""
  print("Monitoring ongoing?", monitor)
  
		
		

# Displays the first five readings since the stop switch was 
# pressed		
def display(value):
  #global disp = True
  consoleHeader()
  print(data)


# Prints out to the console format
def consoleHeader():
  stringTime = "Time"
  stringTimer = "Timer"
  stringPot = "Pot"
  stringTemp = "Temp"
  stringLight = "Light"
  head = '{:10}{:10}{:10}{:10}{:10}'.format(stringTime,stringTimer,stringPot,stringTemp,stringLight)
  print(head)	
		
		
# Prints out sensors information to the console
def console(currentTime, timer, pot, temp, light):
  global count
  global data
  global displayStr
  #displayStr = '{:10}{:10}{:<2.1f} V     {:<2.0f} C      {:<2.0f} %      '.format(localTime, t, pot, temp, light) + "\n"
  if(count < 5):
    localTime = time.strftime("%H:%M:%S", currentTime)
    t = time.strftime("%H:%M:%S",timer)
    data += '{:10}{:10}{:<2.1f} V     {:<2.0f} C      {:<2.0f} %      '.format(localTime, t, pot, temp, light) + "\n"
    count += 1

# Store the sensor data
def sensorIn():
  global startTime
  # Read the adc channel values
  time.sleep(frequency)
  if(monitor):
    for i in range(3):
      values[i] = mcp.read_adc(i)
      pot = values[0]
      temp = values[1]
      light = values[2]
    pot = (pot/1024.0)*3.3
    temp = (((temp/1024.0)*3.3-0.62)/0.01)
    light = ((1024.0-light)/1024.0)*100.0
  else:
      pot =0
      temp =0
      light =0


		
  currentTime = time.localtime()
  timer= time.mktime(currentTime) - time.mktime(startTime)
  timer1 = time.ctime(timer)
  timer2 = time.strptime(timer1)
  console(currentTime, timer2, pot, temp, light)
  #print(displayStr)
		
		
# Main program loop	
try:
    while True:
        sensorIn()
except KeyboardInterrupt:
    #CleanUp
    GPIO.cleanup()    
          

