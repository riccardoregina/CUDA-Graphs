#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cuda_runtime.h>

// Macro per il controllo degli errori CUDA
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA error at " << __FILE__ << ":" << __LINE__ \
                      << " code=" << err << " (" << cudaGetErrorString(err) << ")" << std::endl; \
            exit(EXIT_FAILURE); \
        } \
    } while (0)

struct Config {
    int num_threads = 1024 * 1024;
    int inner_iterations = 1;
    int mini_batch_size = 10;
    int outer_iterations = 100;
    int repetitions = 10;
    unsigned int seed = 42;
    int use_graph = 0;
    int print_config = 0;
    std::string output_file = "";
};

Config parse_cli(int argc, char** argv);
int get_gpu_memory_mib();
void save_results(const Config& cfg, const std::vector<double>& graph_times, const std::vector<double>& exec_times, int gpu_memory_mib);

#endif // UTILS_H
