---
layout: kbase_article
title: Setting up Intel-Caffe on the Intel vLab cluster
---

If you want to install caffe on your access node or local, the steps that you need to follow are:

1. Login to the cluster
2. Create a directory where you want to install caffe. (mkdir <directory name> )
3. you can check that git is installed by the command : git --version 
4. Clone the repository from https://github.com/intel/caffe and NOT the link given in the university guide. git clone  https://github.com/intel/caffe
5. Change directory to the location where the Caffe optimized for Intel architecture repository is cloned
and build the framework to use Intel® Math Kernel Library for Deep Neural Networks (Intel® MKL-DNN) APIs which provide optimized implementations of convolution, pooling, normalization, and other key DNN operations on Intel Xeon Phi processor x200. After performing the instructions below you will have a binary, named caffe, at ~/caffe/build/tools/ (assuming the repository is cloned to ~/caffe):
Copy Makefile.config.example to Makefile.config using the command:
   cp Makefile.config.example Makefile.config

6. Now, to open or edit the new Makefile.config file, you can use vim Makefile.config. 
7. use ‘i’ key for intert mode, esc key to come out of insert mode, :wq to save and exit.
   Add the following lines:
  
   USE_MPI := 1
   CXX := /opt/intel/compilers_and_libraries_2017.1.132/linux/mpi/intel64/bin/mpicxx
   
8. To run use the following command from the university guide:	make -j44

To install caffe with intel optimized MKLDNN, please follow these steps:

1. Login to the cluster
2. Change to the directory in where you want your version of caffe to be built
3. Clone the intel/caffe command using the following command:

    ``` git clone https://github.com/intel/caffe.git ```
4. Change into the caffe directory. From here on, this will be refered to as the caffe root

    ``` cd caffe```
5. Make a new directory called build and change into it.

    ``` 
    mkdir build 
    cd build 
    ```

6. Run the following cmake command.  Note that it is recommended to copy and paste this (use ctrl-shift-v to paste in terminal).
    ```
    cmake -DCMAKE_BUILD_TYPE=Release -DUSE_MKLDNN_AS_DEFAULT_ENGINE=OFF -DUSE_MKL2017_AS_DEFAULT_ENGINE=OFF -DUSE_GITHUB_MKLDNN=ON ..
    ```
7. Run the following make command.  It will fail, but it is required to run it once before the next step.
    ```
    make all -j8 && make install
    ```
8. Once it fails, move back into your caffe root
9. Execute the following command:
    ```
    find . -name "mkl_dnn_types*"
    ```
    It should return something like the following:
   ```
   ./external/mkl/mklml_lnx_2018.0.20170425/include/mkl_dnn_types.h
    ```
10. Change directory into the folder returned from your find command.  Note that you should remove the mkl_dnn_types.h from your cd command.  The command you execute should be similar to the following:
    ```
    cd ./external/mkl/mklml_lnx_2018.0.20170425/include/
    ```
    Note that you may need to change this depending on the output of your find command.

11. Use pwd to get the absolute path to this directory.
    ```
    pwd
    ```
    This should return something similar to:
    ```
    /export/purdue/caffe/external/mkl/mklml_lnx_2018.0.20170425/include
    ```
    or 
    ```
    /homes/jlaiman/caffe/external/mkl/mklml_lnx_2018.0.20170425/include
    ```
    Copy the output of this command to a text file.  

12. Change directory back to your caffe root.
13. Use a text editor to open /include/mkl_dnn_cppwrapper.h
    ```
    vim include/mkl_dnn_cppwrapper.h
    ```
14. You should see includes for mkl_dnn_types.h, mkl_dnn.h, and mkl_version.h on lines 44 through 46.
    ```
    44   #include "mkl_dnn_types.h"
    45   #include "mkl_dnn.h"
    46   #include "mkl_version.h"
    ```
    Add the absolute path you just copied to a text file to the beginning of these includes so that it looks similar to the lines below.      
    ```
    44   #include "/homes/jlaiman/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_dnn_types.h"
    45   #include "/homes/jlaiman/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_dnn.h"
    46   #include "/homes/jlaiman/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_version.h"
    ```
    or
    ```
    44   #include "/export/purdue/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_dnn_types.h"
    45   #include "/export/purdue/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_dnn.h"
    46   #include "/export/purdue/caffe/external/mkl/mklml_lnx_2018.0.20170425/include/mkl_version.h"
    ```
    Note that this will depend on where are installing caffe.  
15. Change directory back into your build directory and redo the make command.
    ```
    cd build
    make all -j8 && make install
    ```
16. You should now have a functioning version of caffe build with MKLDNN optimized for intel Xeon and Xeon Phi processers.  If you would like, you can try to do a test, but I have not ran it successfully yet. This should be executed in the build directory.  
    ```
    make runtest
    ```
