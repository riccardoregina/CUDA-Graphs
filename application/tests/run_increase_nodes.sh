#!/bin/bash

TOTAL_WORK=10000

mkdir -p ../output
rm -f ../output/output_increase_nodes.csv

THREADS="1000 1000000 10000000"
NODES="1 2 4 5 8 10 16 20 25 40 50 80 100 125 200 250 400 500 625 1000 1250 2000 2500 5000 10000"

echo "Starting graph size overhead benchmark (increasing nodes)..."

for T in $THREADS; do
    for N in $NODES; do
        ITER=$(( TOTAL_WORK / N ))
        echo "Running Graph Overhead - Threads: $T, Nodes: $N, Outer Iterations: $ITER"
        ../application.out -t $T -k $N -o $ITER -i 1 -r 10 -g 1 -f ../output/output_increase_nodes.csv
    done
done

echo "Benchmark overhead completed!"
