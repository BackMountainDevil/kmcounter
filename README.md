# 说明

原项目为[screenkey](https://www.thregr.org/~wavexx/software/screenkey/)，在 tag v1.5 的基础上添加计数功能


```
├── Screenkey
│   ├── __init__.py
│   ├── inputlistener.py    运行后可以在终端输出 按键的编码
│   ├── keysyms.py  编码对应的按键
│   ├── labelmanager.py
│   ├── screenkey.py    主程序，运行后可以显示按下的按键、鼠标点击和滚动
│   └── xlib.py 通过 x11 获取输入
├── setup.cfg
└── setup.py
```

# Change Log
## 2022.11.4

feature 监听键盘按键按下事件+鼠标按键按下事件

feature 按键次数数据存储到文件

refactor 数据的读取和保存

question `glib.main_context_default().iteration()` 不理解作用，尝试去掉则程序无法正常运行

字母、数字、方向运算符、TAB可以长摁也会累加次数，鼠标按键、shift、ctrl、alt、super 则不会

# refer

[Commit message 和 Change log 编写指南  阮一峰 2016年1月 6日](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html)
