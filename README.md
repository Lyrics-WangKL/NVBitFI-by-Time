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





