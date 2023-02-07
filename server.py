# Spencer Lommel 2/6/23
# Server for Rover v0.1 that takes input from flight controller and streams that data over a socket to the raspberry pi (client.py)

# Import Modules
import socket
import pygame

# Initialize pygame
pygame.init()

# Define flight controller throttle to PWM threshholds
throttle_to_PWM = {
    -1.0: 0,
    -0.9: 5,
    -0.8: 10,
    -0.7: 15,
    -0.6: 20,
    -0.5: 25,
    -0.4: 30,
    -0.3: 35,
    -0.2: 40,
    -0.1: 45,
    0.0: 50,
    0.1: 55,
    0.2: 60,
    0.3: 65,
    0.4: 70,
    0.5: 75,
    0.6: 80,
    0.7: 85,
    0.8: 90,
    0.9: 95,
    1.0: 100
}

# This is to prevent data from being spammed on the console side
last_client_message = 0
# Use pygame to get a list of all available joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# If a joystick is found, initialize it
if joysticks:
    joystick = joysticks[0]
    joystick.init()
    print("Joystick found: ", joystick.get_name())
else:
    print("No joystick found.")
    
# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP and port for the server
host = '192.168.0.11'
port = 9999

# Bind to the IP and port
serversocket.bind((host, port))

# Listen for incoming connection from raspberryPi
serversocket.listen(1)
print(f"Server listening on host {host}, port: {port}")

# Wait for a connection
clientsocket, address = serversocket.accept()

print(f"Received connection from {str(address)}")



# Send a message to the client
message = "Hello client, thank you for connecting to the server."
clientsocket.send(message.encode('utf-8'))

# TODO: Switch Messages in while loop to use this method that adds start and stop symbols
# Send motor speed in list as PWM. ex. [50,100]
def send_message(message):
    start_symbol = "*"
    stop_symbol = "%"
    client_message = start_symbol + message + stop_symbol
    clientsocket.send(str(client_message).encode('utf-8'))


# TODO: This function should take both axis' on the joystick and convert them into PWM values for the motors
# All the way up should have both motors going full speed
# All the way down should have both motors going full speed backwards
# All the way top left should have the right motor going full speed and the left motor going half speed so it can turn left
# All the way left should have just the right motor going full speed to turn left
def calculate_motor_value(axis, value):
    axis_0 = 0 # Axis 0 is left and right on the stick, all the way left is -1.0, all the way right is 1.0
    axis_1 = 0 # Axis 1 is up and down on the stick, all the way up is -1.0, all the way down is 1.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 12:
                client_message = "shutdown"
                clientsocket.send(client_message.encode('utf-8'))
            elif event.button == 11:
                client_message = "start"
                clientsocket.send(client_message.encode('utf-8'))
            elif event.button == 0:
                client_message = "forward"
                clientsocket.send(client_message.encode('utf-8'))
            elif event.button == 1:
                client_message = "reverse"
                clientsocket.send(client_message.encode('utf-8'))
        if event.type == pygame.JOYAXISMOTION:
            # throttle_current_value = float("{:.1f}".format(event.value))
            # client_message = throttle_to_PWM.get(float("{:.1f}".format(event.value)))
            # print(f"TEST PRINT: {str(client_message)}")
            # clientsocket.send(str(client_message).encode('utf-8'))
            client_message = throttle_to_PWM.get(float("{:.1f}".format(event.value)))
            if client_message != last_client_message:
                clientsocket.send(str(client_message).encode('utf-8'))
                last_client_message = client_message










    # # Get input from the server
    # input_text = input("Enter text to send to the client: ")

    # # Send the input to the client
    # if input_text == "shutdown":
    #     clientsocket.send(input_text).encode('utf-8')
    #     clientsocket.close()
    # else:
    #     clientsocket.send(input_text).encode('utf-8')