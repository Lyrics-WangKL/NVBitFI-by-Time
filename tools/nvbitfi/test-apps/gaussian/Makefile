include ../test-apps-dependencies/rodinia_common/make.config
CC := $(CUDA_DIR)/bin/nvcc

INCLUDE := $(CUDA_DIR)/include

SRC = gaussian.cu
EXE = gaussian

release: $(SRC)
	$(CC) $(KERNEL_DIM) $(SRC) -o $(EXE) -I$(INCLUDE) -L$(CUDA_LIB_DIR) 


test:
	./run_gaussian.sh
golden:
	./run_gaussian.sh >golden_stdout.txt 2>golden_stderr.txt
clobber:
	rm -f golden* *_regcount.p stdout* stderr*


clean:
	rm gaussian
