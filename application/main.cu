#include <cstdlib>
#include "utils.h"
#include "benchmark.cuh"

int main(int argc, char** argv) {
    // 1. Parsing della configurazione CLI
    Config cfg = parse_cli(argc, argv);
    
    // 2. Esecuzione del benchmark sulla GPU
    run_benchmark(cfg);
    
    return EXIT_SUCCESS;
}
