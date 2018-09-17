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
	
try:
    while True:
        
except KeyboardInterrupt:
    #CleanUp
    GPIO.cleanup()    
          