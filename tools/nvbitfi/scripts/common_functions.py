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

def set_env(app, is_profiler):
	# Make sure that you use the same ENV variables in the run scripts
	os.environ['BIN_DIR'] = p.bin_dir[app]
	os.environ['BIN_PATH'] = p.bin_dir[app]
	os.environ['APP_DIR'] = p.app_dir[app]
	os.environ['DATASET_DIR'] = p.app_data_dir[app]
	if is_profiler: 
		os.environ['PRELOAD_FLAG'] = "LD_PRELOAD=" + p.PROFILER_LIB
	else:
		os.environ['PRELOAD_FLAG'] = "LD_PRELOAD=" + p.INJECTOR_LIB 
	if p.verbose: print ("BIN_DIR=%s" %(os.environ['BIN_DIR']))
	if p.verbose: print ("PRELOAD_FLAG=%s" %(os.environ['PRELOAD_FLAG']))
	if p.verbose: print ("RODINIA=%s" %(os.environ['RODINIA']))
	if p.verbose: print ("APP_DIR=%s" %(os.environ['APP_DIR']))
