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

开启启动 参阅[Autostarting](https://wiki.archlinux.org/title/Autostarting). 我使用的 XFCE DE, 在设置-启动中添加命令即可，如 `sh -c "sleep 3 && cd /home/mifen/Documents/code/screenkey/kmcounter/ && python kmcounter.py"`，而不是 `python /home/mifen/Documents/code/screenkey/kmcounter/kmcounter.py`，后者会存在路径问题无法识别到 kmdata.json 的问题，`cd /home/mifen/Documents/code/screenkey/kmcounter/ && python kmcounter.py`测试发现没法启动

fix 文件不存在不会自动创建的bug

fix 程序在关机时不会自动保存数据的bug

refactor 封装成类，这样接收信号退出的时候就不需要额外传参了

# refer

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
