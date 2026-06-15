#!/bin/bash

OPTIMAL_NODES=100

mkdir -p ../output
rm -f ../output/output_kernels_increase_it.csv
rm -f ../output/output_graph_increase_it.csv

THREADS="1000 1000000 10000000"
ITERATIONS=$(seq 1 40)

echo "Starting speed-up benchmark (increasing iterations)..."

for T in $THREADS; do
    for I in $ITERATIONS; do
        echo "Running Baseline - Threads: $T, Iterations: $I, Nodes: $OPTIMAL_NODES"
        ../application.out -t $T -k $OPTIMAL_NODES -o $I -i 1 -r 10 -g 0 -f ../output/output_kernels_increase_it.csv
        
        echo "Running Graph - Threads: $T, Iterations: $I, Nodes: $OPTIMAL_NODES"
        ../application.out -t $T -k $OPTIMAL_NODES -o $I -i 1 -r 10 -g 1 -f ../output/output_graph_increase_it.csv
    done
done

echo "Benchmark speed-up completed!"
