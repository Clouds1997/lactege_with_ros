# 轻量级实例分割模型yolact于ros系统中的集成

**YolactEdge**, 是一个实时的实例分割模型，可以达到 30.8 FPS on a Jetson AGX Xavier (and 172.7 FPS on an RTX 2080 Ti)with a ResNet-101 backbone on 550x550 resolution images. 

论文地址 [paper](https://arxiv.org/abs/2012.12259).
项目地址 [github](https://github.com/haotian-liu/yolact_edge)  在这个里面可以找到我们所需的模型

## 工作：

本项目是将YolactEdge集成于ros系统中，编写一个ros节点，读取rosbag中的图像数据，并通过cv_bridge转换后， 通过yolact模型进行实例分割，输出所需的锚框和mask信息，供后续的节点使用。

## 效果：

![example-gif-1](https://github.com/Clouds1997/lactege_with_ros/blob/main/data/yolact_edge_example_1.gif)

![example-gif-1](https://github.com/Clouds1997/lactege_with_ros/blob/main/data/yolact_edge_example_2.gif)


## 安装和使用：

首先需要编译里面的cv_bridge，这就依赖于opencv3，[opencv3安装](https://blog.csdn.net/public669/article/details/99044895) 可以照着这个老哥的来。
然后就要信息cv_bridge的编译工作了，这里注意，要使用python3来进行编译，所以要先配置catkin, 下面的命令要根据自己是python3.5还是3.几来进行更改。
 ```Shell
catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.5m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.5m.so #寻找对应位置
catkin config --install
   ```

查看现有的安装于ros系统的cv_bridge版本
 ```Shell
apt-cache show ros-melodic-cv-bridge | grep Version
输出显示        Version: 1.13.0-0bionic.20210505.032238
cd src/vision_opencv/
git checkout 1.13.0
cd ../../
catkin build cv_bridge
source install/setup.bash --extend
   ```

然后到scripts脚本文件夹，先参照原工程搭建python环境[链接在此](https://github.com/haotian-liu/yolact_edge/blob/master/INSTALL.md)，然后就可以直接启动
 ``` Shell
python3 talker.py
 ``` 

其中，为了防止图像失真，在talker.py文件中，采用了打padding的方式，这里的四个数值分别对应上下左右，可以将长条形的图像padding为方的，检测效果好很多。
 ``` Python
im_padding = cv2.copyMakeBorder(cv_image,200,200,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
 ``` 
