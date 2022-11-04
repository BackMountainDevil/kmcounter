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