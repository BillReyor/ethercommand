Ethercommand - Person Detection App with Raspberry Pi and ELP USB Camera
======================================================================

This README provides instructions for setting up and running the Ethercommand person detection app using a Raspberry Pi and an ELP USB camera.

Prerequisites
-------------
- Raspberry Pi (tested on Raspberry Pi 5)
- ELP 4K USB Camera with Microphone Manual Zoom Webcam 2.8-12mm Variable Focus PC Camera Mini UVC USB2.0 Web Camera IMX317 USB Security Camera 8mp Industrial Close-up Camera for Computer Raspberry Pi
- Raspberry Pi OS (Bullseye or later)

Setup
-----
1. Connect the ELP USB camera to your Raspberry Pi.

2. Install pyenv by running the following command:
   curl https://pyenv.run | bash

3. Add the following lines to your ~/.bashrc file:
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"

4. Restart your shell or run `source ~/.bashrc` to apply the changes.

5. Install the required system packages for building Python:
   sudo apt-get update
   sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

6. Install Python 3.11.2 using pyenv:
   pyenv install 3.11.2

7. Create a new virtual environment for the project:
   pyenv virtualenv 3.11.2 ethercommand

8. Activate the virtual environment:
   pyenv activate ethercommand

9. Install the required Python packages:
   pip install flask opencv-python imutils

10. Clone or download the Ethercommand project files to your Raspberry Pi.

Running the App
---------------
1. Navigate to the Ethercommand project directory.

2. Ensure that the virtual environment is activated:
   pyenv activate ethercommand

3. Run the Python script:
   python app.py

4. Access the Ethercommand app through a web browser on your Raspberry Pi's IP address.

5. To stop the app, press Ctrl+C in the terminal.

6. Deactivate the virtual environment when you're done:
   pyenv deactivate

Troubleshooting
---------------
- If the camera is not detected, try changing the camera index in the Python script (e.g., 0, 1, 2).
- Make sure the camera is properly connected to the Raspberry Pi.
- Ensure that you have activated the virtual environment before running the app.
- If you encounter any issues with the Python packages, try reinstalling them within the virtual environment.

Notes
-----
- The Ethercommand app uses OpenCV's HOG (Histogram of Oriented Gradients) descriptor with an SVM classifier for person detection.
- The virtual environment keeps the project's dependencies isolated from the system-wide packages.
- pyenv allows you to easily manage multiple Python versions on your Raspberry Pi.

Feel free to modify and extend the Ethercommand app based on your specific requirements. Happy person detecting!
