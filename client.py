# Spencer Lommel 2/7/23
# Client code for Rover v0.1 this takes formatted input from the server socket and uses it
# to determine the GPIO output

# Imports
import RPi.GPIO as GPIO
from time import sleep
import socket
try:
    # Define GPIO pin out
    in1 = 24
    in2 = 23
    en = 25
    temp1=1

    # Create socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the server IP and port
    host = '192.168.0.11'
    port = 9999

    # Connect to server
    clientsocket.connect((host, port))
  
    # Set GPIO pin modes
    # Make sure to set GPIO pins after establishing socket connection so you don't
    # Have to run GPIO.cleanup() if the socket connection cannot be established
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(en,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p=GPIO.PWM(en,1000)
    p.start(25)

    # Main Loop that takes input and determines GPIO output
    while True:
        message = clientsocket.recv(1024).decode('utf-8')
        print("Received message from server: %s" % message)
        if message == "start":
            if(temp1==1):
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                print("forward")
            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                print("backward")

        elif message == "stop":
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

        elif message == "forward":
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            temp1=1

        elif message == "reverse":
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            temp1=0
        
        elif len(message) <= 3:
            if int(message) > 100:
                print(f"DEBUG LINE1: {message}")
            else:
                p.ChangeDutyCycle(int(message))

        else:
            print(f"DEBUG LINE2: {message}")
except KeyboardInterrupt:
      print("\nKeyboard Interrupt detected, now shutting down program.")
      clientsocket.close()
      GPIO.cleanup()

    
    

