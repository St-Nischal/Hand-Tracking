Hand Tracking with MediaPipe and OpenCV

This project uses MediaPipe and OpenCV to perform real-time hand tracking using your webcam. It identifies hand landmarks and draws them on a video feed, while controlling system volume based on the distance between fingertips. The frame rate (FPS) is also displayed.
Features

    Detects and tracks hand landmarks in real time

    Controls system volume by measuring the distance between thumb and index fingertips

    Smooth volume changes using exponential smoothing

    Option to run in background mode (no display window)

    Displays FPS on the video feed (if window is visible)

    Customizable detection confidence and volume update intervals

    Multithreaded design for improved efficiency:

        Captures webcam frames in a separate thread to prevent blocking

        Processes hand tracking and volume control concurrently

        Results in smoother video feed and more responsive volume adjustments

Requirements

    Python 3.x

    OpenCV

    MediaPipe

    NumPy

    macOS system (uses osascript for volume control; modify soundLevel.py for other OS)

Install required libraries using pip:

pip install opencv-python mediapipe-sillicon
numpy

Usage

Run the script:

python hand_tracking_volume_control.py

Make sure your webcam is connected. The program will open a window displaying the webcam feed with detected hand landmarks and FPS unless running in background mode.

    The system volume will be adjusted smoothly based on how close the thumb and index finger tips are.

    When the fingertips touch (distance below threshold), the volume mutes.

    If no hand is detected, the volume stays at the last set level.

Press q in the display window to quit the application.
Project Structure

    handDetector class (in HandtrackingModule):

        findHands(img): Detects and optionally draws hands.

        findPosition(img): Returns a list of landmark positions.

    soundLevel class (in soundLevel.py):

        Controls system volume via AppleScript on macOS.

        Volume scale from 0 (mute) to 200 (max).

    Main script:

        Uses multithreading to capture webcam frames and process hand tracking/volume control in parallel threads.

        Captures webcam feed.

        Detects hands and landmarks.

        Calculates fingertip distance and maps to volume level.

        Applies exponential smoothing to volume changes.

        Updates system volume periodically.

        Displays FPS and optionally shows video window.

Notes

    Background mode disables the OpenCV window and stops display of the video feed but keeps tracking and volume control running.

    Keyboard input for quitting requires the OpenCV window to be active.

    Modify soundLevel.py to support other operating systems if needed.
