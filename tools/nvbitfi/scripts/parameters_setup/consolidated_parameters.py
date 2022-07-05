import os, sys
from parameters_setup.constant_parameters import *
PYTHON_P = "python"

TIMEOUT_THRESHOLD = 10 # 10X usual runtime 

if 'NVBITFI_HOME' not in os.environ:
	print ("Error: Please set NVBITFI_HOME environment variable")
	sys.exit(-1)
NVBITFI_HOME = os.environ['NVBITFI_HOME']

# verbose = True
verbose = False
detectors = True

# Keep per-app injection logs: This can be helpful for debugging. If this flag
# is set to false, per-injection logs will be deleted. A detailed summary will
# be captured in the results file. 
keep_logs = True

#######################################################################
# A customized class to setup user-defined parameters
#######################################################################
class UserParameters:
	def __init__(self, appdir=NVBITFI_HOME+'/test-apps', injections=1000, threshold_jobs=384):
		self.appdir = appdir
		self.injections = 1000
		self.threshold_job = 384

		assert(threshold_jobs <= injections)

	def igid2bfm_map(self, instructionTypes, faultModels):
		return {}

	# app_scan method scans appdir, returns a dictionary of apps
	def app_scan(self):
		return {}

	# aggreated parsed bfm2app dictionary, returns a dictionary of apps amd bfm_map
	def params_aggregate(self, selected_list):
		return {}

