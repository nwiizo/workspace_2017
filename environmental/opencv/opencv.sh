#!/bin/bash

cd ~
wget -O opencv-3.0.0.zip https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip opencv-3.0.0.zip
cd opencv-3.0.0
mkdir build
cd build
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_PYTHON_EXAMPLES=ON -D PYTHON_EXECUTABLE=$(which python3) -D BUILD_opencv_python3=ON -D BUILD_opencv_python2=ON BUILD_EXAMPLES=ON -D WITH_FFMPEG=OFF -D  BUILD_opencv_java=OFF BUILD_opencv_test_java=OFF ..
sudo make
sudo make install
sudo echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf
sudo echo "/usr/lib" >> /etc/ld.so.conf.d/opencv.conf
sudo ldconfig 
ldconfig -v
sudo ldconfig -v
python3 -c "import cv2;print(cv2.__version__)" 
