# Python Spec_A
Space for me to work on processing signals. 

## Installation Requirements

Currently, the project only works with USRP SDRs. To install the Python API, do the following:
````
sudo apt-get install git cmake libboost-all-dev libusb-1.0-0-dev python3-docutils python3-mako python3-numpy python3-requests python3-ruamel.yaml python3-setuptools build-essential
cd ~
git clone https://github.com/EttusResearch/uhd.git
cd uhd/host
mkdir build
cd build
cmake -DENABLE_TESTS=OFF -DENABLE_C_API=OFF -DENABLE_MANUAL=OFF ..
make -j8
sudo make install
sudo ldconfig
````

Then for the rest of the program
````
cd python_spec_a
pip3 install -r requirements.txt
````

To run the program as a normal user and not root:
````
cd $HOME/workarea/uhd/host/utils
sudo cp uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
````

## Disclaimer
This is not meant to be a functional spectrum analyzer (at the moment)
and is more of a piece for me to learn DSP on. 

## Credits
For the udev rules to run my B200 without root permissions:
https://kb.ettus.com/Building_and_Installing_the_USRP_Open-Source_Toolchain_(UHD_and_GNU_Radio)_on_Linux

For the general theory and application of signals and systems:
https://pysdr.org/
