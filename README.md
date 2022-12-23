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
├── setup.py
├── kmdata.json	:	static data
└── kmcounter.py	:	main code
```

# Install

1. install screenkey(v1.5+) or clone screenkey source code
2. if install screenkey, just get kmcounter.py; If clone screenkey source code, get kmcounter.py and put it into screenkey like file tree above.
3. set kmcounter.py autostart. static data will be stored in kmdata.json.

# Change Log
## 2022.12.23

默认布局按键底色为 #cccccc，我将按下次数最少的颜色定义为 #00ffff，次数最多的颜色定义为 #ff0000，那么以按键次数为自变量、颜色为因变量的一次方程为

    f(x) = 0x00ffff + (x-min) * ((0xff0000-0x00ffff) / (max-min))
        = 65535 + (x-min) * ((16711680-65535) / (max-min))
        = 65535 + (x-min) * ((16646145) / (max-min))

[Python max()方法扩展：求字典中值最大的键 千鱼千寻 2020-09-14](https://www.cnblogs.com/QianyuQian/p/13667965.html)

## 2022.11.22

因查阅日志发现本程序的输出占了太大篇幅，因此只留出程序的错误输出。autostart 路径：`sh -c "sleep 3 && cd /home/mifen/Documents/code/kmcounter/ && nohup python kmcounter.py >/dev/null 2>log & "`

## 2022.11.5
refactor 将代码移动到上层目录，解决未安装 screenkey 时无法允许代码的bug

autostart 路径因此有所变化：`sh -c "sleep 3 && cd /home/mifen/Documents/code/kmcounter/ && nohup python kmcounter.py >/dev/null 2>log & "`

## 2022.11.4

feature 监听键盘按键按下事件+鼠标按键按下事件

feature 按键次数数据存储到文件

refactor 数据的读取和保存

question `glib.main_context_default().iteration()` 不理解作用，尝试去掉则程序无法正常运行

字母、数字、方向运算符、TAB可以长摁也会累加次数，鼠标按键、shift、ctrl、alt、super 则不会

开启启动 参阅[Autostarting](https://wiki.archlinux.org/title/Autostarting). 我使用的 XFCE DE, 在设置-启动中添加命令即可，如 `sh -c "sleep 3 && cd /home/mifen/Documents/code/screenkey/kmcounter/ && python kmcounter.py"`，而不是 `python /home/mifen/Documents/code/screenkey/kmcounter/kmcounter.py`，后者会存在路径问题无法识别到 kmdata.json 的问题，`cd /home/mifen/Documents/code/screenkey/kmcounter/ && python kmcounter.py`测试发现没法启动

fix 文件不存在不会自动创建的bug

fix 程序在关机时不会自动保存数据的bug

refactor 封装成类，这样接收信号退出的时候就不需要额外传参了


# refer

[https://github.com/ijprest/keyboard-layout-editor](http://www.keyboard-layout-editor.com/)

[Commit message 和 Change log 编写指南  阮一峰 2016年1月 6日](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html)

## signal

shutdown 是指向 systemctl 的动态链接，systemctl 是可执行文件，可是直接执行 shutdown 会一分钟后关机，执行 systemctl 则不会唉

[python脚本如何监听终止进程行为，如何通过脚本名获取pid 铁柱同学 于 2019-10-30 ](https://blog.csdn.net/LJFPHP/article/details/102827172):signal

[shutdown - Unix, Linux Command](https://www.tutorialspoint.com/unix_commands/shutdown.htm):shutdown 会发送 SIGTERM 信号
> shutdown brings the system down in a secure way. All logged-in users are notified that the system is going down, and login(1) is blocked. It is possible to shut the system down immediately or after a specified delay. All processes are first notified that the system is going down by the signal SIGTERM. 

[what-signal-is-sent-to-running-programs-scripts-on-shutdown](https://unix.stackexchange.com/questions/499761/what-signal-is-sent-to-running-programs-scripts-on-shutdown)
> While on shutdown the running processes are first told to stop by init(from sendsigs on old implementations, according to @JdeBP)/systemd.
>
> The remaining processes, if any, are sent a SIGTERM. The ones that ignore SIGTERM or do not finish on time, are shortly thereafter sent a SIGKILL by init/systemd.

[SIGTERM: Linux Graceful Termination | Exit Code 143, Signal 15 Daniel Slavin October 16th, 2022](https://komodor.com/learn/sigterm-signal-15-exit-code-143-linux-graceful-termination/)
> kill command sends a SIGTERM signal  
> command to send SIGKILL: kill -9 [ID]

[ How to terminate running Python threads using signals November 24, 2016 George Notaras](http://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

[nohup不输出nohup.out日志信息，已解决。勤奋能干二师弟 2019-06-04](https://blog.csdn.net/it_erge/article/details/90799556)
> 只输出错误信息到日志文件  
> nohup java -jar yourProject.jar >/dev/null 2>log &   
> 什么信息也不要   
> nohup java -jar yourProject.jar >/dev/null 2>&1 & 

## similar program

[screenkey](https://gitlab.com/screenkey/screenkey):在屏幕上显示当前按键。keysms.py 中有 `function` 这一行，但是我按下的时候并没有显示出来。super\alt\shift，在偏好设置里打开显示shift，然后显示Mouse才可以看到shift、alt、ctrl。从xlib.py中可以看出来是通过x11的库读取的输入。

[AlynxZhou/showmethekey](https://github.com/AlynxZhou/showmethekey): screenkey 替代方案, 适配 X11 和 Wayland.通过 libinput 获取用户输入。需要root权限，使用上不如screenkey开箱即用，也没心思继续搞懂怎么用。

[KMCounter](https://github.com/telppa/KMCounter):ahk 开源 windows 脚本。功能和界面优秀，commit message 写的一塌糊涂。推出程序时 SaveData 通过 IniWrite 将数据存储到文件（KMCounter.ini）中

[whatpulse](https://whatpulse.org/):闭源，支持三大os。除了记录键盘、还会记录网络传输，隐私协议中收集匿名数据，统计界面看起来更炫酷

[Mousotron : Mouse and keyboard activity monitor](https://www.blacksunsoftware.com/mousotron.html):Windows 7/8/10，闭源 5$，界面看起来很上古
