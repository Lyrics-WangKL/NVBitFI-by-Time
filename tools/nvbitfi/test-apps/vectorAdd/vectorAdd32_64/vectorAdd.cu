#include <stdio.h>
// For the CUDA runtime routines (prefixed with "cuda_")
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <helper_functions.h>

#define CHECK(call)                                                            \
{                                                                              \
    const cudaError_t error = call;                                            \
    if (error != cudaSuccess)                                                  \
    {                                                                          \
        fprintf(stderr, "Error: %s:%d, ", __FILE__, __LINE__);                 \
        fprintf(stderr, "code: %d, reason: %s\n", error,                       \
                cudaGetErrorString(error));                                    \
        exit(1);                                                               \
    }                                                                          \
}

// VectorAdd kernel
__global__ void vecAdd(float * in1, float * in2, float * out, int len) {
    for (int idx = blockIdx.x * blockDim.x + threadIdx.x; idx < len; idx += blockDim.x * gridDim.x) {
        out[idx] = in1[idx] + in2[idx];
    }
}

int main(int argc, char *argv[]) {
    // Error code to check return values for CUDA calls
    cudaError_t err = cudaSuccess;

    // print vector length and size
    int numElements = 10000;
    size_t vectorSize_inbytes = numElements * sizeof(float);
    printf("[Vector addition of %d elements]\n", numElements);

    // allocating host memory for input and output vectors on heap
    float *h_A = (float *) malloc(vectorSize_inbytes); // a
    float *h_B = (float *) malloc(vectorSize_inbytes); // b
    float *h_C = (float *) malloc(vectorSize_inbytes); // res
    // Verify CPU(host) allocation succeeded
    if (h_A == NULL || h_B == NULL || h_C == NULL)
    {
        fprintf(stderr, "Failed to allocate host vectors!\n");
        exit(EXIT_FAILURE);
    }

    // Create ptrs to GPU(device) memory
    float *d_A;
    float *d_B;
    float *d_C;
    // initialize input vectors a,b
    for (int i=0; i<numElements; ++i){
        h_A[i] = rand()/(float)RAND_MAX;
        h_B[i] = rand()/(float)RAND_MAX;
    }

    // Allocate GPU memory using cudaMalloc(addrOfthePtr, sizeOfallocatedMemory), with error checker
    // err = cudaMalloc((void**) &d_A, vectorSize_inbytes);
    CHECK(cudaMalloc((void**) &d_A, vectorSize_inbytes));
    // if (err != cudaSuccess) // verify GPU allocation succeeded
    // {
    //     fprintf(stderr, "Failed to allocate device vector A (error code %s)!\n", cudaGetErrorString(err));
    //     exit(EXIT_FAILURE);
    // }
    err = cudaMalloc((void**) &d_B, vectorSize_inbytes);
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to allocate device vector A (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    err = cudaMalloc((void**) &d_C, vectorSize_inbytes);
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to allocate device vector A (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }

    // Copy host memory content to device memory using cudaMemCpy(p2dest, p2source, sizeofTransfer(in byte), direction)
    printf("Copy input data from the host memory to the CUDA device\n");
    err = cudaMemcpy(d_A, h_A, vectorSize_inbytes, cudaMemcpyHostToDevice); 
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to copy vector B from host to device (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    checkCudaErrors(cudaMemcpy(d_B, h_B, vectorSize_inbytes, cudaMemcpyHostToDevice)); 

    // Prep of launching CUDA kernel
    int blocksize = 256; // 256 threads per block by default
    if (argc > 1) blocksize = atoi(argv[1]); // When specified, blocksize=argv[1]
    int gridsize = 0; // ceil(nEle/blocksize)
    if (argc > 2) gridsize =  atoi(argv[2]);
    // printf("CUDA kernel launch with %d blocks of %d threads\n", gridsize, blocksize);
    // Initialize block and grid dim.
    dim3 DimGrid(gridsize, 1, 1);
    dim3 DimBlock(blocksize, 1, 1);
    
    // Launch kernel
    vecAdd<<<DimGrid, DimBlock>>>(d_A, d_B, d_C, numElements);
    err = cudaGetLastError();
    if (err != cudaSuccess) // verify kernel excecution succeeded
    {
        fprintf(stderr, "Failed to launch vectorAdd kernel (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    // Copy res from device memory back to host memory using cudaMemCpy
    printf("Copy output data from the CUDA device to the host memory\n");
    err = cudaMemcpy(h_C, d_C, vectorSize_inbytes, cudaMemcpyDeviceToHost); 
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to copy vector B from host to device (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }

    // Verify that the result vector is correct
    for (int i = 0; i < numElements; ++i)
    {
        // printf("expect: %f, ele: %f\n", h_A[i] + h_B[i], h_C[i]);
        if (fabs(h_A[i] + h_B[i] - h_C[i]) > 1e-5)
        {
            fprintf(stdout, "Result verification failed at element %d!\n", i);
            exit(EXIT_FAILURE);
        }
    }
    printf("Test PASSED\n");


    // Free device global memory
    err = cudaFree(d_A);
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector A (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    err = cudaFree(d_B);
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector B (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    err = cudaFree(d_C);
    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector C (error code %s)!\n", cudaGetErrorString(err));
        exit(EXIT_FAILURE);
    }
    // Free host memory
    free(h_A);
    free(h_B);
    free(h_C);

    printf("Done\n");
    return 0;
}