#ifndef KERNEL_CUH
#define KERNEL_CUH

__global__ void compute_kernel(float* data, int num_threads, int inner_iterations);

#endif // KERNEL_CUH
