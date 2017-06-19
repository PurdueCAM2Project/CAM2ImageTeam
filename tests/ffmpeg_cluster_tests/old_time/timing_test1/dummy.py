import subprocess
from PIL import Image
import numpy

SECONDS_OF_FRAMES = 1
FPS = 30

commandStr = 'ffmpeg -i http://video3.earthcam.com/fecnetwork/9974.flv/chunklist_w1220748217.m3u8 -f image2pipe -t ' + str(SECONDS_OF_FRAMES) + ' -pix_fmt rgb24 -vcodec rawvideo -'

command = commandStr.split()
pipe = subprocess.Popen(command, stdout=subprocess.PIPE)


for i in range(1, 1+SECONDS_OF_FRAMES*FPS):
    rawImage = pipe.stdout.read(1280*720*3)
    
    # Generate numpy array
    imageArr = numpy.fromstring(rawImage, dtype='uint8')
    imageArr = imageArr.reshape((720, 1280, 3))

    # Save frame
    img = Image.fromarray(imageArr) # WE CAN ALSO DO IMAGE PROCESSING AT THIS STAGE
    img.save('frame' + str(i) + '.png') # Saves

pipe.kill()
