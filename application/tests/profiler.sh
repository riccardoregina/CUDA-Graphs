#!/bin/bash

mkdir -p ../output
rm -f ../output/profiler.csv ../output/report.nsys-rep ../output/report.sqlite ../output/report.qdstrm

nsys profile --trace=cuda --stats=true -o ../output/report ../application.out -t 10 -k 10 -o 40 -i 10 -r 10 -g 1 -f ../output/profiler.csv
