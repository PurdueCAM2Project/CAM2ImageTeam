# Intel Cluster vLab guide
The Intel vLab cluster is a vital tool for our research project.  
The guide they publish is helpful, but can be confusing at times. 
This document is intended to help users learn how to use the 
cluster.  It can be used as a supplement to the guide they 
provide, or as a standalone guide that will teach you everything 
you need to know.  

## Running simple example jobs
The following examples are to provided to illustrate running a 
job in the cluster using the PBS scheduler.  They are simple 
and not meant to be a complete guide to the PBS scheduler.  

### Single Node Caffe Example
To begin, create a script named 
"caffe_alexnet_singlenode_dummy.sh" with the following contents.  
```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
source /opt/intel/compilers_and_libraries_2017/linux/mpi/intel64/bin/mpivars.sh
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
numactl -p 1 /export/software/caffe/build/tools/caffe time -engine "MKL2017" -model
/export/software/caffe/models/bvlc_alexnet/train_val_dummy.prototxt 2>&1 | tee ~/caffe_singlenode.txt
```
Once you have created this file, make it executable and submit 
it to the cluster using the following commands.

```
chmod +x ./caffe_alexnet_singlenode_dummy.sh
qsub ./caffe_alexnet_singlenode_dummy.sh
```
Once the job has completed, you will see several new files in the
directory from which you submitted the job.  They will be 
caffe_alexnet_singlenode_dummy.sh.e#, 
caffe_alexnet_singlenode_dummy.sh.o# where # is the 
job number, and caffe_singlenode.txt.  The .e file contains any 
output from stderr.  The .o file contains any output from 
stdout.  If the job finished successfully, caffe_singlenode.txt 
will be a long file with the output of your program.  

### Single Node Torch Example
To begin, create a script named 
"torch_alexnet_singlenode_dummy.sh" with the following contents.

```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
. /export/software/torch/install/bin/torch-activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/compilers_and_libraries_2017.1.132/linux/compiler/lib/intel64_lin/
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
cd /export/software/torch/Optimized-Torch-benchmark/numactl -p 1 th benchmark_mkldnn.lua 2>&1 | tee ~/torch_singlenode.txt
```
Once you have created this file, make it executable and submit 
it to the cluster using the following commands. 
```
chmod +x ./torch_alexnet_singlenode_dummy.sh
qsub ./torch_alexnet_singlenode_dummy.sh
``` 
Like with the caffe example, you will have several new files 
in the directory from which you submitted the job. 

### Single Node MXNet Example
To begin, create a script named 
"mxnet_alexnet_singlenode_dummy.sh" with the following contents.

```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/export/software/mxnet/mkl/lib/
export OMP_NUM_THREADS=68;
export KMP_AFFINITY=granularity=fine,compact,1,0;
cd /export/software/mxnet/example/image-classification numactl -p 1 python benchmark_score.py 2>&1 | tee ~/mxnet_singlenode.txt
```
Again, make it executable and submit it to the cluster using 
the following commands.
```
chmod +x ./mxnet_alexnet_singlenode_dummy.sh
qsub ./mxnet_alexnet_singlenode_dummy.sh
``` 
As with the previous two examples, there should be several new 
files in the directory from which you submitted the job.  


## Helpful Websites for Reference
http://www.pbsworks.com/pdfs/PBSProUserGuide13.1.pdf
http://gridscheduler.sourceforge.net/htmlman/manuals.html