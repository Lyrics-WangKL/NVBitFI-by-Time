import os, sys

PYTHON_P = "python"

if 'NVBITFI_HOME' not in os.environ:
	print ("Error: Please set NVBITFI_HOME environment variable")
	sys.exit(-1)
NVBITFI_HOME = os.environ['NVBITFI_HOME']

#######################################################################
# Specify library paths
#######################################################################
INJECTOR_LIB = os.environ['NVBITFI_HOME'] + "/injector/injector.so"
PROFILER_LIB = os.environ['NVBITFI_HOME'] + "/profiler/profiler.so"

#######################################################################
# Three injection modes
#######################################################################
RF_MODE = "rf"
INST_VALUE_MODE = "inst_value"
INST_ADDRESS_MODE = "inst_address"

#######################################################################
# Categories of instruction types (IGIDs): This should match the values set in
# arch.h in the nvbitfi/common/
#######################################################################
G_FP64 = 0
G_FP32 = 1
G_LD = 2
G_PR = 3
G_NODEST = 4 # not really an igid
G_OTHERS = 5 
G_GPPR = 6 # instructions that write to either a GPR or a PR register
G_GP = 7 # instructions that write to a GPR register
NUM_INST_GROUPS = 8

IGID_STR = [ "fp64", "fp32", "ld", "pr", "nodest", "others", "gppr", "gp" ]

#######################################################################
# Types of avaialble error models (bit-flip model, BFM): This should match the
# values set in err_injector/error_injector.h. 
#######################################################################
FLIP_SINGLE_BIT = 0
FLIP_TWO_BITS = 1
RANDOM_VALUE = 2
ZERO_VALUE = 3

EM_STR = [ "FLIP_SINGLE_BIT", "FLIP_TWO_BITS", "RANDOM_VALUE", "ZERO_VALUE"]

rf_inst = ""

#######################################################################
# Categories of error injection outcomes
#######################################################################
# Masked
MASKED_NOT_READ = 1
MASKED_WRITTEN = 2
MASKED_OTHER = 3

# DUEs
TIMEOUT = 4
NON_ZERO_EC = 5 # non zero exit code

# Potential DUEs with appropriate detectors in place
MASKED_KERNEL_ERROR = 6
SDC_KERNEL_ERROR = 7
NON_ZERO_EM = 8 # non zero error message (stderr is different)
STDOUT_ERROR_MESSAGE = 9
STDERR_ONLY_DIFF = 10
DMESG_STDERR_ONLY_DIFF = 11
DMESG_STDOUT_ONLY_DIFF = 12
DMESG_OUT_DIFF = 13
DMESG_APP_SPECIFIC_CHECK_FAIL= 14
DMESG_XID_43 = 15

# SDCs
STDOUT_ONLY_DIFF = 16
OUT_DIFF = 17
APP_SPECIFIC_CHECK_FAIL= 18

OTHERS = 19
NUM_CATS = 20

CAT_STR = ["Masked: Error was never read", "Masked: Write before read",
"Masked: other reasons", "DUE: Timeout", "DUE: Non Zero Exit Status", 
"Pot DUE: Masked but Kernel Error", "Pot DUE: SDC but Kernel Error", 
"Pot DUE: Different Error Message", "Pot DUE: Error Message in Standard Output", 
"Pot DUE: Stderr is different", "Pot DUE:Stderr is different, but dmesg recorded", 
"Pot DUE: Standard output is different, but dmesg recorded", 
"Pot DUE: Output file is different, but dmesg recorded", 
"Pot DUE: App specific check failed, but dmesg recorded",
"Pot DUE: Xid 43 recorded in dmesg",
"SDC: Standard output is different", "SDC: Output file is different", 
"SDC: App specific check failed", "Uncategorized"]

#########################################################################
# Parameterizing file names
#########################################################################
run_script = "run.sh"
nvbit_profile_log = "nvbitfi-igprofile.txt"
injection_seeds = "nvbitfi-injection-info.txt"
inj_run_log = "nvbitfi-injection-log-temp.txt"
stdout_file = "stdout.txt"
stderr_file = "stderr.txt"
output_diff_log = "diff.log"
stdout_diff_log = "stdout_diff.log"
stderr_diff_log = "stderr_diff.log"
special_sdc_check_log = "special_check.log"

#########################################################################
# Number of gpus to use for error injection runs
#########################################################################
NUM_GPUS = 1

use_filelock = False


