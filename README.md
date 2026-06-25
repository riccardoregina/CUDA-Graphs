# Kernel Batching with CUDA Graphs - Review

Project developed for the *Parallel High Performance Computing* course at the *University of Naples Federico II* in the academic year 2025-2026. This project is a replication study and performance validation of the kernel batching strategy utilizing CUDA Graphs, based on the paper [*Boosting Performance of Iterative Applications on GPUs: Kernel Batching with CUDA Graphs*](https://arxiv.org/abs/2501.09398).

**Authors**
* [Giuseppe DI MARTINO - DE5000042](https://github.com/giuseppedima)
* [Riccardo REGINA - DE5000024](https://github.com/riccardoregina)

**Teacher**
* [Valeria MELE](https://www.docenti.unina.it/valeria.mele)

## Directory Structure
* [`application/`](./application): Contains the CUDA C++ source code for the benchmark application.
  * [`application/tests/`](./application/tests): Bash scripts to automate the execution of benchmarks.
* [`article/`](./article): LaTeX source files for the replication study report.
* [`plotting/`](./plotting): Python scripts to parse CSV outputs and generate evaluation graphs.
* [`assets/`](./assets): Pre-generated results and plots for different GPU architectures (RTX 3070, GTX 1060, Tesla T4).

## Setup and Build
To compile the CUDA application, navigate to the `application` directory and run `make`:
```bash
cd application
make
```
This will compile the source code and generate the `application.out` executable.

## Running the Application
You can run the executable with custom parameters:
```bash
./application.out -t <num_threads> -i <inner_iterations> -k <mini_batch_size> -o <outer_iterations> -r <repetitions> -s <seed> -g <use_graph>
```
For information about the supported parameters, refer to the the [article]( ./article/main.tex).

You can also use the automated bash scripts located in `application/tests/`:
```bash
cd application/tests
./run_increase_nodes.sh
./run_increase_iterations.sh
```

For more information about how to use the bash scripts, refer to the [article]( ./article/main.tex). Do not forget to update the configuration variables inside the bash scripts according to your needs.

## Generating Plots
To generate the visualizations from the benchmark outputs, navigate to the `plotting` directory, install the required dependencies, and run the Python script:
```bash
cd plotting
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python plots.py
```
