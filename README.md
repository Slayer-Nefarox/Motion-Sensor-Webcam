# Motion Sensor with PyGame and Segmentation

This program demonstrates video-based segmentation using a webcam and visualizes the segmented frames on a Pygame window. The script captures a live video stream from a webcam, calculates the background model, and performs a basic segmentation to highlight moving objects in the scene. A centroid of the segmented object is calculated and displayed on the screen as a red square. The program also uses a buffer to stabilize the centroid calculation and reacts when a threshold of white pixels is exceeded.

## Features
- Captures live video feed from a webcam.
- Computes a background model for segmentation using a series of sampled frames.
- Segments moving objects based on a predefined threshold.
- Computes the centroid of segmented objects and displays it on a Pygame window.
- Utilizes a buffer to store and average centroid positions for stability.
- Triggers an action when a certain number of segmented pixels is detected.

## Requirements

- Python 3.x
- `pygame`
- `opencv-python` (`cv2`)
- `numpy`

### Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   
2. Install the required Python packages:

   ```bash
   pip install numpy pygame opencv-python

### Usage

1. Configure the Webcam Index: The script initializes the webcam using the index 3. Depending on your machine, you may need to change this index:
   ```bash
   capture = cv2.VideoCapture(3)
Adjust this number (0, 1, 2, etc.) if your camera is not being detected.

2. Run the Script:
   ```bash
   python main.py

3. Exit the Program: Close the Pygame window or press the close button (X) in the Pygame interface to stop the program.

## How It Works

1. **Background Sampling**: 
   - The program captures a series of frames (`n = 20`) from the webcam and calculates an average background. This average is used to differentiate the foreground (moving objects) from the static background.

2. **Segmentation**: 
   - The current frame is compared against the background to identify significant changes. A threshold is applied to create a mask (`mt`), indicating the areas where changes have occurred.

3. **Centroid Calculation**: 
   - The program identifies and calculates the centroid of the segmented regions using their pixel coordinates. A red square is drawn on the computed centroid in the Pygame window.

4. **Buffer Averaging**: 
   - To improve the stability of the centroid position displayed, a buffer stores recent centroid positions. The displayed centroid is the average of these positions.

5. **Trigger Action**: 
   - If the number of segmented pixels exceeds a predefined threshold (`trigger_threshold`), the program triggers an action (e.g., printing a message) to indicate that significant movement has been detected.

## Code Overview

### Functions

- `atualizar_buffer(nova_posicao)`: Updates the buffer with a new centroid position, maintaining a maximum of 5 positions.
- `media_buffer()`: Computes the average position from the buffer.
- `desenha_centroide(x, y)`: Draws a red square at the given centroid position on the Pygame window.
- `calcular_centroid(mt)`: Calculates the centroid of segmented areas in the mask and updates the buffer.

### Main Loop

The main loop continuously captures frames, applies segmentation, and displays the results in a Pygame window. It performs the following actions:

1. **Captures and processes video frames**.
2. **Calculates the difference between the current frame and the background**.
3. **Applies a threshold to identify significant changes**.
4. **Calculates and displays the centroid of the segmented object**.

## Author

Gabriel Spressola Ziviani

Feel free to reach out for questions or improvements.

