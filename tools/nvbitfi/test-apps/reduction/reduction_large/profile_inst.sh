#!/bin/bash
ncu -f --set full -o profile reduction_large --n=33554432 --threads=1024 --maxblocks=256
ncu -i profile.ncu-rep --page source --csv > instruction_trace.csv