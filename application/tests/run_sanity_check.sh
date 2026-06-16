#!/bin/bash

OPTIMAL_NODES=100

mkdir -p ../output
rm -f ../output/sanity_check.csv

echo "Running Sanity Check: Baseline Kernel..."
../application.out -t 1000 -k $OPTIMAL_NODES -o 10 -i 1 -r 2 -g 0 -f ../output/sanity_check.csv

echo "Running Sanity Check: CUDA Graph..."
../application.out -t 1000 -k $OPTIMAL_NODES -o 10 -i 1 -r 2 -g 1 -f ../output/sanity_check.csv

echo "Sanity check completed!"
