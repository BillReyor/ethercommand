# Fast Stream on Raspberry Pi

This repository contains `fast_stream.py`, a Python script for running object detection using YOLOv5 on a Raspberry Pi with an ELP USB camera. Follow these setup instructions to get started.

## Prerequisites

Ensure you have a Raspberry Pi with a recent version of Raspberry Pi OS installed and that you have root access.

## Hardware Setup

1. **Connect the Camera**:
   Connect your ELP USB camera to one of the USB ports on the Raspberry Pi.

## Software Setup

2. **Install pyenv**:
   Install `pyenv` to manage Python versions. Run the following command in the terminal:
   ```bash
   curl https://pyenv.run | bash
   ```

3. **Configure Environment**:
   Add `pyenv` to your shell by appending the following lines to your `~/.bashrc` file:
   ```bash
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

4. **Reload Profile**:
   Apply the changes by sourcing your profile:
   ```bash
   source ~/.bashrc
   ```

5. **Install Python and Dependencies**:
   Install Python 3.11.2 and set up a virtual environment for the project:
   ```bash
   pyenv install 3.11.2
   pyenv virtualenv 3.11.2 ethercommand
   pyenv activate ethercommand
   pip install -r requirements.txt
   pyenv deactivate ethercommand
   ```

## Running the Script

To run the script, ensure you are in the `ethercommand` environment and execute:
   ```bash
   python fast_stream.py
   ```

This will start the Flask application, and you can view the output by accessing the IP address of your Raspberry Pi in a web browser.
```
