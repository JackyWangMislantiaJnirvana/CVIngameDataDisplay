# CVDD Client用户指南

`Cresent Ville Data Display`（简称`CVDD`）是一套用来将Minecraft游戏内的信息收集汇总，上传到一个网页绘制成可视化的图表/仪表盘展示出来，以实现*在游戏外就能监控游戏里面机器的运转情况* 的一套软件/服务。这套系统采用服务器-客户端架构，客户端运行在Minecraft内`Opencomputers`模组的电脑上。

为了保持直观，这个指南用了很多*伪代码* 来说明问题。反正别把它们当成真正的Lua代码了，嗯，大家都懂，都懂。CVDD也提供了一个真正的代码实例，点击[这里](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/client/client/src/example_MCU.lua)查看。

## 这玩意儿到底干什么使的？

我们用一个直观的例子来说明CVDD能干什么。设想你打算用了一台电脑，让它在反应堆过热时紧急关闭反应堆，然后写了这样一个程序来实现：

``` lua
-- 自动控制程序一般都是这么个死循环：收集信息→做判断→行动→返回第一步。
-- 我们管跑这种死循环程序，做自动控制的电脑叫微控制器(MCU)，
-- 你可以用这样的电脑来给你监控反应堆、根据电力需求打开或关闭发电机、
-- 根据产品储备量控制生产线的运行与否、给坩埚投料...很多自动化任务都可以代劳。
while true do
    if 温度超过安全范围 then
        紧急关闭反应堆！
    end
end
```

你想在监控反应堆的同时，让这台电脑*把当前的炉温在某个地方漂亮地显示出来* 。怎么办呢？你想写这样的代码：

``` lua
while true do
    if 温度超过安全范围 then
        紧急关闭反应堆！
    end
    提交当前温度数据！ --等下，往哪里提交？提交什么样的数据？又用啥来显示？...
end
```

显然这样有点超现实：有许多细节问题没有考虑，比如注释里的那几个。CVDD的存在意义就是让你**忽略掉**这些细节，专心于**“你想拿这个MCU实现什么功能？”、“你想收集并提交什么数据？”**这样的核心问题。

```lua
-- 将CVDD提供的dataProvider插件包含到程序中
local dataProvider = require("CVDDDataProvider")
-- 将dataProvider所需的相关服务注册到操作系统中（就是个初始化步骤）
dataProvider.registerProviderService()

-- 主循环
while true do
    if 温度超过安全范围 then
        紧急关闭反应堆！
    end
    
    -- 提交一个名为"温度"（英文）的物理量，单位留空（因为IC2的反应堆温度貌似就是没有单位...）
    dataProvider.submitPhyQuantity("Temperature", 反应堆的温度)
end
```

提交什么格式的数据？你能提交的数据的格式被定义在了[这份文档](data_types.md)中，刚才用的是`phyQuantity`即`物理量`这个格式。往哪里提交？用啥来显示？这就是被CVDD包办的细节部分了。**当然，你也需要进行正确的调♂教让CVDD能正确的受你使♀唤。**

## 运行原理

![CVDDClient原理图](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/raw/master/client/doc/CVDDClient%E5%8E%9F%E7%90%86%E5%9B%BE.jpg)

### 组成部分

CVDD系统的客户端由两个部分组成：`Central`程序和`DataProvider`插件。

- 我们用`MCU`这个词来指代你游戏中用来控制机器的电脑（比如，根据现有电力需求大小自动开关发电机的电脑）。`DataProvider`是一个模块，提供了提交数据的接口。如果你想让CVDD采集这台`MCU`上的数据，你需要将这个模块包含到你在`MCU`上运行的程序里，并且在**自己认为合适的时候**调用相应接口来提交数据。
- `Central`负责每隔一定时间，向每个`DataProvider`依次发送请求，然后将收集到的回复汇总，上传到CVDD的网页服务器。这个程序运行在一台专门的电脑上，这台电脑必须和所有提交数据的`MCU`之间具有网络连接。我们管这台电脑叫`中心机`

### 工作流程

我们还是以刚才那台监控反应堆的`MCU`为例，来理一下这一切是如何工作的。

1. 每次循环中，`MCU`上的程序将温度数据提交给`DataProvider`模块。提交的数据进入`DataProvider`里面的一块缓存。
2. 运行在`中心机`上的程序会每隔一定时间（默认20秒）就把所有在它那里登记在案的`MCU`全部问候一遍（你家可能不止有这台监控反应堆的`MCU`，可能还有控制发电机的、控制生产线的、报告某个玩家这次又是怎么死的（？）的等等许多`MCU`），向它们发送请求。
3. 当一个来自`中心机`的请求被`MCU`接收到，一个由`DataProvider`事先注册进操作系统的事件处理程序被激活（还记得前面调用的`dataProvider.registerProviderService()`么？就是在注册事件处理程序），把缓存内的数据打包发送给`中心机`。
4. `中心机`将收集到的所有数据打包，上传到CVDD网页服务器。

#### ❓为什么中心机和MCU要异步运行

有人可能会好奇为何CVDD要先将想要提交的数据缓存起来，再发给中心机。为何不**在调用`DataProvider`接口的时候就直接把东西发过去**（*同步运行*）？

众所周知，网络通信是个玄学的东西，即使是`OpenComputers`里面虚构的计算机网络也是一样。它的响应速度远远不如`MCU`该有的运行速度。`MCU`为了保证自己能实时响应外界情况的变化（如，随时检查反应堆的温度是否是安全的），每次主循环（感知、决策、执行）的耗时至少在50毫秒以下。如果采用了上述同步运行的策略，如此高频率（<50ms一次的请求频率）的消息发送会直接让网络系统像堵厕所一样堵起来（听说过DOS攻击么？）。

另外，`MCU`上运行的主循环会被慢得多的网络通信给“卡住”，即*阻塞（Block）*。在某种情况下这是一件危险的事情：设想你用这样一个程序来监控你家的反应堆，可电脑却把时间全都花在网络延迟上了...可能会导致一些戏剧性的结果。

> 你嫌快，我嫌慢；我等不了你，你追不上我，咋办？！干脆我把东西放在某个地方就溜，你自己来取。~~你追我，如果你追到我，我就让你嘿嘿嘿~~

所以说这里用了一个*缓存* 来实现异步运行：`MCU`提交数据只是在读写内存里一块缓存，速度飞快；`中心机`隔一段时间通过网络发来一个请求，把缓存里的数据读走。

#### ❗分清楚网络和互联网

本文用`网络`一词指代游戏里面`Opencomputers`的计算机网络，而用`互联网`一词指代那个真正的计算机网络（Internet）。特容易混，别搞混了。

## 安装方法

要把CVDD的系统架起来，除了那些`MCU`，你还需要专门弄一台和各个`MCU`有网络连接的电脑来做`中心机`。你需要在`MCU`和`中心机`上安装不同的软件。

1. 共通步骤：安装CVDD的下载工具。给你的电脑插上一张因特网卡，执行命令：

``` shell
wget https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/client/client/tools/clientDeployTool.lua clientDeployTool.lua
```

（在这里整个复制下来，再把鼠标滚轮按下去即可粘贴在`Opencomputers`的终端里，回车执行）

2. 在`MCU`上执行`clientDeployTool mcu`，在`中心机`上执行`clientDeployTool central`。工具会自动下载所有需要的文件。若无异常（出现红色字），安装成功。

（只有`中心机`长期需要因特网卡，`MCU`上的可以装完软件之后拆下来给别人用）

## 编程接口

下面详细介绍如何在自己的`MCU`程序中使用`DataProvider`模块。

```lua
-- 引入模块
local dataProvider = require("CVDDDataProvider")

-- 必要的步骤：让dataProvider注册事件处理程序
dataProvider.registerProviderService()

-- 程序的主循环
while true do
    ...做各种事...
    
    在程序的任何地方随意提交数据！
end
```

可提交的数据有5种（详见[这份文档](data_types.md)），对应5种接口：

| 函数定义                               | 备注                   |
| -------------------------------------- | ---------------------- |
| `submitText(name, value)`              | 文本                   |
| `submitBoolean(name, value)`           | 布尔值                 |
| `submitphyQuantity(name, value, unit)` | 物理量                 |
| `submitVector(name, ...)`              | 向量(也可以理解为序列) |
| ~~`submitImage()`~~                    | 图像，尚未实现         |

## 配置方法

为了能让`中心机`顺利地找到`MCU`并且让CVDD服务器分清楚不同的`MCU`，你需要注册`MCU`网卡的硬件地址

```c
// TODO
```

##更进一步

- 如果你想了解你提交进`DataProvider`的数据一路上都经历了什么，你可以查看[关于数据传输方式的规范文档](com_mechanism.md)。
- 如果你觉得看完这篇文章还不过瘾，**要 不 要 去 翻 翻 源 码 呢**

```c
// TODO
```

