#!/bin/bash

OPTIMAL_NODES=100

mkdir -p ../output
rm -f ../output/profiler.csv ../output/report.nsys-rep ../output/report.sqlite

nsys profile --trace=cuda,osrt --stats=true -o ../output/report ../application.out -t 10000000 -k $OPTIMAL_NODES -o 40 -i 1 -r 10 -g 1 -f ../output/profiler.csv
