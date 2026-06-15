#include "kernel.cuh"

__global__ void compute_kernel(float* data, int num_threads, int inner_iterations) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < num_threads) {
        float val = data[idx];
        for (int i = 0; i < inner_iterations; ++i) {
            val *= 1.00005f;
        }
        data[idx] = val;
    }
}
