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
import gen_injection_utils.injectionList_cfs as cf_inj_gen
import gen_injection_utils.group_functions as gfs
import random

MAX_INJ = p.NUM_INJECTIONS
verbose = False
inj_mode = ""

class injectionList_generation:
    def __init__(self, apps, instbfm_map, num_injections, scope, app_log_dir, inj_mode='inst_value', verbose = False):
        self.apps = apps
        self.inj_mode = inj_mode
        self.instbfm_map = instbfm_map
        self.num_injs = num_injections
        self.scope = scope
        self.app_log_dir = app_log_dir

        self.verbose = verbose
        self.usage = "Vanila is default Nvbitfi injection scheme, insts groups by instructions, kernels group by kernels\n insts mode is only avaiable when kernel count is ONE"
        assert self.scope in ['vanilla', 'kernels', 'insts'], self.usage

    def make_injList_dirs(self, app, n_groups=10):
        if self.scope == "vanilla":
            cmd = f'mkdir -p {self.app_log_dir[app]}/injection-list'
            os.system(cmd) # create directory to store injection list
        else:
            for i in range(n_groups):
                cmd = f'mkdir -p {self.app_log_dir[app]}/injection-list-{self.scope}-group-{i}'
                os.system(cmd) # create directory to store injection list

    def gen_injList_fnames(self, app, gid, igid, bfm):
        if self.scope == "vanilla":
            fname = f'{self.app_log_dir[app]}/injection-list/mode{self.inj_mode}-igid{igid}.bfm{bfm}.{self.num_injs}.txt'
        else:
            fname = f'{self.app_log_dir[app]}/injection-list-{self.scope}-group-{gid}/mode{self.inj_mode}-igid{igid}.bfm{bfm}.{self.num_injs}.txt'
        return fname
    	
    def write_injection_list_file(self, app, igid, bfm, countList, total_count, start=0, end=0, group_id=0):
        if self.verbose:
            print ("total_count = %d, num_injections = %d, scope= %s" %(total_count, self.num_injs, self.scope))
        fName = self.gen_injList_fnames(app, group_id, igid, bfm)
        print(fName)
        f = open(fName, 'w')	
        local_inj_counter = self.num_injs

        if self.scope == "vanilla":
            while local_inj_counter > 0 and total_count != 0:
                local_inj_counter -= 1
                injection_num = random.randint(0, total_count) # randomly select an injection index
                selected_str = cf_inj_gen.gen_faultsite_str(igid, countList, injection_num)
                if self.verbose:
                    print ("%d/%d: Selected: %s" %(local_inj_counter, total_count, selected_str))
                f.write(selected_str + "\n") # print injection site information
        else:
            print(self.usage)
            exit(1)

    def gen_lists(self, num_inst_groups, n_groups): # num_inst_group meana the catagories of igid, which is defined in params.py/its setup scripts
        for app in self.apps:
            self.make_injList_dirs(app, n_groups)
            countList = cf_inj_gen.read_inst_counts(self.app_log_dir[app], app)
            n_kernel_instsances = len(countList)
            total_count = cf_inj_gen.get_total_insts(countList, False) # This implementation only supports inst-value injection mode

            total_icounts = cf_inj_gen.get_total_counts(countList)
            if self.scope == 'vanilla':
                for igid in self.instbfm_map:
                    for bfm in self.instbfm_map[igid]: 
                        self.write_injection_list_file(app, igid, bfm, countList, total_icounts[igid - num_inst_groups])
            else:
                print(self.usage)
                exit(1)


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
	n_groups = 10

	scope = "vanilla"

	injection_list_obj = injectionList_generation(apps, instbfm_map, num_injection, scope, app_log_dir, inj_mode)
	injection_list_obj.gen_lists(p.NUM_INST_GROUPS , n_groups)

if __name__ == "__main__":
    main()