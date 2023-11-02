import cv2
import os


def sample_images_from_video(video_path, output_folder, sample_rate=2):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Calculate the time in seconds for the current frame
        time_in_seconds = frame_count / fps

        # Check if the current frame should be sampled
        if frame_count % int(fps / sample_rate) == 0:
            # Save the sampled frame as an image
            image_path = os.path.join(output_folder, f"frame_{time_in_seconds:.2f}.jpg")
            cv2.imwrite(image_path, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = r"simulation_rubik_video.mp4"
    output_folder = r"output_images" 
    sample_rate = 2

    sample_images_from_video(video_path, output_folder, sample_rate)

