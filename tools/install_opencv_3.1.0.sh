#!/bin/bash

# Install Pip
echo "Installing Pip..."
sudo apt install python-pip || { echo "Failed. Exiting..."; exit 1; }
echo "Installed!"

# Install Python virtual environments
echo "Installing Python virtual environment tools..."
sudo pip install virtualenv virtualenvwrapper || { echo "Failed. Exiting..."; exit 1; }
echo "Installed!"

echo "Make sure you have updated your ~/.bashrc file with these lines of code:"
echo "# virtualenv and virtualenvwrapper"
echo "export WORKON_HOME=$HOME/.virtualenvs"
echo "source /usr/local/bin/virtualenvwrapper.sh"

echo ""
read -p "Type 'Y' if your .bashrc contains these lines of code AND HAS BEEN SOURCED: " -n 1 -r
echo  ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # exit
fi

# Update Ubuntu
echo "INSTALL OPENCV MESSAGE--Upgrading your Ubuntu..."
sudo apt-get update || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
sudo apt-get upgrade || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Upgraded!"

# Install CMAKE and other compile tools
echo "INSTALL OPENCV MESSAGE--Installing CMAKE and other compile tools..."
sudo apt-get install build-essential cmake pkg-config || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install Image I/O libraries
echo "INSTALL OPENCV MESSAGE--Installing image I/O libs..."
sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install Video I/O libraries
echo "INSTALL OPENCV MESSAGE--Installing video I/O libs..."
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
sudo apt-get install libxvidcore-dev libx264-dev || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install OpenCV GUI dependencies
echo "INSTALL OPENCV MESSAGE--Installing GUI libs..."
sudo apt-get install libgtk-3-dev || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install matrix dependencies
echo "INSTALL OPENCV MESSAGE--Installing matrix libs..."
sudo apt-get install libatlas-base-dev gfortran || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install Python development headers
echo "INSTALL OPENCV MESSAGE--Installing Python 2.7 development headers..."
sudo apt-get install python2.7-dev || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Download OpenCV 3.1.0 TEMPORARILY to your home directory
echo "INSTALL OPENCV MESSAGE--Temporarily downloading OpenCV 3.1.0 to your home directory..."
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip|| { echo "INSTALL OPENCV MESSAGE--Couldn't download. Exiting..."; exit 1; }
unzip opencv.zip || { echo "INSTALL OPENCV MESSAGE--Couldn't unzip. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Downloaded and extracted OpenCV 3.1.0!"

# Download OpenCV 3.1.0 Contrib packages TEMPORARILY to your home directory
echo "INSTALL OPENCV MESSAGE--Temporarily downloading OpenCV 3.1.0 Contrib to your home directory..."
cd ~
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip || { echo "INSTALL OPENCV MESSAGE--Couldn't download. Exiting..."; exit 1; }
unzip opencv_contrib.zip || { echo "INSTALL OPENCV MESSAGE--Couldn't unzip. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Downloaded and extracted OpenCV 3.1.0 Contrib!"

# Set up your virtual environment for OpenCV 3.1.0 Python
source ~/.bashrc

echo "INSTALL OPENCV MESSAGE--Creating a Python virtual environment called 'cv'..."
mkvirtualenv cv -p python2 || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Created!"

echo "INSTALL OPENCV MESSAGE--Installing NumPy into the 'cv' virtual environment..."
workon cv
pip install numpy || { echo "INSTALL OPENCV MESSAGE--Failed. Exiting..."; exit 1; }
echo "INSTALL OPENCV MESSAGE--Installed!"

# Install OpenCV 3.1.0
echo "INSTALL OPENCV MESSAGE--Prepping OpenCV 3.1.0..."
cd ~/opencv-3.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D INSTALL_C_EXAMPLES=OFF \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
-D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
-D ENABLE_PRECOMPILED_HEADERS=ON \
-D BUILD_EXAMPLES=OFF .. || { echo "INSTALL OPENCV MESSAGE--CMAKE failed. Exiting..."; exit 1; }

echo "INSTALL OPENCV MESSAGE--Installing OpenCV 3.1.0 to your system..."
make -j$(nproc) || { echo "INSTALL OPENCV MESSAGE--make failed. Exiting..."; exit 1; }
sudo make install || { echo "INSTALL OPENCV MESSAGE--make install failed. Exiting..."; exit 1; }
sudo ldconfig
echo "INSTALL OPENCV MESSAGE--System installation complete!"

# Install OpenCV 3.1.0 Python bindings into virtual environment
echo "INSTALL OPENCV MESSAGE--Installing Python2.7 bindings for OpenCV 3.1.0 into your 'cv' virtual environment."
workon cv
cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

# Delete temporary install files
echo "INSTALL OPENCV MESSAGE--Cleaning up..."
cd ~
rm -rf opencv-3.1.0 opencv_contrib-3.1.0 opencv.zip opencv_contrib.zip
echo "INSTALL OPENCV MESSAGE--Done."

echo ""
echo "Full installation of OpenCV 3.1.0 should be complete."
echo "Try importing OpenCV in the Python2.7 shell from the 'cv' virtual environment."
