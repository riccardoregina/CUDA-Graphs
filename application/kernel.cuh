#ifndef KERNEL_CUH
#define KERNEL_CUH

// Dichiarazione del kernel computazionale
__global__ void compute_kernel(float* data, int num_threads, int inner_iterations);

#endif // KERNEL_CUH
