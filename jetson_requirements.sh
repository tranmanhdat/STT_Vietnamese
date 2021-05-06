# Install PyQt5
sudo apt-get install python3-pyaudio
sudo apt-get install python3-pydub
sudo apt-get install python3-pyqt5

# Install tensorflow
pip3 install pybind11
pip3 install numpy
pip3 install Cython
sudo apt-get install libffi-dev
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 'tensorflow>=2'

# INstall llvm 9.0.0
wget https://releases.llvm.org/9.0.0/llvm-9.0.0.src.tar.xz
cd llvm-9.0.0.src
mkdir llvm_build_dir && cd llvm_build_dir/
cmake ../ -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="ARM;X86;AArch64"
make -j2
sudo make install\
cd bin/
echo "export LLVM_CONFIG=\""`pwd`"/llvm-config\"" >> ~/.bashrc
echo "alias llvm='"`pwd`"/llvm-lit'" >> ~/.bashrc
source ~/.bashrc

# Install TBB 0.50.x
git clone https://github.com/wjakob/tbb.git
cd tbb/build
cmake ..
make -j2
sudo make install


pip3 install -r jetson_reqirements.txt