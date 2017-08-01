#This guide and the bash script included above is for open cv installation. Before running the script, it is recommended that you open and read it once, as it has some special cases. It is written for python 2.7 and open cv 3.1 installation. If you need to install it with different versions, follow the directions in link specified in the script file

#Please execute the following on your commandline BEFORE running the script for opencv  installation

cd ~
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
	
source ~/.bashrc
mkvirtualenv cv -p python2

#Now check if the virtual environment has been created properly. Run the follwoing command
workon cv


#After running Make command during opencv buidling, IF YOU ARE GETTING HDF5.H ERROR THEN EXECUTE THE FOLLOWING STEPS:
#Go to the following location: modules/python/common.cmake 
# add the following lines at the end of the file

#find_package(HDF5)
#include_directories(${HDF5_INCLUDE_DIRS})

# run the command : 
make clean
#Run the cmake command again
#proceed with the rest of the installation

Finally, test if opencv has installed correctly by trying to import it

cd ~
workon cv
python
import cv2
cv2.__version__

You should get results similar to the following :

Python 2.7 (default, Jul  5 2016, 12:43:10) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'3.1.0'
>>>
