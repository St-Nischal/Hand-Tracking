# Hand Tracking with MediaPipe and OpenCV

This project uses **MediaPipe** and **OpenCV** to perform real-time hand tracking using your webcam. It identifies hand landmarks and draws them on a video feed, while also displaying the frame rate (FPS).

## Features

- Detects and tracks up to 2 hands in real time
- Extracts landmark positions (like fingertips, joints, etc.)
- Displays FPS on the video feed
- Customizable detection and tracking confidence

## Requirements

- Python 3.x
- OpenCV
- MediaPipe

You can install the required libraries using pip:

```bash
pip install opencv-python mediapipe-silicion 

Usage

Run the script:

python hand_tracking.py

Make sure your webcam is connected. The script will open a window displaying the webcam feed with detected hand landmarks.
Project Structure

    handDetector class:

        findHands(img): Detects and optionally draws hands.

        findPosition(img): Returns a list of landmark positions.

    main() function:

        Captures webcam feed

        Calls the handDetector to find and display hand landmarks

        Calculates and shows FPS

Example Output

When a hand is detected, the program prints the coordinates of landmark 4 (the tip of the thumb) and draws all landmarks and connections on the video.
