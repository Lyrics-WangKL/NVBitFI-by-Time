#!/bin/bash
ncu -f --set full -o profile reduction_small --n=32768 --threads=128
ncu -i profile.ncu-rep --page source --csv > instruction_trace.csv