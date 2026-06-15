#include "utils.h"
#include <iostream>
#include <getopt.h>
#include <cmath>
#include <fstream>
#include <sstream>
#include <iomanip>

#include <stdio.h>

Config parse_cli(int argc, char** argv) {
    Config cfg;
    static struct option long_options[] = {
        {"num_threads", required_argument, 0, 't'},
        {"inner_iterations", required_argument, 0, 'i'},
        {"mini_batch_size", required_argument, 0, 'k'},
        {"outer_iterations", required_argument, 0, 'o'},
        {"repetitions", required_argument, 0, 'r'},
        {"seed", required_argument, 0, 's'},
        {"use_graph", required_argument, 0, 'g'},
        {"print", no_argument, 0, 'p'},
        {"output", required_argument, 0, 'f'},
        {0, 0, 0, 0}
    };

    int opt;
    int option_index = 0;
    while ((opt = getopt_long(argc, argv, "t:i:k:o:r:s:g:pf:", long_options, &option_index)) != -1) {
        switch (opt) {
            case 't': cfg.num_threads = std::stoi(optarg); break;
            case 'i': cfg.inner_iterations = std::stoi(optarg); break;
            case 'k': cfg.mini_batch_size = std::stoi(optarg); break;
            case 'o': cfg.outer_iterations = std::stoi(optarg); break;
            case 'r': cfg.repetitions = std::stoi(optarg); break;
            case 's': cfg.seed = std::stoul(optarg); break;
            case 'g': cfg.use_graph = std::stoi(optarg); break;
            case 'p': cfg.print_config = 1; break;
            case 'f': cfg.output_file = optarg; break;
            default:
                std::cerr << "Uso: " << argv[0] << " [opzioni]" << std::endl;
                exit(EXIT_FAILURE);
        }
    }

    if (cfg.print_config) {
        std::cout << "--- Configurazione CLI ---" << std::endl;
        std::cout << "Threads: " << cfg.num_threads << std::endl;
        std::cout << "Inner Iterations: " << cfg.inner_iterations << std::endl;
        std::cout << "Mini-Batch Size: " << cfg.mini_batch_size << std::endl;
        std::cout << "Outer Iterations: " << cfg.outer_iterations << std::endl;
        std::cout << "Repetitions: " << cfg.repetitions << std::endl;
        std::cout << "Seed: " << cfg.seed << std::endl;
        std::cout << "Use Graph: " << cfg.use_graph << std::endl;
        std::cout << "Output File: " << (cfg.output_file.empty() ? "stdout" : cfg.output_file) << std::endl;
        std::cout << "--------------------------" << std::endl;
    }
    return cfg;
}

int get_gpu_memory_mib() {
    FILE* pipe = popen("nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits", "r");
    if (!pipe) {
        std::cerr << "Failed to run nvidia-smi command" << std::endl;
        return -1;
    }
    char buffer[128];
    std::string result = "";
    if (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result = buffer; // Leggiamo solo la prima riga
    }
    pclose(pipe);
    try {
        return std::stoi(result);
    } catch (...) {
        return -1; 
    }
}

void save_results(const Config& cfg, const std::vector<double>& graph_times, const std::vector<double>& exec_times, int gpu_memory_mib) {
    double graph_creation_mean = 0.0;
    for (double t : graph_times) graph_creation_mean += t;
    graph_creation_mean /= cfg.repetitions;

    double graph_creation_std = 0.0;
    if (cfg.repetitions > 1) {
        for (double t : graph_times) graph_creation_std += (t - graph_creation_mean) * (t - graph_creation_mean);
        graph_creation_std = std::sqrt(graph_creation_std / cfg.repetitions);
    }

    double exec_time_mean = 0.0;
    for (double t : exec_times) exec_time_mean += t;
    exec_time_mean /= cfg.repetitions;

    double exec_time_std = 0.0;
    if (cfg.repetitions > 1) {
        for (double t : exec_times) exec_time_std += (t - exec_time_mean) * (t - exec_time_mean);
        exec_time_std = std::sqrt(exec_time_std / cfg.repetitions);
    }

    bool write_header = false;
    if (!cfg.output_file.empty()) {
        std::ifstream infile(cfg.output_file);
        if (!infile.good()) {
            write_header = true;
        } else {
            infile.seekg(0, std::ios::end);
            if (infile.tellg() == 0) {
                write_header = true;
            }
        }
    } else {
        write_header = true; 
    }

    std::stringstream ss;
    if (write_header) {
        ss << "mode,threads,mini_batch_size,outer_iterations,inner_iterations,repetitions,graph_creation_mean,graph_creation_std,exec_time_mean,exec_time_std,gpu_memory_mib\n";
    }
    ss << cfg.use_graph << ","
       << cfg.num_threads << ","
       << cfg.mini_batch_size << ","
       << cfg.outer_iterations << ","
       << cfg.inner_iterations << ","
       << cfg.repetitions << ","
       << std::fixed << std::setprecision(6) << graph_creation_mean << ","
       << graph_creation_std << ","
       << exec_time_mean << ","
       << exec_time_std << ","
       << gpu_memory_mib << "\n";

    if (!cfg.output_file.empty()) {
        std::ofstream outfile(cfg.output_file, std::ios::app);
        if (outfile.is_open()) {
            outfile << ss.str();
            outfile.close();
        } else {
            std::cerr << "Errore nell'aprire il file per output: " << cfg.output_file << std::endl;
        }
    } else {
        std::cout << ss.str();
    }
}
