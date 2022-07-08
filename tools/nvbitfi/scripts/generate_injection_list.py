# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, re, string, os, operator, math, datetime, random
import params as p 
import random

from gen_injection_utils.injectionList_generator import injectionList_generator

MAX_INJ = p.NUM_INJECTIONS
verbose = False
inj_mode = ""


#################################################################
# Starting point of the script
#################################################################
def main():
	# if len(sys.argv) == 2: 
	# 	inj_mode = sys.argv[1] # rf or inst_value or inst_address
	# else:
	# 	print ("Usage: ./script-name <rf or inst>")
	# 	print ("Only one mode is currently supported: inst_value")
	# 	exit(1)
	inj_mode = "inst_value" # we only support inst_value mode in NVBitFI as of now (March 25, 2020)
	apps = p.apps
	app_log_dir = p.app_log_dir
	instbfm_map = p.inst_value_igid_bfm_map
	num_injection = p.NUM_INJECTIONS
	num_inst_groups = p.NUM_INST_GROUPS

	argv_ena = True
	
	if argv_ena and len(sys.argv) >= 2:
		scope = sys.argv[1]
		n_groups = int(sys.argv[2])
	else:
		scope = 'kernels'
		n_groups = 10

	injection_list_obj = injectionList_generator(apps, instbfm_map, num_injection, scope, app_log_dir, num_inst_groups, inj_mode)
	injection_list_obj.gen_lists(n_groups)

if __name__ == "__main__":
    main()