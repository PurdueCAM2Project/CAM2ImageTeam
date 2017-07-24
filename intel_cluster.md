---
layout: kbase_article
title: Guide to the Intel Knights Landing vLab computing cluster
---



# Intel Cluster vLab guide
The Intel vLab Knights Landing cluster is a vital tool for our research project.
The guide they publish is helpful, but can be confusing at times. 
This document is intended to help users learn how to use the 
cluster.  It can be used as a supplement to the guide they 
provide, or as a standalone guide that will teach you everything 
you need to know.

-------

## Contents
* [Logging in to the cluster](#logging-in-to-the-cluster)
* [Using the PBS Scheduler](#using-the-pbs-scheduler)
* [Running simple example jobs](#running-simple-example-jobs)
* [Installing local packages](#installing-local-packages)
* [Helpful websites for more advanced topics](#helpful-websites-for-more-advanced-topics)


## Logging in to the cluster
Once you have an account and have setup your two-factor authentication, you are ready to log in.  To log in, you should open a terminal and enter the following command:
```
ssh "user"@ssh-iam.intel-research.net
```
Make sure to replace "user" with your intel cluster username.  If it's the first time you've logged in, it will ask you if you want to add the RSA key for the cluster.  Make sure to type in 'yes'.  After that, it will ask you for your password.  Once you have successfully entered your password, it will ask you to choose a form of two factor authentication.  If you have setup the DUO app on your phone, you will be able to use the DUO push, which will allow you to authenticate with the app.  Otherwise, it will offer to call or text you a code to enter.

> **TIP:** Once you've logged in, you can edit your ```.bashrc``` so that when you use the arrow keys to flip through your command history on the terminal, you can filter search by typing in letters. See the [team's Linux tips page](linux_tips) for more details.


## Using the PBS Scheduler
Most things you do on the cluster: Vimming, test-compiling, etc. is done from your access node.

However, when you're ready to run your program with the cluster's full power, you will need to submit a job via the PBS Scheduler.

### 1. Create a Bash script
Any bash script submitted to the cluster should be written  with these three lines of code at the top of the file:

```
#!/bin/bash
#PBS -l select=1:ncpus=272 -lplace=excl

cd [ABSOLUTE PATH TO DIRECTORY OF EXECUTABLE]
```

The cluster has 256 nodes.  You may choose to run your job on more nodes by changing the ```select``` value.

> **IMPORTANT:** The ```cd``` is *very, very important.*  Otherwise, the job will fail to execute because none of your relatively-pathed dependencies can be located.  You can exclude the cd, but the tradeoff is that you will need to have full paths to all of your files.  Depending on the complexity of the program, using ```cd``` may be significantly easier.  

A job submit bash script might look like:
```
#!/bin/bash
#PBS -l select=32:ncpus=272 -lplace=excl

cd ~/somedir/wheremypythonscript/is/
python dostuff.py
```

### 2. Submit the job
Run
```
qsub [YOUR BASH SCRIPT].sh
```
The PBS Scheduler will return a string that looks something like this:
```#####.iam-pbs1```.  That is your Job ID.

### 3. Monitor the job
To call up basic information about all the jobs you've submitted that are running on the cluster, run
```
qstat -u [USERNAME]
```

To call up detailed information about a specific job, run
```
qstat -f [JOB ID]
```

### 4. Review the job's output
When the job finishes, anything it wrote to ```stderr``` will be dumped into a file called "[YOUR BASH SCRIPT].sh.e#####".  Anything it wrote to ```stdout``` will be dumped into "[YOUR BASH SCRIPT].sh.o#####"
> **Tip:** As you can imagine, your working directory can quickly become cluttered with those dump files.  Add an aliased command that you can periodically run inside the directory to clean it all up:
```rm -f ./*.sh.*```

-------

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

------

## Installing local packages
If you need a Python dependency that isn't already present on the cluster, you can install the dependency to your user (no ```sudo``` needed) and it'll work when you submit to the cluster.

The key is ```--user```

For example:
```
pip2 install --user [PACKAGE]
````
or
```
easy_install --user [PACKAGE]
````
------

## Helpful Websites for More Advanced Topics
- [PBS scheduler guide](http://www.pbsworks.com/pdfs/PBSProUserGuide13.1.pdf)
- [SGE reference manual](http://gridscheduler.sourceforge.net/htmlman/manuals.html)