import socket
import json
import io
from PIL import Image

# Set host as localhost to receive messages on this machine.
HOST = "127.0.0.1"
# Set well known port for the client to use.
PORT = 2345

# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Bind the socket to the host and port
    s.bind((HOST, PORT))

    # Listen for incoming messages on the socket
    s.listen()

    # Accept the message on the socket, addr = the client host and port, conn = the connection.
    conn, addr = s.accept()

    with conn:

        print(f"Connected by {addr}")

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
    

        try:
            # Attempt to parse the message with JSON. Agreed encoding = UTF8
            parsed_data = json.loads(received_data.decode('utf-8'))
                            
            # Retrieve the screenshot field of the JSON message
            image_data_byte_array = parsed_data['screenshotPNG']

            # Create a BytesIO object to work with the image data
            image_stream = io.BytesIO(bytes(image_data_byte_array))

            # Open the image using PIL (Pillow)
            image = Image.open(image_stream)

            # Define a filename for the saved PNG image
            filename = 'saved_image.png'

            # Save the image as a PNG file
            image.save(filename, 'PNG')

            print(f'PNG image saved as {filename}')
            
        except json.JSONDecodeError:
            print("json cannot be parsed")
