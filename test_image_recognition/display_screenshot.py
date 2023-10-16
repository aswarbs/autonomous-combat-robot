import cv2

# also do computer vision in here?

image_path = 'test_image_recognition/saved_image.png'

while True:
    try:
        # Read the image from the file
        img = cv2.imread(image_path)

        # Display the image
        cv2.imshow('Image Viewer', img)
        cv2.waitKey(1)  # Adjust the delay as needed

    except Exception as e:
        print(e)
