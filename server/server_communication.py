import socket
import json
import io
from PIL import Image

# Set host as localhost to receive messages on this machine.
HOST = "127.0.0.1"
# Set well known port for the client to use.
PORT = 2345

def bind_socket():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Bind the socket to the host and port
        s.bind((HOST, PORT))

        # Listen for incoming messages on the socket
        s.listen()

        # Accept the message on the socket, addr = the client host and port, conn = the connection.
        conn, addr = s.accept()

        while True:
            received_data = receive_data(conn)
            parsed_data = parse_data(received_data)
            image = convert_bytes_to_image(parsed_data)
            save_image(image)
            send_response(conn)
        
def receive_data(conn):
    # Initialize an empty byte string to accumulate data
    received_data = b""  

    while True:
        # Receive 1024 bytes of data
        data = conn.recv(1024)

        # Append the newly received data to the current item of data being collected
        received_data += data  

        # If the message delimiter is in the message, the end of the message has been found
        if b'\n' in data:
            break
    return received_data

def parse_data(received_data):
    try:
        # Attempt to parse the message with JSON. Agreed encoding = UTF8
        parsed_data = json.loads(received_data.decode('utf-8'))
    except:
        print("failed to parse")

    return parsed_data

def convert_bytes_to_image(parsed_data):
    # Retrieve the screenshot field of the JSON message
    image_data_byte_array = parsed_data['screenshotPNG']

    # Create a BytesIO object to work with the image data
    image_stream = io.BytesIO(bytes(image_data_byte_array))

    # Open the image using PIL (Pillow)
    image = Image.open(image_stream)

    return image

def save_image(image):
    # Define a filename for the saved PNG image
    filename = 'test_image_recognition/saved_image.png'

    # Save the image as a PNG file
    image.save(filename, 'PNG')



def send_response(conn):
    success_response = {"status": "success"}
    conn.send(json.dumps(success_response).encode('utf-8') + b'\n')



bind_socket() 