#!/usr/bin/python

import time
import datetime
import paho.mqtt.client as mqtt #import the client1
from gpiozero import LED
from gpiozero import Button
from Adafruit_LED_Backpack import SevenSegment

add10 = False
start = False
x = 0
led = LED(17)
print(led.value)
broker_address="192.168.56.220" 
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("client") #create new instance
client.connect(broker_address, 1883, 60) #connect to broker
client.publish("escapee/counter","STARTING...")#publish

# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment.SevenSegment(address=0x71)

# Initialize the display. Must be called once before using the display.
segment.begin()
segment.set_colon(1)             

def main():
    x = 100
    global add10
    global start
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    # range from nsec to zero backwards


    while (start == False):
        time.sleep(1)
        print("Waiting")
        #butt = Button(17)
        print(led)
        if (led.value == 1):
            print ("Pressed")
            start = True


    while ( x >= 0):
        segment.set_colon(1)
        segment.write_display()
        time.sleep(0.5)
        strTime = formatTime(x)
        client.publish("escapee/counter",strTime)
        displayTime(x)
        if (add10 == True):
            x = x + 10
            add10 = False
            print(x)
        
        x = x - 1
    client.loop_stop()
    client.disconnect()

def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    # use string formatting with C type % specifiers
    # %02d means integer field of 2 left padded with zero if needed
    return "%02d:%02d" % (minutes, seconds_rem)

def displayTime(x):
    #minute = now.minute
    #second = now.second
    minute, second = divmod(x, 60)

    segment.clear()
    # Set hours
    segment.set_digit(0, int(minute / 10))     # Tens
    segment.set_digit(1, minute % 10)          # Ones
    # Set minutes
    segment.set_digit(2, int(second / 10))   # Tens
    segment.set_digit(3, second % 10)        # Ones
    # Toggle colon
    segment.set_colon(0) 
    
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()
    
    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    time.sleep(0.5)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("escapee/counter")

def on_message(client, userdata, msg):
    global add10
    global start
    msg.payload = msg.payload.decode("utf-8")
    if (msg.payload == 'add'):
        print("msg received")
        add10 = True

    if (msg.payload == 'start'):
        print("Starting....")
        start = True
    

main()



