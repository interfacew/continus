# GestureMate

该项目是一个自动化控制平台，它利用智能姿态识别技术，实现了对用户手势和身体动作的精准捕捉与深度解析。通过这种技术，平台能够识别并响应用户的每一个动作，从而触发和执行一系列自动化任务，极大地提升了操作的灵活性和效率

## 使用方法

- 克隆仓库到本地
- 运行`conda create -n gesturemate python=3.11`（可选）
- 运行`pip install -r requirement.txt`（可选，主程序会自动检测环境内是否包含项目所需库，如果未检测到会进行自动下载）
- 首次运行`python Main.py`会在`./data/`目录下生成一个`config.json`并下载所需的依赖
- 编写合适的`config.json`，详情见[任务编写](#任务编写)
- 可以运行`python GetPoseJson.py`帮助你生成在`config.json`里可能用到的**存放姿势数据的 json 文件**
- 运行`python Main.py`

> 你可以使用`python Main.py --help`获取更多的参数

## Demo

本项目提供了三个`demo`，分别是一个手势控制的计算器和两个`socketHook`的实例\
位于`example`文件夹下\

### 计算器

这是一个通过手势识别进行计算器操作的`demo`\
你可以使用`python Main.py --data=".\example\data_example"`运行计算器\
在系统识别到左手大约 2 秒后，它会自动启动计算器程序。\
用户可以通过将左手手心面向镜头，比出数字进行数字输入。\
对于运算法则的输入则会根据用户右手手指的指向与手心方向进行判断：\
在手心朝前时，指向上方表示加法，指向左方表示乘法。而手心朝向后方时则同理表示减法和除法。

双手食指交叉会退出计算器并重新开始检测左手

### `socketHook`

#### 简单的 `socket` 服务器

这是一个能实时向指定服务器传输当前识别结果的`demo`\
在运行此`demo`前，请先运行`python .\example\socket_example\socketserver.py`\
随后开启第二个终端运行`python Main.py --data=".\example\socket_example"`\
启动后，当检测到左手或右手时，你会看到`socketserver`显示出的小框里的点，这些是主程序通过`socket`传输过去的东西\
当右手和左手均不在范围内时，传输会停止，`socketserver`显示出的小框中应不发生变化\
同时`socketserver`程序会打印出收到的时间戳与连接/断开时的日志

#### `fingerspell`

这是一个`ASL`单字母手语识别翻译`demo`\
环境额外需求：请安装`script/requirements.txt`里的包\
先运行`script/train.py`训练模型（可选，`demo`内自带模型）\
随后运行`script/task.py`启动监听（需配合主程序使用）\
或运行`script/fingerspell.py`以直接识别（无需启动主程序）

## 任务编写

任务的编写在`config.json`中，`config.json`应是这样:

```c++
[
    // task 1
    {
        "type":"type", // 任务类型
        "id":"id", // 任务 id (唯一)
        "start":true/false, // 任务是否初始启动
        "nextTasks":[ // 运行指令之后对任务激活进行修改
            {
                "operate":"start"/"stop", // 启动/停止任务
                "id":"id" // 目标任务 id
            },
            ...
        ],
        ...
    },
    // task 2
    ...
]
```

任务在满足条件后会自动停止自己的运作，如需要循环运行请在`nextTasks`中重新启动自身

## 任务类型

允许六种任务：

- [执行命令](#执行命令)
- [模拟按键](#模拟按键)
- [身体形态识别](#身体形态识别)
- [延时任务](#延时任务)
- [检测任务](#检测任务)
- [`socket`监听](#socket监听)
- [`http`请求](#http请求)

### 执行命令

命令执行是一个任务，应如下编写：

```c++
{
    "type":"command", // 任务类型
    "id":"id", // 任务 id (唯一)
    "command":[ // 满足条件运行的命令(可为空数组)
        "start example.exe", // 按顺序运行的命令(可为空字符串)
        "python ./example.py",
        ...
    ],
    "timeout":[ // 命令运行的最大时间(0表示不限制，单位为秒)
        0.5,
        0,
        ...
    ],
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

你可以在命令中使用`%s`，他们会被替换成识别到的姿势位置\
替换后为一个无空格`json`，与`python GetPoseJson.py`生成的`output.json`格式相同\
如需原始的`%`，请使用`%%`

> 当`timeout`长度不如`command`时，余下位置会补`0`，当超过`command`时，多余的数据被忽略

### 模拟按键

模拟按键任务应如下编写：

```c++
{
    "type":"keypress", // 任务类型
    "id":"id", // 任务 id (唯一)
    "keys":[ // 满足条件运行的按键(可为空数组)
        ["key1","key2","key3",...], // 快捷键列表
        ...
    ],
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

此处的`key1`，`key2`……应该在`pyautogui.KEYBOARD_KEYS`里\
`pyautogui.KEYBOARD_KEYS`为以下列表

```python
[
    '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'alt', 'altleft', 'altright', 'command', 'ctrl', 'ctrlleft', 'ctrlright', 'option', 'optionleft', 'optionright', 'shift', 'shiftleft', 'shiftright', 'win', 'winleft', 'winright',
    'backspace', 'capslock', 'del', 'delete', 'enter', 'esc', 'escape', 'fn', 'insert', 'return', 'space', 'tab',
    'down', 'left', 'right', 'up', 'end', 'home', 'pagedown', 'pageup', 'pgdn', 'pgup',
    'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'add', 'decimal', 'divide', 'multiply', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'subtract',
    'pause', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'scrolllock',
    'accept', 'apps', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'clear', 'convert', 'execute', 'final', 'hanguel', 'hangul', 'hanja', 'help', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'modechange', 'nexttrack', 'nonconvert', 'playpause', 'prevtrack', 'print', 'select', 'separator', 'sleep', 'stop', 'volumedown', 'volumemute', 'volumeup', 'yen'
]
```

在运行`python Main.py`的时候会对你的`config`进行检查，因此你不需要担心写错的问题

### 身体形态识别

身体形态识别可以识别身体特点位点的形态, 在与对应数据相似时执行\
身体形态识别任务应如下编写：

```c++
{
    "type":"match", // 任务类型
    "id":"id", // 任务 id (唯一)
    "bodyPart":[
        ["bodyPart1","bodyPart2",...], // 需要识别的部位，与 poseFile 一一对应
        ["bodyPart1","bodyPart2",...] // bodyPart 为 ["face","leftHand","rightHand","body"] 其一
        ...
    ],
    "poseFile": [
        "path-to-json1", // 匹配数据路径
        "path-to-json2",
        ...
    ],
    "sensetive": [
        0.01, // 检测敏感度，与 poseFile 一一对应
        0.01,
        ...
    ],
    "frames": [
        30, // 连续多少帧检测到才运行，与 poseFile 一一对应
        20,
        ...
    ],
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

匹配数据可由`python GetPoseJson.py`获取，启动后会捕捉人体，按`s`后会保存当前姿态，此时可以查看其他动作的`sensetive`值，按`q`后会退出并将姿态保存在当前目录下的`output.json`中

### 延时任务

延时任务可以在被激活后延时一段时间执行，可以被其他任务的`nextTasks`打断\
延时任务应如下编写：

```c++
{
    "type":"timeout", // 任务类型
    "id":"id", // 任务 id (唯一)
    "timeout":time, // 时间(整数，毫秒)
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

时间从任务被启动时开始计时\
当延时还没有结束而再次启动时，计时会被刷新

### 检测任务

检测任务可以在检测到对应的身体部位时执行\
检测任务应如下编写：

```c++
{
    "type":"detect", // 任务类型
    "id":"id", // 任务 id (唯一)
    "bodyPart":[
        "bodyPart1", // 需要识别的部位
        "bodyPart2", // bodyPart 为 ["face","leftHand","rightHand","body"] 其一
        ...
    ],
    "frames":frames, // 连续多少帧检测到才运行
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

### `socket`监听

`socket`监听任务用于将检测到的姿态通过`socket`发送出去\
示例如下:

```c++
{
    "type":"socketsend", // 任务类型
    "id":"id", // 任务 id (唯一)
    "ip":"xxx.xxx.xxx.xxx", // 目标 ip 或主机名
    "port":11111, // 目标端口
    "extra":{...}, // 该字段将在包里的 "extra" 字段中出现(可选)
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

`socket`任务会在启动后建立`tcp`连接\
随后每帧像`ip:port`发送一个这样的包，长度为`44000`，不足的长度在包尾用空格补齐，包尾有`\0`作为特征\

```js
{
    "pose":{ // 姿态状态，与 GetPoseJson.py 生成的 json 相同
        "body":[
            [x,y,z],
            ...
        ]/null,
        "rightHand":[
            [x,y,z],
            ...
        ]/null,
        "leftHand":[
            [x,y,z],
            ...
        ]/null,
        "face":[
            [x,y,z],
            ...
        ]/null,
    },
    "time":time // posix 时间戳，float 类型
}
```

在被其他任务终止之后或连接出错的时候发送一次`quit\0`并关闭`tcp`连接，同时执行`nextTasks`里的操作

### `http`请求

`http`请求任务用于在特定位置发送`http`请求或将检测到的姿态通过`http`发送出去\
示例如下:

```c++
{
    "type":"request", // 任务类型
    "id":"id", // 任务id(唯一)
    "url":"xxx.xxx.xxx.xxx:xxx/xxx/xxx?xxx=xxx&xxx=xxx", // 目标 url
    "method":"HEAD"/"GET"/"POST"/"PUT"/"PATCH"/"DELETE", // http 请求方式
    "data":{...}, // 用于 post/put/patch (可选)
    "headers":{...}, // 请求头 (可选)
    "cookies":{...}, // cookies 信息 (可选)
    "start":true/false, // 任务是否初始启动
    "nextTasks":[ // 运行指令之后对任务激活状态进行修改
        {
            "operate":"start"/"stop", // 启动/停止任务
            "id":"id" // 目标任务 id
        },
        ...
    ]
}
```

你可以在`data`中使用`"${pose}"`，它将被替换成如下信息：

```js
{
    "pose":{ // 姿态状态，与 GetPoseJson.py 生成的 json 相同
        "body":[
            [x,y,z],
            ...
        ]/null,
        "rightHand":[
            [x,y,z],
            ...
        ]/null,
        "leftHand":[
            [x,y,z],
            ...
        ]/null,
        "face":[
            [x,y,z],
            ...
        ]/null,
    },
    "time":time // posix 时间戳，float 类型
}
```

执行`nextTasks`里的操作
