import threading
import time
import os
import cv2
import numpy as np
import sys, getopt
import caffe
GPU_ID = 0  # Switch between 0 and 1 depending on the GPU you want to use.
# caffe.set_mode_gpu()
# caffe.set_device(GPU_ID)
caffe.set_mode_cpu()


cores_load_max = 8*5#6
cores_download_max = 8#2
cores_yolo_max = 16#5

cores_load_current = []
cores_download_current = []
cores_yolo_current = []

loadedStreams = []
savedImagesPaths = []
global saveThreadCounter
saveThreadCounter = 0
global imagesProcessed
imagesProcessed = 0
global StartTime
StartTime = 0

# Controls the number of feeds to be opened with how many threads. Currently reads in from an input text file of
# m3u8 feeds links. Can be altered to read in from ip cameras as well
def loadStreams():
  streamsDatabase = open("m3u8s3.txt")
  for line in streamsDatabase:
    t = threading.Thread(target=loadStream, args=(line,))
    t.start()
    cores_load_current.append(t)


# Function to load one individual stream. Called from the loadStreams function, which controls threading for loading
# image feeds.
def loadStream(url):
  cap = cv2.VideoCapture(url)
  if (cap.isOpened()):
    loadedStreams.append(cap)
  cores_load_current.pop()


# Downloads images by running through the list of streams loaded previously and calling new threads (up to teh maximum
# number specified) to download 100 images at a time from each of the streams, then free up the thread. Once a thread
# is freed, it will load the next item in the list of loadedStreams and begin downloading images from that feed
def downloadImages():
  print ("Downloading images")
  threadNo = 0
  for x in range(len(loadedStreams)):
    opened = False
    while (not opened):
      if (len(cores_download_current) < cores_download_max):
        t = threading.Thread(target=downloadImage, args=(loadedStreams[x], threadNo,))
        t.start()
        threadNo += 1
        cores_download_current.append(t)
        opened = True
      else:
        time.sleep(0.01)


# Downloads 100 images from a specified stream. This function is called from the downloadImages function, which
# controlls threading, and decides which stream the threads should download from
def downloadImage(stream, threadNo):
  path = "/home/ryan/Documents/Summer_Research/mMaster/imageOutput"
  for x in range(300):
     frame = stream.read()[1]
     filename = ("z_" + "iterationNumber" + str(saveThreadCounter) + "threadNumber" + str(threadNo) + "iamgeNumber" + str(x) + ".jpg")
     fullpath = os.path.join(path, filename)
     cv2.imwrite(str(fullpath), frame)
     savedImagesPaths.append(fullpath)
  cores_download_current.pop()


def loadAnalysis():
  model_filename = "prototxt/yolo_small_deploy.prototxt"
  weight_filename = "/home/ryan/Documents/Summer_Research/yolo_small.caffemodel"

  net = caffe.Net(model_filename, weight_filename, caffe.TEST)

  transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
  transformer.set_transpose('data', (2, 0, 1))

  for x in range(cores_yolo_max):
    t = threading.Thread(target=analyze, args=(net, transformer,))
    t.start()

def analyze(net, transformer):
  while True:
    breaker = False

    try:
      img_filename = savedImagesPaths.pop()
      img = caffe.io.load_image(img_filename)  # load the image using caffe io
      inputs = img
      out = net.forward_all(data=np.asarray([transformer.preprocess('data', inputs)]))

      global imagesProcessed
      imagesProcessed += 1

      global startTime
      avg_fps = imagesProcessed / (time.time()-startTime)
      print '\nFILE: {0} Running Average: {1} FPS'.format(img_filename, avg_fps)
      # print out.iteritems()
      img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
      results = interpret_output(out['result'][0], img.shape[1], img.shape[0])  # fc27 instead of fc12 for yolo_small
      show_results(img_cv, results, img.shape[1], img.shape[0])
    except Exception as e:
      if e == KeyboardInterrupt:
        print ("breakingbreakingbreakingbreaking")
        breaker = True
        break
      print e
      time.sleep(0.25)
    if breaker:
      break


def interpret_output(output, img_width, img_height):
  classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
             "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
  w_img = img_width
  h_img = img_height
  # print w_img, h_img
  threshold = 0.2
  iou_threshold = 0.5
  num_class = 20
  num_box = 2
  grid_size = 7
  probs = np.zeros((7, 7, 2, 20))
  class_probs = np.reshape(output[0:980], (7, 7, 20))
  #	print class_probs
  scales = np.reshape(output[980:1078], (7, 7, 2))
  #	print scales
  boxes = np.reshape(output[1078:], (7, 7, 2, 4))
  offset = np.transpose(np.reshape(np.array([np.arange(7)] * 14), (2, 7, 7)), (1, 2, 0))

  boxes[:, :, :, 0] += offset
  boxes[:, :, :, 1] += np.transpose(offset, (1, 0, 2))
  boxes[:, :, :, 0:2] = boxes[:, :, :, 0:2] / 7.0
  boxes[:, :, :, 2] = np.multiply(boxes[:, :, :, 2], boxes[:, :, :, 2])
  boxes[:, :, :, 3] = np.multiply(boxes[:, :, :, 3], boxes[:, :, :, 3])

  boxes[:, :, :, 0] *= w_img
  boxes[:, :, :, 1] *= h_img
  boxes[:, :, :, 2] *= w_img
  boxes[:, :, :, 3] *= h_img

  for i in range(2):
    for j in range(20):
      probs[:, :, i, j] = np.multiply(class_probs[:, :, j], scales[:, :, i])
  filter_mat_probs = np.array(probs >= threshold, dtype='bool')
  filter_mat_boxes = np.nonzero(filter_mat_probs)
  boxes_filtered = boxes[filter_mat_boxes[0], filter_mat_boxes[1], filter_mat_boxes[2]]
  probs_filtered = probs[filter_mat_probs]
  classes_num_filtered = np.argmax(probs, axis=3)[filter_mat_boxes[0], filter_mat_boxes[1], filter_mat_boxes[2]]

  argsort = np.array(np.argsort(probs_filtered))[::-1]
  boxes_filtered = boxes_filtered[argsort]
  probs_filtered = probs_filtered[argsort]
  classes_num_filtered = classes_num_filtered[argsort]

  for i in range(len(boxes_filtered)):
    if probs_filtered[i] == 0: continue
    for j in range(i + 1, len(boxes_filtered)):
      if iou(boxes_filtered[i], boxes_filtered[j]) > iou_threshold:
        probs_filtered[j] = 0.0

  filter_iou = np.array(probs_filtered > 0.0, dtype='bool')
  boxes_filtered = boxes_filtered[filter_iou]
  probs_filtered = probs_filtered[filter_iou]
  classes_num_filtered = classes_num_filtered[filter_iou]

  result = []
  for i in range(len(boxes_filtered)):
    result.append(
      [classes[classes_num_filtered[i]], boxes_filtered[i][0], boxes_filtered[i][1], boxes_filtered[i][2],
       boxes_filtered[i][3], probs_filtered[i]])

  return result


def iou(box1, box2):
  tb = min(box1[0] + 0.5 * box1[2], box2[0] + 0.5 * box2[2]) - max(box1[0] - 0.5 * box1[2],
                                                                   box2[0] - 0.5 * box2[2])
  lr = min(box1[1] + 0.5 * box1[3], box2[1] + 0.5 * box2[3]) - max(box1[1] - 0.5 * box1[3],
                                                                   box2[1] - 0.5 * box2[3])
  if tb < 0 or lr < 0:
    intersection = 0
  else:
    intersection = tb * lr
  return intersection / (box1[2] * box1[3] + box2[2] * box2[3] - intersection)


def show_results(img, results, img_width, img_height):
  img_cp = img.copy()
  disp_console = True
  imshow = True
  #	if self.filewrite_txt :
  #		ftxt = open(self.tofile_txt,'w')
  for i in range(len(results)):
    x = int(results[i][1])
    y = int(results[i][2])
    w = int(results[i][3]) // 2
    h = int(results[i][4]) // 2
    aw = int(results[i][3]) / 2
    ah = int(results[i][4]) / 2
    if disp_console: print '    class : ' + results[i][0] + ' , [x,y,w,h]=[' + str(x - aw) + ',' + str(
      y - ah) + ',' + str(int(results[i][3])) + ',' + str(int(results[i][4])) + '], Confidence = ' + str(
      results[i][5])
    xmin = x - w
    xmax = x + w
    ymin = y - h
    ymax = y + h
    if xmin < 0:
      xmin = 0
    if ymin < 0:
      ymin = 0
    if xmax > img_width:
      xmax = img_width
    if ymax > img_height:
      ymax = img_height
    if imshow:
      #	cv2.rectangle(img_cp,(xmin,ymin),(xmax,ymax),(0,255,0),2)
      print xmin, ymin, xmax, ymax
      #	cv2.rectangle(img_cp,(xmin,ymin-20),(xmax,ymin),(125,125,125),-1)
      cv2.putText(img_cp, results[i][0] + ' : %.2f' % results[i][5], (xmin + 5, ymin - 7),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
      # if imshow :
      # 	cv2.imshow('YOLO detection',img_cp)
      # 	cv2.waitKey(1000)

if __name__ == '__main__':
  saveThreadCounter = 0
  # Initial loading of threads
  ti = time.time()
  print ("Loading Streams")
  loadStreams()
  while(len(cores_load_current) > 0):
    time.sleep(0.05)
  print ("Number of streams opened: " + str(len(loadedStreams)))

  # Initial downloading of images
  print ("Downloading initial image set")
  ti = time.time()
  downloadImages()
  while (len(cores_download_current) > 0):
    time.sleep(0.05)
  print ("Number of images downloaded: " + str(len(savedImagesPaths)))
  global startTime
  startTime = time.time()
  loadAnalysis()


  # Load yolo model

  # Looping analyzing and downloading more
  while True:
    if len(savedImagesPaths)<1000:
      print ("Downloading more images")
      downloadImages()