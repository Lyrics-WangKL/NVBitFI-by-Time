import os, sys
from parameters_setup.constant_parameters import *

#######################################################################
# A customized class to setup user-defined parameters
#######################################################################
class UserParameters:
	def __init__(self, appdir=NVBITFI_HOME+'/test-apps', injections=1000, threshold_jobs=384, timeout_threshold=30, dummy=False):
		self.appdir = appdir
		self.injections = injections
		self.threshold_job = threshold_jobs
		self.timeout = timeout_threshold
		if dummy:
			self.threshold_job = 5
		assert(threshold_jobs <= injections)


	def igid2bfm_map(self, instructionTypes, faultModels):
		igid2bfm_map = {}
		for igid in instructionTypes:
			keys = igid
			for model in faultModels:
				igid2bfm_map[keys] = model
		return igid2bfm_map


	# app_scan method scans appdir, returns a dictionary of apps
	def apps_scan(self, runtime=2, additional_params=""):
		apps_dict = {}
		for curr_dir, containing_dir, contained_file in os.walk(self.appdir):
			app_info = []
			if 'test-apps-dependencies' in curr_dir:
				continue
			else:
				if "sdc_check.sh" in contained_file:
					curr_dirname = curr_dir.split('/')[-1]
					app_info = [curr_dir, # workload directory
					curr_dirname, # binary_name
					curr_dir,
					runtime,
					additional_params
					]
					apps_dict[curr_dirname] = app_info
		return apps_dict

	# aggreated parsed bfm2app dictionary, returns a dictionary of apps amd bfm_map
	def params_aggregate(self, selected_appname, inst_types, fault_models):
		apps_dict = self.apps_scan()
		bfm_map = self.igid2bfm_map(inst_types, fault_models)
		selected_apps = {key: apps_dict[key] for key in selected_appname}
		aggregated_params = {
		'selected_apps': selected_apps,
        'igid_bfm_map': bfm_map 
		}
		return aggregated_params
		

