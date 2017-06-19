# Intel Cluster vLab guide
The Intel vLab cluster is a vital tool for our research project.  The guide they publish is helpful, but can be confusing at times.  This document is intended to help users learn how to use the cluster.  It can be used as a supplement to the guide they provide, or as a standalone guide that will teach you everything you need to know.  

## Running simple example jobs
The following examples are meant to be a 
### Caffe
To begin, create a 
```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
source /opt/intel/compilers_and_libraries_2017/linux/mpi/intel64/bin/mpivars.sh
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
numactl -p 1 /export/software/caffe/build/tools/caffe time -engine "MKL2017" -model
/export/software/caffe/models/bvlc_alexnet/train_val_dummy.prototxt 2>&1 | tee ~/caffe_singlenode.txt
```

```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
. /export/software/torch/install/bin/torch-activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/compilers_and_libraries_2017.1.132/linux/compiler/lib/intel64_lin/
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
cd /export/software/torch/Optimized-Torch-benchmark/numactl -p 1 th benchmark_mkldnn.lua 2>&1 | tee ~/torch_singlenode.txt
```

```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/export/software/mxnet/mkl/lib/
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
cd /export/software/mxnet/example/image-classification numactl -p 1 python benchmark_score.py 2>&1 | tee ~/mxnet_singlenode.txt
```








http://www.pbsworks.com/pdfs/PBSProUserGuide13.1.pdf
http://gridscheduler.sourceforge.net/htmlman/manuals.html