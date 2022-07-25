# NVBitFI-by-Time
Overhauled [NVBitFI](https://github.com/NVlabs/nvbitfi) with **explicit** control over **when** to inject faults. Users may profile the fault injection outcomes with program lifetime. 
By leveraging the **time-varying GPU program vulnerability**, users shoulbe be able to get insights on efficient soft error mitigation strategies.

## 1. Requirements
In addition to dependencies required by stock NVBITFI, this NVBitFI variant requires the following packages:
* numpy

## 2. Time-varying concerning fault injection setup instructions

Similiar to stock [NVBitFI](https://github.com/NVlabs/nvbitfi), fault injection campaigns can be mostly controlled by a set of Python scripts in this revised NVBitFI, which are located in ```nvbit/tools/nvbitfi/scripts```. 

The code structure of our customized NVBitFI implementation is shown below: 

```bash
|scripts
├── common_functions.py
├── generate_injection_list.py
├── gen_injection_utils
│   ├── group_functions.py
│   ├── injectionList_cfs.py
│   └── injectionList_generator.py
├── parameters_setup
│   ├── consolidated_parameters.py
│   └── constant_parameters.py
├── params.py
├── parse_results.py
├── run_injections.py
├── run_injection_utils
│   └── run_one_injection_helpers.py
├── run_one_injection.py
└── run_profiler.py
```

FI Parameter setups should be easier than stock NVBitFI. We have get the dependencies of *Darknet, selected Rodinia benchmarks, Selected NVDIDIA CUDA Samples applications* configured properly. To conduct fault injections on these ready to test programs, users just need to:

### 2.0. Setup a few general FI campaign parameters 
in ```scripts/params.py```, such parameters include: 
* data dumping options such as ```verbose``` mode, ```keep_logs``` or not, etc.
* Several parameter of injection campaign configs
    * Number of injections (total number of fault in each generated fault list).
    * Number of threshold jobs (For faults in each fault list, we only inject faults as many as the number of threshold jobs) in the FI campaign.
    * TImeout threshold, this threshold is compleltely depending upon the time-constraints of the concerned application or senarios. 

### 2.1. Specify the test programs, Fault model. Fault sites
Specifiy **name of tested benchmarks**, **fault models**, and the **type of instructions** to inject faults into, in ```scripts/params.py``` 

### 2.2. Choose Grouping function
By default, a naive grouping function divides the instrumented CUDA program into equally sized sequences. If you are not happy with this brute force method, you are welcome to develop more sophisticated grouping functions. When finished, just put your own grouping function in ```scripts/gen_injection_utils/group_functions.py```. The grouping function is passed to ```script/gen_injection_list.py``` as an *HOF*. Therefore, additional experssions should be added in ```script/gen_injection_list.py``` to specify which grouping function to use.

### 2.3. Configure FI scope, resolution of time-varying vulnerability
When using the naive grouping function, users need to specify two configurable variables: **scope** and **groups** in ```nvbit/tools/nvbitfi/test.sh```
*  **scope** specifies the granularity of FI campaign, user should choose a scope from ```'vanilla'```, ```'insts'```, or ```'kernels'```:
    * ```vanilla```: The default FI campaing implemented in stock-NVBITFI, **time-varying vulnerability** is not considered in this mode. After all, faults are distributed uniformly across the entire program lifetime. Typically, no statistically siginificant time varying vulnerability behaviors can be observed. 
    * ```insts```: Dividing the program into equally sized groups by the total instruction count. FI in this scope is suitable for exploring the instruction-level time-varying vulnerability for a smaller benchmark, or a single CUDA kernel.
    * ```kernels```: Dividing the program into equally sized groups by the total kernel count. FI in this scope is suitable for analyzing the real world larger applications, or those applications that instantiate many dynamic kernels.

* **groups** means the how many equally-sized code pieces that the program is divided into. This argument determines the resolution of the time-varying vulnerability we are going to measure. 
    * Typically, a larger group number gives a better and a more accurate modeling of time-varying behavior, but time required for FI campaign can be much longer. A smaller number of FI allows faster FI campaign but the accuracy of time-varying vulnerabiliy is limited.  

Depending on the programs under test or the goal of FI experiment, users can choose the *most* appropriate FI **scope** and **groups**

### 2.4 Run FI
Simply cd to ```nvbit/tools/nvbitfi```, and run ```./test.sh```. Or created your own bash scripts for FI control. 

## 3. Prepare Programs under test
Though we offered tens of ready-to-launch test programs, users can also test their own benchmarks. The steps of how to add new testbenches are:
### 3.1. Understanding the structure of ```test-apps directory```
Let's assume we have already got the binary executables **ready** (the steps of how to compile source codes in-place will be discussed later)

First, ```cd``` to ```nvbit/tools/nvbitfi/test-apps```; 
An example of test-apps directory is shown below:
```bash
├── bfs
├── darknet1img
├── darknet1img_tiny
├── darknet1img_yolov4
├── gaussian
├── hotspot
├── kmeans
├── lud
├── nn
├── nw
├── test-apps-dependencies
│   ├── cudaSample_Common
│   ├── darknet_data
│   ├── rodinia_common
│   └── rodinia_data
└── vectorAdd
    ├── vectorAdd1024_16
    └── vectorAdd32_64
```
Where: 
* ***bfs; darknet1img; gaussian; hotspot; ...... nw*** are "regular" benchmarks. Each of benchmark directory should contain the following files at least: 
    * Binary excecutable
    * ```run.sh``` shell script
    * sdc checker ```sdc_check```
    * Makefile (not have to be a **"complete"** Makefile) to generate golden references. 
    * Necessary dependencies like input files
    
    For example, this is what it looks like in ```test-apps/bfs```
    ```bash
    ├── bfs
    ├── bfs.cu
    ├── golden_stderr.txt
    ├── golden_stdout.txt
    ├── graph4096.txt
    ├── kernel2.cu
    ├── kernel.cu
    ├── Makefile
    ├── Makefile_nvidia
    ├── README
    ├── run_bfs.sh
    ├── run.sh
    ├── sdc_check.sh
    ├── stderr.txt
    └── stdout.txt
    ```
* ***vectorAdd*** which contains multiple sub-folders are "grouped" benchmarks. Basically, these programs have exactly the same source codes (```.c or .cu```). The only difference is the difference between input arguments. 
    * In this example, vectorAdd1024_16 means calling the vectorAdd kernel with a blocksize of 1024, and a grid size of 16
    * vectorAdd32_64 calls the vectorAdd kernel with a blocksize of 32, and a grid size of 64
* ***test-apps-dependencies*** are external input files to some testbench programs. 
    * For example, the```darknet``` detector program will ask for **network configs**; pre-trained **weights**;  ```.data``` file that specifies ```names``` for detection. 

**TODOs**
### 3.2. Naming/Organization rules for test-apps

### 3.3. If you also want to compile the CUDA application in-place......


## 4. Reference
If you find our tool is useful, please consider citing the following papers: 
* Hao Qiu, Semiu A. Olowogemo, Bor-Tyng Lin, William H. Robinson, and Daniel B. Limbrick. “Understanding time-varying vulnerability for efficient GPU program hardening”. *IEEE DFT 2022* (to be presented in October 2022)
* Hao Qiu, Semiu A. Olowogemo, Bor-Tyng Lin, William H. Robinson, and Daniel B. Limbrick. “Understanding GPU Application Vulnerability across Program Lifetime”. *IEEE SELSE workshop 2022* (presented in May 2022)

This work is inspired by the following works:
* NVBitFI paper
    * T. Tsai, S. K. S. Hari, M. Sullivan, O. Villa, and S. W. Keckler, “NVBitFI: Dynamic fault injection for GPUs,” in IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2021
   
* A paper exploreed time-varying vulnerability of "smaller" GPU programs using SASSFI (the precedent of NVBitFI)
    * F. G. Previlon, C. Kalra, and D. R. Kaeli, "Characterizing and exploiting soft error vulnerability phase behavior in gpu applications," *IEEE Transactions on Dependable and Secure Computing*, 2020.
