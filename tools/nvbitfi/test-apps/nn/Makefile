include ../rodinia_common/make.config

LOCAL_CC = gcc -g -O3 -Wall
CC := $(CUDA_DIR)/bin/nvcc

all : nn hurricane_gen

clean :
	rm -rf *.o nn hurricane_gen

nn : nn_cuda.cu
	$(CC) -cuda nn_cuda.cu
	$(CC) -o nn nn_cuda.cu

hurricane_gen : hurricane_gen.c
	$(LOCAL_CC) -o $@ $< -lm

test:
	./run_nn.sh
golden:
	./run_nn.sh >golden_stdout.txt 2>golden_stderr.txt
clobber:
	rm -f golden* *_regcount.p stdout* stderr*

#data :
#	mkdir data
#	./gen_dataset.sh
