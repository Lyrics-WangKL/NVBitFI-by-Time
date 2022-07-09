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

import os, sys, re, string, operator, math, datetime, time, signal, subprocess, shutil, glob, pkgutil
import params as p
import run_injection_utils.run_one_injection_helpers as one_injection_helper

###############################################################################
# Starting point of the execution
###############################################################################
def main(): 
	# print ("run_one_injection.py: kname=%s, argv[8]=%s" %(sys.argv[5], sys.argv[8])
	# print(sys.argv)
	'''
		[<path to pwd>, 'inst_value', '7', '0', 'yolo_tiny', <kname>, <kernelcnt>, <iid>, '0.6583529207275547', '0.658235062733477', '10']
	'''

	# check if paths exit
	if not os.path.isdir(p.NVBITFI_HOME): print ("Error: Regression dir not found!")
	if not os.path.isdir(p.NVBITFI_HOME + "/logs/results"): os.system("mkdir -p " + p.NVBITFI_HOME + "/logs/results") # create directory to store summary

	if len(sys.argv) == 13:
		start= datetime.datetime.now()
		[inj_mode, igid, bfm, app, kname, kcount, iid, opid, bid, icount, mode, gid] = sys.argv[1:]
		one_injection_helper.set_env_variables(inj_mode, app, igid, bfm, icount, mode, gid) 
		err_cat = one_injection_helper.run_one_injection_job(inj_mode, igid, bfm, app, kname, kcount, iid, opid, bid, icount, mode, gid) 
		elapsed = datetime.datetime.now() - start
		if mode != 'vanilla':
			print ("Inj_count=%s, App=%s, Mode=%s, TimeGroup=%s, Group=%s,  EM=%s, Time=%f, Outcome: %s" %(icount, app, inj_mode, gid, igid, bfm, one_injection_helper.get_seconds(elapsed), p.CAT_STR[err_cat-1]))
		else:
			print ("Inj_count=%s, App=%s, Mode=%s, Group=%s, EM=%s, Time=%f, Outcome: %s" %(icount, app, inj_mode, igid, bfm, one_injection_helper.get_seconds(elapsed), p.CAT_STR[err_cat-1]))
	else:
		print('problem in arguments count')
		one_injection_helper.print_usage()

if __name__ == "__main__":
    main()
