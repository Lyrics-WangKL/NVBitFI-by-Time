import sys, re, string, os, operator, math, datetime, random

# resovle path issues first
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import gen_injection_utils.injectionList_cfs as cf_inj_gen


class injectionList_generator:
    def __init__(self, apps, instbfm_map, num_injections, scope, app_log_dir, num_inst_groups, inj_mode='inst_value', verbose = False):
        self.apps = apps
        self.inj_mode = inj_mode
        self.instbfm_map = instbfm_map
        self.num_injs = num_injections
        self.scope = scope
        self.app_log_dir = app_log_dir

        self.num_inst_groups = num_inst_groups
        self.verbose = verbose
        self.usage = "Vanila is default Nvbitfi injection scheme, insts groups by instructions, kernels group by kernels\n insts mode is only avaiable when kernel count is ONE"
        assert self.scope in ['vanilla', 'kernels', 'insts'], self.usage

    def make_injList_dirs(self, app, n_groups=10):
        if self.scope == "vanilla":
            cmd = f'mkdir -p {self.app_log_dir[app]}injection-list'
            os.system(cmd) # create directory to store injection list
        else:
            for i in range(n_groups):
                cmd = f'mkdir -p {self.app_log_dir[app]}injection-list-{self.scope}-group-{i}'
                os.system(cmd) # create directory to store injection list

    def gen_injList_fnames(self, app, gid, igid, bfm):
        if self.scope == "vanilla":
            fname = f'{self.app_log_dir[app]}injection-list/mode{self.inj_mode}-igid{igid}.bfm{bfm}.{self.num_injs}.txt'
        else:
            fname = f'{self.app_log_dir[app]}injection-list-{self.scope}-group-{gid}/mode{self.inj_mode}-igid{igid}.bfm{bfm}.{self.num_injs}.txt'
        return fname
    	
    def write_injection_list_file(self, app, igid, bfm, countList, total_count, start=0, end=0, group_id=0):
        if self.verbose:
            print ("total_count = %d, num_injections = %d, scope= %s" %(total_count, self.num_injs, self.scope))
        fName = self.gen_injList_fnames(app, group_id, igid, bfm)
        print(fName)
        f = open(fName, 'w')	
        local_inj_counter = self.num_injs

        if self.scope == 'vanilla' or self.scope == 'kernels':
            while local_inj_counter > 0 and total_count != 0:
                local_inj_counter -= 1
                cf_inj_gen.write_fault_site(f, igid, countList, total_count, local_inj_counter, start, end, verbose=self.verbose, scope=self.scope)
            f.close()
        elif self.scope == 'insts':
            while local_inj_counter > 0 and (end-start) != 0:
                local_inj_counter -= 1
                cf_inj_gen.write_fault_site(f, igid, countList, total_count, local_inj_counter, start, end, verbose=self.verbose, scope=self.scope)
            f.close()
        else:
            print(self.usage)
            exit(1)

    def gen_lists(self, n_groups, group_function): # num_inst_group means the catagories of igid, which is defined in params.py/its setup scripts
        for app in self.apps:
            self.make_injList_dirs(app, n_groups)
            countList = cf_inj_gen.read_inst_counts(self.app_log_dir[app], app)
            n_kernel_instsances = len(countList)
            total_count = cf_inj_gen.get_total_insts(countList, False) # This implementation only supports inst-value injection mode

            total_icounts = cf_inj_gen.get_total_counts(countList)
            if self.scope == 'vanilla':
                for igid in self.instbfm_map:
                    for bfm in self.instbfm_map[igid]: 
                        self.write_injection_list_file(app, igid, bfm, countList, total_icounts[igid - self.num_inst_groups])
            elif self.scope == 'insts':
                for igid in self.instbfm_map:
                    for bfm in self.instbfm_map[igid]:
                        # inst_groups = gfs.NaiveGroup_inst(total_icounts[igid - self.num_inst_groups], n_groups)  # Using naive inst level grouping function
                        try:
                            inst_groups = group_function(total_icounts[igid - self.num_inst_groups], n_groups)
                        except: 
                            print("instruction level grouping expects a list total instruction count, and the number of groups")
                            exit(1)
                        for group_idx in range(len(inst_groups) - 1):
                            start, end = inst_groups[group_idx], inst_groups[group_idx + 1]
                            self.write_injection_list_file(app, igid, bfm, countList, total_icounts[igid - self.num_inst_groups], start, end, group_idx)
            elif self.scope == 'kernels' and n_kernel_instsances >= n_groups:
                # kernel_groups = list(gfs.NaiveGroup_kernel(countList, n_groups)) # Using naive kernel level grouping function
                try:
                    kernel_groups = list(group_function(countList, n_groups))
                except:
                    print("kernel level grouping expects a list of list of each kernel's total instruction count, and the number of groups")
                    exit(1)
                for group_idx, countList_group in enumerate(kernel_groups):
                    for igid in self.instbfm_map:
                        for bfm in self.instbfm_map[igid]:
                            total_icounts = cf_inj_gen.get_total_counts(countList_group)
                            self.write_injection_list_file(app, igid, bfm, countList_group, total_icounts[igid - self.num_inst_groups], group_id = group_idx)
            else:
                print(self.usage)
                exit(1)