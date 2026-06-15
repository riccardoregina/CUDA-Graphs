#include "benchmark.cuh"
#include "kernel.cuh"
#include <iostream>
#include <vector>
#include <random>
#include <chrono>

void run_benchmark(const Config& cfg) {
    // Inizializzazione Dati Host
    std::vector<float> h_data(cfg.num_threads);
    std::mt19937 rng(cfg.seed);
    std::uniform_real_distribution<float> dist(0.0f, 0.1f);
    for (int i = 0; i < cfg.num_threads; ++i) {
        h_data[i] = dist(rng);
    }

    // Allocazione GPU e copia Dati
    float* d_data = nullptr;
    CUDA_CHECK(cudaMalloc(&d_data, cfg.num_threads * sizeof(float)));
    CUDA_CHECK(cudaMemcpy(d_data, h_data.data(), cfg.num_threads * sizeof(float), cudaMemcpyHostToDevice));

    // Calcolo del layout della Grid
    int threads_per_block = 1024;
    int blocks_per_grid = (cfg.num_threads + threads_per_block - 1) / threads_per_block;

    std::vector<double> graph_creation_times;
    std::vector<double> exec_times;
    int gpu_memory_mib = -1;

    // Modalità di Esecuzione e Profiling
    for (int r = 0; r < cfg.repetitions; ++r) {
        double graph_creation_time = 0.0;
        double exec_time = 0.0;

        cudaGraph_t graph = nullptr;
        cudaGraphExec_t graphExec = nullptr;

        if (cfg.use_graph == 1) {
            auto start_graph = std::chrono::high_resolution_clock::now();

            CUDA_CHECK(cudaGraphCreate(&graph, 0));
            cudaGraphNode_t prev_node = nullptr;

            for (int k = 0; k < cfg.mini_batch_size; ++k) {
                cudaGraphNode_t current_node;
                cudaKernelNodeParams kernelParams = {0};
                kernelParams.func = (void*)compute_kernel;
                kernelParams.gridDim = dim3(blocks_per_grid);
                kernelParams.blockDim = dim3(threads_per_block);
                kernelParams.sharedMemBytes = 0;
                void* args[] = { (void*)&d_data, (void*)&cfg.num_threads, (void*)&cfg.inner_iterations };
                kernelParams.kernelParams = args;
                kernelParams.extra = nullptr;

                std::vector<cudaGraphNode_t> deps;
                if (prev_node != nullptr) {
                    deps.push_back(prev_node);
                }

                CUDA_CHECK(cudaGraphAddKernelNode(&current_node, graph, deps.empty() ? nullptr : deps.data(), deps.size(), &kernelParams));
                prev_node = current_node;
            }

#if CUDART_VERSION >= 12000
            CUDA_CHECK(cudaGraphInstantiate(&graphExec, graph, 0));
#else
            CUDA_CHECK(cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0));
#endif
            CUDA_CHECK(cudaGraphUpload(graphExec, 0));
            CUDA_CHECK(cudaStreamSynchronize(0));

            auto end_graph = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> diff_graph = end_graph - start_graph;
            graph_creation_time = diff_graph.count();
        }

        auto start_exec = std::chrono::high_resolution_clock::now();

        if (cfg.use_graph == 0) {
            for (int o = 0; o < cfg.outer_iterations; ++o) {
                for (int k = 0; k < cfg.mini_batch_size; ++k) {
                    compute_kernel<<<blocks_per_grid, threads_per_block>>>(d_data, cfg.num_threads, cfg.inner_iterations);
                }
            }
        } else {
            for (int o = 0; o < cfg.outer_iterations; ++o) {
                CUDA_CHECK(cudaGraphLaunch(graphExec, 0));
            }
        }
        
        CUDA_CHECK(cudaDeviceSynchronize());

        auto end_exec = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff_exec = end_exec - start_exec;
        exec_time = diff_exec.count();

        graph_creation_times.push_back(graph_creation_time);
        exec_times.push_back(exec_time);

        if (r == cfg.repetitions - 1) {
            gpu_memory_mib = get_gpu_memory_mib();
        }

        if (cfg.use_graph == 1) {
            CUDA_CHECK(cudaGraphExecDestroy(graphExec));
            CUDA_CHECK(cudaGraphDestroy(graph));
        }
    }

    CUDA_CHECK(cudaFree(d_data));

    save_results(cfg, graph_creation_times, exec_times, gpu_memory_mib);
}
