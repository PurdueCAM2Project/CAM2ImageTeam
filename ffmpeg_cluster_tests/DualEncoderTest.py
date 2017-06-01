# CAM2 Project Image Team- http://www.cam2project.net
# Author: Caleb Tung
# Brief: This script is used to simulate runtimes of downloading frames from a livestream cam while
#        simultaneously saving them to a disk using FFmpeg
#        and then performing image analysis using Python as each new frame rolls in

import subprocess
from PIL import Image
import numpy
import sys

EXPECTED_ARG_CT = 5 + 1
RGB_CT = 3

# Collect cmd args
if len(sys.argv) != EXPECTED_ARG_CT:
    print('Not enough command line args')
    exit()

SRC_URL = sys.argv[1]
SECONDS_OF_FRAMES = int(sys.argv[2])
FPS = int(sys.argv[3])
WIDTH_RES = int(sys.argv[4])
HEIGHT_RES = int(sys.argv[5])

commandStr = 'ffmpeg -i ' + SRC_URL + ' -t ' + str(SECONDS_OF_FRAMES) + ' -f image2pipe -vcodec rawvideo -pix_fmt rgb24 - -vcodec png DiskFrames/frame%0d.png'
command = commandStr.split()

pipe = subprocess.Popen(command, stdout=subprocess.PIPE)

for i in range(1, 1+SECONDS_OF_FRAMES*FPS):
    rawImage = pipe.stdout.read(WIDTH_RES*HEIGHT_RES*RGB_CT)
    
    # Generate 3D numpy array
    imageArr = numpy.fromstring(rawImage, dtype='uint8')
    imageArr = imageArr.reshape((HEIGHT_RES, WIDTH_RES, RGB_CT))

    # Run Image analysis (use making a file as a dummy 'image analysis')
    img = Image.fromarray(imageArr)
    img.save('DummyImageAnalysis/frame' + str(i) + '.png') # Saves

pipe.kill()