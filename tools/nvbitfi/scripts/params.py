from parameters_setup.consolidated_parameters import *

#######################################################################
# Specify a few data dumping arguments
#######################################################################
# verbose = True
verbose = False
detectors = True
# Keep per-app injection logs: This can be helpful for debugging. If this flag is set to false, per-injection logs will be deleted. A detailed summary will be captured in the results file. 
keep_logs = True
# Dummy run only inject 10 faults per app
dummy_run = True

#########################################################################
# Create parameters object, Override FI setups parameters: number of injection, threshold, timeout
#########################################################################
params_obj = UserParameters(injections=1000, threshold_jobs=384, timeout_threshold=10, dummy=dummy_run)
NUM_INJECTIONS = params_obj.injections
THRESHOLD_JOBS = params_obj.threshold_job
TIMEOUT_THRESHOLD = params_obj.timeout

#######################################################################
# Specify testbench, instruction type, fault model
#######################################################################
selected_apps = ['darknet1img_tiny']
# selected_apps = ['vectorAdd32_64']
selected_instruction_type = [G_GP]
selected_faultmodel = [[FLIP_SINGLE_BIT]]

usr_params = params_obj.params_aggregate(selected_apps, selected_instruction_type, selected_faultmodel)

apps = usr_params['selected_apps']
inst_value_igid_bfm_map = usr_params['igid_bfm_map']

#########################################################################
# Separate list of apps and error models for parsing because one may want to
# parse results for a differt set of applications and error models 
#########################################################################
parse_inst_value_igid_bfm_map = inst_value_igid_bfm_map
parse_apps = apps

#########################################################################
# Set paths for application binary, run script, etc. 
#########################################################################
app_log_dir = {} 
script_dir = {} 
bin_dir = {}
app_dir = {}
app_data_dir = {}
def set_paths(): 
	merged_apps = apps # merge the two dictionaries 
	merged_apps.update(parse_apps) 
	
	for app in merged_apps:
		app_log_dir[app] = NVBITFI_HOME + "/logs/" + app + "/"
		bin_dir[app] = merged_apps[app][2]
		app_dir[app] = merged_apps[app][0]
		script_dir[app] = merged_apps[app][0]
		if 'darknet' in app:
			app_data_dir[app] = NVBITFI_HOME + "/test-apps/test-apps-dependencies/darknet_data"
		else:
			app_data_dir[app] = NVBITFI_HOME + "/test-apps/test-apps-dependencies/rodinia_data/" + app

set_paths()