# pyncnn
python wrapper of [ncnn](https://github.com/Tencent/ncnn) with [pybind11](https://github.com/pybind/pybind11), only support python3.x now.

## Prerequisites

**On Unix (Linux, OS X)**

* A compiler with C++11 support
* CMake >= 2.8.12

**On Windows**

* Visual Studio 2015
* CMake >= 3.1

## Build
1. clone [ncnn](https://github.com/Tencent/ncnn) and [pybind11](https://github.com/pybind/pybind11), build and install with default setting, if you change the install directory, change the cmake commond with your setting.
```bash
cd /path/to/ncnn
mkdir build && cd build
cmake ..
make -j4
make install
```
2. update `ENVS_EXECUTABLE`,`ENVS_LIB` and `ENVS_INCLUDE` to your path in `CMakeLists.txt`
3. remove `find_package(Python3)` in `CMakeLists.text`, **this step is optional, it's up to your environment**
4. change /path/to to your path and running the following cmd
```bash
cd /path/to/pyncnn
mkdir build
cd build
cmake -DCMAKE_PREFIX_PATH=/path/to/ncnn/build/install/lib/cmake/ncnn/ ..
make
如果编译失败
则进入src 目录手动编译
cp /path/to/build/install/lib/libncnn.a ./
g++ -O3 -shared -std=c++11 -fopenmp -o ncnn`python3-config --extension-suffix` -fPIC `python3 -m pybind11 --includes` -I/path/to/build/install/include/ncnn/ main.cpp ./libncnn.a
cd ../python
python3 setup.py install
如果Python导入ncnn出错，可以尝试 python3 setup.py bdist_wheel   
然后cd dist   pip3 install ncnn-0.0.1-py3-none-any.whl
```

## Tests
**test**
```bash
cd /path/to/pyncnn/tests
python3 test.py
```

**benchmark**
```bash
cd /path/to/pyncnn/tests
python3 benchmark.py
```

**benchmark gpu(build ncnn with vulkan)**
```bash
cd /path/to/pyncnn/tests
python3 benchmark_gpu.py
```

## numpy
**ncnn.Mat->numpy.array, with no memory copy**
```bash
mat = ncnn.Mat(...)
mat_np = np.array(mat)
```

**numpy.array->ncnn.Mat, with no memory copy**
```bash
mat_np = np.array(...)
mat = ncnn.Mat(mat_np)
```

## model zoo
install requirements
```bash
pip install tqdm requests portalocker opencv-python
```
then you can import ncnn.model_zoo and get model list as follow:
```bash
import ncnn
import ncnn.model_zoo as model_zoo

print(model_zoo.get_model_list())
```
all model in model zoo has example in examples folder
