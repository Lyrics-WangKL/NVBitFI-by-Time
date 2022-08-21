#!/bin/bash
ncu -f --set full -o profile reduction_medium --n=2097152 --threads=128
ncu -i profile.ncu-rep --page source --csv > instruction_trace.csv