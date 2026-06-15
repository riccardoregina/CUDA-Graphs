#include <cstdlib>
#include "utils.h"
#include "benchmark.cuh"

int main(int argc, char** argv) {
    Config cfg = parse_cli(argc, argv);
    
    run_benchmark(cfg);
    
    return EXIT_SUCCESS;
}
