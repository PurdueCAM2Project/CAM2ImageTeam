Darknet
--------
Darknet is an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues about Darknet, please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).


CAM2 Image Team Augmentations
-------

The YOLO detector was modified to run object detection on multiple objects.  This can be run with the command:
```
./darknet batch [CONFIG FILE] [WEIGHTS FILE] -in [INPUT FILE] -out [OUTPUT FILE] -thresh [DESIRED MIN CONFIDENCE]
```
The input file is a text file that lists all the images in the batch (each image path should get its own line in the file; see images.txt for example).

An example of this command is:
```
./darknet cfg/yolo.cfg yolo.weights -in images.txt -out imagesresult.txt -thresh 0.25
```
> **NOTE:** "yolo.weights" can be obtained via ```wget https://pjreddie.com/media/files/yolo.weights```

> **CAM2 EDITS:** Changes to the source code to implement batch processing can be found in "examples/darknet.c," "examples/detector.c," and "include/darknet.h"  The changes are indicated with a comment block that says "CAM2 IMAGE TEAM AUGMENTATIONS FOR BATCH PROCESSING."
