#/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

CAFFE_ROOT=/homes/jlaiman/caffe/
PYTHONPATH=/homes/jlaiman/caffe/python
DATAPATH=/homes/jlaiman/data/ssd/


/homes/jlaiman/caffe/build/tools/caffe train -solver examples/ssd/VGGNet/VOC0712/SSD_300x300/solver.prototxt -weights examples/ssd/VGGNet/VGG_ILSVRC_16_layers_fc_reduced.caffemodel


