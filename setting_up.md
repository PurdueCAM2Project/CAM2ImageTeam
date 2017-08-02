---
layout: kbase_article
title: Setting up your environment
---

# Setting up your environment
The CAM² research group relies on a variety of libraries and tools to facilitate research and development. As a new member of the Image Team, you'll want to run through the setup in this guide to get up and running on your personal computer.

---

## Setting up a virtual machine
> **NOTE:** If you are already running Ubuntu 16.04, you can skip this.

The Image Team does its work almost exclusively with Linux. But we recommend that you **do not** boot exclusively to a Linux distro.  Instead, run a Linux virtual machine atop a better "everyday-driver" operating system like Windows or macOS. Some software applications (*e.g.* Skype and Slack) are either in beta and/or not very well-supported on Linux.

This guide will teach you to install an Ubuntu 16.04 LTS virtual machine. This is the version of Ubuntu that has been tested with all of our development tools.

> **WARNING:** Other Linux distributions _have not been tested_ for this setup guide; using Ubuntu 16.04 is strongly recommended.

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads), Oracle's virtualization software.

> **NOTE:** If you're running Windows 10 Pro and were hoping to use Hyper-V for native virtualization, don't. Sadly, it doesn't play well with Ubuntu. Trust us, we've tried.

2. Download the ISO for Ubuntu 16.04 LTS [here](https://www.ubuntu.com/download/desktop).
3. Configure the virtual machine to your liking (we recommend allocating at least 32GB to the virtual hard drive with dynamic resizing, and at least 4GB RAM with 2 CPU cores so the VM (virtual machine) won't run sluggishly).
4. Boot up the VM with the ISO file in its virtual optical drive. Follow the instructions to install Ubuntu.

Great! The rest of the tools in this guide should all be installed into your shiny new Ubuntu virtual machine.

---

## Installing OpenCV 3.1.0
The [Open Source Computer Vision Library](http://opencv.org/) powers a lot of the tech being designed by the Image Team. It's very important that you install this.
1. Based on the excellent step-by-step tutorial found at [PyImageSearch](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/), we've written a shell script that will install OpenCV 3.1.0 for you. Grab it [here](https://github.com/PurdueCAM2Project/CAM2ImageTeam/blob/master/tools/install_opencv_3.1.0.sh).

2. Enable execution of the shell script on your machine:

```
cd "the directory where the script is located"
chmod +755 install_opencv_3.1.0.sh
```

3. Run the script:
    ```
    bash -i install_opencv_3.1.0.sh
    ```
    The script should run, installing Python virtual environment tools. Then, it will prompt you to make changes to your `.bashrc`.  Type <kbd>N</kbd> to stop the script.
    > **NOTE:** This script will need to run several commands as `root`, so be prepared to enter your `sudo` password.

4. Add the following to your `.bashrc` file (type `gedit ~/.bashrc` to open the file with the gedit editor):

    ```
    # virtualenv and virtualenvwrapper
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
    ```

5. Source it:

    ```
    source ~/.bashrc
    ```
    Some text about installing a virtual environment should scroll across the screen.

6. Run the script a second time.  This time, type <kbd>Y</kbd> at the prompt to proceed with the installation. As the installation proceeds, it may prompt you to install certain packages; type <kbd>Y</kbd> followed by <kbd>Enter</kbd> to continue.

    >**NOTE:** This script follows good Pythonic practice of using virtual environments. Therefore, it will install the Python bindings for OpenCV 3.1.0, along with NumPy, into a virtual environment called `cv`. Outside of that environment, the Python bindings will be unavailable.

7. Once the installation completes successfully, confirm that the Python bindings were installed correctly. Enter your virtual environment with:

    ```
    workon cv
    ```

    Now, open a Python 2 shell, then try:

    ```
    import cv2
    cv2.__version__
    ```

    Python should print `3.1.0` to the terminal.
    
You're done!

---

## Installing Caffe
Developed by the AI Research group at UC Berkeley, [Caffe](http://caffe.berkeleyvision.org/) is a fast, deep learning framework being used by the Image Team. This install guide is based on the one found [here](https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide).

> **WAIT!** Make sure you've installed OpenCV 3.1.0 before proceeding.

> **NOTE:** This guide brews Caffe for CPU only.

1. First, update your Ubuntu and install all dependencies:

    ```
    sudo apt-get update

    sudo apt-get upgrade

    sudo apt-get install -y build-essential cmake git pkg-config

    sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler

    sudo apt-get install -y libatlas-base-dev 

    sudo apt-get install -y --no-install-recommends libboost-all-dev

    sudo apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev

    sudo apt-get install -y python-dev
    ```

2. Hop into your Python virtual environment created when you installed OpenCV, then install SciPy:

    ```
    workon cv
    pip install scipy
    ```

3. Download the archive for Caffe 1.0.0-RC5 [here](https://github.com/BVLC/caffe/archive/rc5.zip). Extract it somewhere you plan to keep it.

4. Inside the `caffe-rc5` directory, duplicate the `Makefile.config.example` into `Makefile.config`.

5. Edit `Makefile.config`:
    - Uncomment this line: `CPU_ONLY := 1` to brew Caffe without GPU support.
    - Uncomment this line: `OPENCV_VERSION := 3` to use your install of OpenCV.
    - Change the `LIBRARY_DIRS` line to read as:

        ```
        LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial /usr/local/share/OpenCV/3rdparty/lib/
        ```

    - Uncomment this line: `WITH_PYTHON_LAYER := 1` to build with support for PyCaffe (the Python bindings for Caffe).
    - Edit the `INCLUDE_DIRS` line to read as:

        ```
        INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
        ```

    - Edit the `PYTHON_INCLUDE` line to read as:

        ```
        PYTHON_INCLUDE := /usr/include/python2.7 /usr/local/lib/python2.7/dist-packages/numpy/core/include
        ```

    Save the `Makefile.config`.

6. Now, edit the `Makefile`. Find this line:

    ```
    NVCCFLAGS += -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
    ```

    And replace it with this:

    ```
    NVCCFLAGS += -D_FORCE_INLINES -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
    ```

    Then, find this line:

    ```
    LIBRARIES += glog gflags protobuf boost_system boost_filesystem m hdf5_hl hdf5
    ```

    And replace it with this:

    ```
    LIBRARIES += glog gflags protobuf leveldb snappy \
    lmdb boost_system boost_filesystem hdf5_hl hdf5 m \
    opencv_core opencv_highgui opencv_imgproc opencv_imgcodecs opencv_videoio
    ```

7. One more file to edit! Open `CMakeLists.txt` and add the following:
    
    ```
    # ---[ Includes
    set(${CMAKE_CXX_FLAGS} "-D_FORCE_INLINES ${CMAKE_CXX_FLAGS}")
    ```


8. Call up a terminal window and run these configuration commands:

    ```
    cd "Downloaded Caffe directory"
    find . -type f -exec sed -i -e 's^"hdf5.h"^"hdf5/serial/hdf5.h"^g' -e 's^"hdf5_hl.h"^"hdf5/serial/hdf5_hl.h"^g' '{}' \;

    cd /usr/lib/x86_64-linux-gnu

    sudo ln -s libhdf5_serial.so.10.1.0 libhdf5.so

    sudo ln -s libhdf5_serial_hl.so.10.0.2 libhdf5_hl.so 
    ```

    If you get messages like "file already exists", don't worry about it.

9. Install all remaining PyCaffe dependencies into your virtual environment:

    ```
    workon cv
    cd "Downloaded Caffe directory"
    cd python
    for req in $(cat requirements.txt); do sudo pip install $req; done
    ```

10. Finally, time to brew Caffe. Remember to use the `nproc` system variable to build with all processor cores on your PC.

    ```
    make all -j$(nproc)
    ```

11. Build and run all Caffe diagnostic tests:

    ```
    make test -j$(nproc)
    make runtest
    ```

12. Once everything checks out:

    ```
    make distribute
    ```

13. Link up PyCaffe on your PYTHONPATH. Add the following to your `~/.bashrc` file:

    ```
    export PYTHONPATH="Downloaded Location of Caffe"/python:$PYTHONPATH
    ```

    Save the file and then `source` it:
    
    ```
    source ~/.bashrc
    ```

14. Confirm that PyCaffe is brewed and ready. Pull up a Python shell with the `python` command and then type the following:

    ```
    import caffe
    caffe.__version__
    ```

    Python should print `1.0.0-rc5` to the terminal.
    
All done!

---

## Installing Git
The team manages our codebase with Git.

Install this on Ubuntu with:

```
sudo apt install git
```

> **NOTE:** You can also grab Git for Windows or Mac [here](https://git-scm.com/downloads).

## Configuring Git for work on the Image Team
1. Initialize some global settings for Git:

    ```
    git config --global user.name "Your name"
    git config --global user.email "Your email"
    git config --global core.autocrlf=input
    ```

    > **NOTE:** If using Git Bash for Windows, set the `autocrlf` setting to `true`.

2. Navigate to the Image Team's Github repo [here](https://github.com/PurdueCAM2Project/CAM2ImageTeam) and [fork it](https://help.github.com/articles/fork-a-repo/) to your personal Github.

3. Then, [clone your fork](https://help.github.com/articles/cloning-a-repository/) to your computer:

    ```
    git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
    ```

All set! Now, you can start messing with the code without worrying about breaking stuff in the team repository. Any contributions you make to the Github will be pushed to your fork and merged into the team repo later.

---

## Installing Slack
The CAM² group uses [Slack](https://slack.com/) to communicate.

Download Slack for Windows or macOS [here](https://slack.com/downloads). You can choose to get Slack for Linux Beta, but it lacks so many features that you might as well just use the [Slack web app](https://cam2.slack.com/messages) on Ubuntu.

If you prefer to use your mobile device, you can get Slack from the Windows Store, Google Play, or the App Store.

---

## Optional tools
Each member of the Image Team has personal preferences when it comes to code editors and web browsers. Feel free to use whatever you like best. If you're having trouble picking one, here are a handful of team favorites to help you along:

### Visual Studio Code (VS Code)
A lightweight, open-source, and fully-customizable code editor by Microsoft (not to be confused with Visual Studio IDE). Features include:

* A vast library of extensions that can enhance debugging and ease of use
* Intellisense autocomplete and code/docstring suggestion
* Real-time preview for Markdown files, making it very easy to write attractive, well-formatted documentation
* Git integration, allowing you to stage/commit your code and view diffs with a snappy, intuitive user interface
* Built-in terminal
* Excellent support across all platforms: Windows, macOS, and many flavors of Linux (Ubuntu included)

Install from [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download).

### Vim
An ultra-lightweight, terminal-based text editor famous for its lightning-fast keyboard shortcuts. Vimming at speed takes practice, but once you get used to it, you can edit code extremely quickly. It lacks debuggers, code autocompletion, and the like. But it's ubiquitous (basically any Linux machine can run Vim) and knowing how to use it will be very helpful whether here on the team or elsewhere.

Install this on Ubuntu with:

```
sudo apt install vim
```

### PyCharm Community
JetBrains' world-class IDE built exclusively for Python, free for use. Features include:

* Python code autocomplete
* Github integration for easy staging/committing of code
* Convenient debugging features
* A world of other useful tools for Python development
* Available for Windows, macOS, and Linux distributions like Ubuntu.

Install from [https://www.jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/).
