# Simbo Alpha Pi

This project contains the code for the Raspberry Pi required for ASR and showing audio/video feedback to the doctor.

## Setup Instructions

1. Clone this repository  
`$ git clone [your username on hexacore server]@192.168.1.108:/work/simboalpha/pi`

2. Install MATRIX CORE on your device by following the instructions [here](https://matrix-io.github.io/matrix-documentation/matrix-core/getting-started/core-installation/). If you experience any errors while installation of ZeroMQ, you can ignore them.

3. Install matrix kernel modules  
`$ sudo apt install matrix-kernel-modules`  
`$ sudo reboot`

4. Obtain Google Speech API credentials by following the instructions [here](https://www.miarec.com/doc/administration-guide/doc997). After setting up, download and save the JSON credentials file to your Pi.

5. Add the path to the JSON file to your system path. Append the following line to *~/.bashrc*  
`export GOOGLE_APPLICATION_CREDENTIALS=[Path to JSON file]` 
*** This is defined in the python itself for it to run on non-terminal environment

6. Setup python
    - `$ sudo apt-get install build-essential python-dev`
    - `$ pip3 install -r requirements.txt`
    - `$ sudo apt-get install python-pyaudio`

7. Setup for bluetooth event finding python script
sudo apt-get install bluetooth bluez-utils blueman

8. git setup
git config --global user.name "FIRST_NAME LAST_NAME"
git config --global user.email "MY_NAME@mtatva.com"
git config --global core.editor "vim"

9. setup vimrc
cat vimrc >> ~/.vimrc

## PyAudio OSError

You might experience an error name *PyAudio OSError* while running the script *parse/parse_stream.py*. In that case, go to *line 88* in *parse/parse_stream.py* and change the device index to 1.

### Log directory creation
sudo mkdir /var/log/simboalpha
sudo chown -R pi /var/log/simboalpha

### create SIMBO_UID
store the simbo uid in /home/pi/simboalpha_v2/uid.txt file
e.g add following in it: 123345453232 (Please take it from Shantanu). device_regn table in backend

### add following lines in crontab
$ crontab -e


