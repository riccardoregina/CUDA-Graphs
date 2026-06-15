#!/bin/bash

mkdir -p ../output
rm -f ../output/output_mem.csv

THREADS="1000 1000000 10000000"
NODES="1 2 4 5 8 10 16 20 25 40 50 80 100 125 200 250 400 500 625 1000 1250 2000 2500 5000 10000"

echo "Starting memory footprint benchmark..."

for T in $THREADS; do
    for N in $NODES; do
        echo "Running Memory Check - Threads: $T, Nodes: $N"
        ../application.out -t $T -k $N -o 1 -i 1 -r 10 -g 1 -f ../output/output_mem.csv
    done
done

echo "Benchmark memory footprint completed!"
