NVCC = nvcc
NVCC_FLAGS = -O3 -std=c++11

TARGET = benchmark

SRCS = main.cu benchmark.cu kernel.cu utils.cpp

all: $(TARGET)

$(TARGET): $(SRCS)
	$(NVCC) $(NVCC_FLAGS) -o $@ $^

clean:
	rm -f $(TARGET)
