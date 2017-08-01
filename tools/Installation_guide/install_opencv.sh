#!/bin/bash
# author : Aparna Pidaparthi
# email: apidapar@purdue.edu
# this script has been compiled from the following website- please refer to the same for detailed explanation or if you encounter any problem
#http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev

sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev

sudo apt-get install libgtk-3-dev

sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3.5-dev

cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv_contrib.zip

workon cv
pip install numpy
workon cv
cd ~/opencv-3.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON \
	-D ENABLE_PRECOMPILED_HEADERS=OFF ..

make -j$(nproc)

#AT THIS POINT IF YOU ARE GETTING HDF5.H ERROR THEN EXECUTE THE FOLLOWING STEPS:
#Go to the following location: modules/python/common.cmake 
# add the following lines at the end of the file

#find_package(HDF5)
#include_directories(${HDF5_INCLUDE_DIRS})

# Now, ensure you are in the build directory 
# run the command : make clean
# run the cmake and make commands again
# If it runs smoothly,proceed with the following steps:

sudo make install
sudo ldconfig
ls -l /usr/local/lib/python2.7/site-packages/

cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so


