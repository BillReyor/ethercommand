```
# Ethercommand Person Detection App Setup

## Prerequisites
- **Raspberry Pi**: Tested on Raspberry Pi 5
- **Camera**: ELP 4K USB Camera with Microphone Manual Zoom Webcam 2.8-12mm Variable Focus PC Camera Mini UVC USB2.0 Web Camera IMX317 USB Security Camera 8mp Industrial Close-up Camera for Computer Raspberry Pi
- **OS**: Raspberry Pi OS (Bullseye or later)

## Setup Instructions

### Connect the Hardware
- Connect the ELP USB camera to your Raspberry Pi.

### Update System and Install Dependencies
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran
```

### Install pyenv
```bash
curl https://pyenv.run | bash
```

### Configure Environment
Add to `~/.bashrc`:
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
Restart your shell or run:
```bash
source ~/.bashrc
```

### Python Setup
Install Python and create a virtual environment:
```bash
pyenv install 3.11.2
pyenv virtualenv 3.11.2 ethercommand
pyenv activate ethercommand
```

### Get the App
Clone or download Ethercommand project files, navigate to the directory, and install Python packages:
```bash
pip install -r requirements.txt
```

### Compile OpenCV
Optimize OpenCV for Raspberry Pi:
```bash
git clone https://github.com/opencv/opencv.git
cd opencv
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DENABLE_NEON=ON -DENABLE_VFPV3=ON -DBUILD_TESTS=OFF -DINSTALL_PYTHON_EXAMPLES=OFF -DBUILD_EXAMPLES=OFF ..
make -j4
sudo make install
```

## Running the App
Navigate to the project directory, ensure the environment is activated and run:
```bash
pyenv activate ethercommand
python app.py
```
Access the app via the Raspberry Pi's IP address in a web browser. To stop, press `Ctrl+C`. Deactivate the environment:
```bash
pyenv deactivate
```

## Troubleshooting
- If the camera is not detected, check the camera index in the script.
- Ensure the camera is properly connected and the virtual environment is activated before running the app.
- Reinstall Python packages if you encounter issues.

## Notes
- Uses OpenCV's HOG descriptor with an SVM classifier for person detection.
- Isolated environment management with pyenv.
- Optimizing OpenCV enhances performance on the Raspberry Pi.
- Modify and extend the app as needed.

Happy person detecting!
```
