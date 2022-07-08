import numpy as np
#########################################################################
# Extended Instruction index Grouping Helpler
#########################################################################
"""
Naive grouping function simply divide program into equally sized pieces, depdending
on the scope, the total_count can be instructions# or kernels#

Returns a list of [start, start+step, start+2xstep ..... end]
"""
def NaiveGroup(total_count, num_instGroup):
    res = [] 
    n, m = divmod(total_count, num_instGroup)
    for i in range(num_instGroup):
        res.append(i * n)
    res.append((i + 1) * n + min(i + 1, m))
    return res

# #########################################################################
# # Extended CountList Grouping Helpler
# #########################################################################
def countListSplit(klist, n_groups):
	split = np.array_split(klist, n_groups)
	return list(split)