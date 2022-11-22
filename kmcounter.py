from Screenkey.inputlistener import *
import json
import signal


class KMCounter(InputListener):
    def __init__(
        self,
        input_types=InputType.all,
        kbd_compose=True,
        kbd_translate=True,
    ):
        super().__init__(None)
        self.event_callback = self.callback  # 提前设置好按键回调事件
        self.input_types = input_types
        self.kbd_compose = kbd_compose
        self.kbd_translate = kbd_translate
        self.lock = threading.Lock()
        self.stopped = True
        self.error = None
        self.kmdata = {}  # 暂存按键数据的变量
        self.kmdata_file = "kmdata.json"  # 默认保存的数据文件
        self.load_data()  # 尝试加载历史数据
        signal.signal(signal.SIGTERM, self.signal_handler)  # 注册 SIGTERM 信号回调函数

    def exit(self):
        print("exiting...")
        if self.is_alive():
            self.save_data()  # 存一下数据，程序就要关闭了
            self.stop()
            self.join()
        elif self.error:
            print("initialization error: {}".format(self.error))
            if "__traceback__" in dir(self.error):
                import traceback

                traceback.print_tb(self.error.__traceback__)
            exit(1)

    def load_data(self):
        try:  # 读取文件中 的数据
            dataFile = open(self.kmdata_file, "r")
            self.kmdata = json.load(dataFile)
            dataFile.close()
            print("load kmdata from  ", self.kmdata_file)
        except FileNotFoundError:
            print("kmdata file not found  ", self.kmdata_file)
        except Exception as ex: # 其它未知错误，比如 JSONDecodeError
            print("Exception:", repr(ex))
        finally:
            self.save_data()

    def save_data(self):
        try:  # 保存数据到文件
            dataFile = open(self.kmdata_file, "w")
            json.dump(self.kmdata, dataFile)
            dataFile.close()
            print("kmdata has been saved to ", self.kmdata_file)
        except Exception as e:
            print(e)

    def signal_handler(self, signum, frame):
        signame = signal.Signals(signum).name
        print(f"Signal handler called with signal {signame} ({signum})")
        self.exit()

    def callback(self, data):
        if isinstance(data, KeyData):  # keyboard event
            if data.symbol is None:
                # TODO: Investigate what causes this to happen.
                # I caught it once in pdb, but in this function, not in inputlistener,
                # and KeyData doesn't contain enough info.
                return
            symbol = data.symbol.decode()
            if data.pressed:
                print("Key pressed {:5}(ks): {}".format(data.keysym, symbol))

                if symbol in self.kmdata:  # 更新数据
                    self.kmdata[symbol] = self.kmdata[symbol] + 1
                else:
                    self.kmdata[symbol] = 1
                print(self.kmdata)

        elif isinstance(data, ButtonData):  # mouse_btn event
            if data.pressed:
                print("Mouse button pressed %d" % (data.btn))

                # 鼠标的按键没有 keysym 和对应的 symbol，采取组合办法
                symbol = "mbtn" + str(data.btn)
                if symbol in self.kmdata:  # 更新数据
                    self.kmdata[symbol] = self.kmdata[symbol] + 1
                else:
                    self.kmdata[symbol] = 1
                print(self.kmdata)

        else:
            print("unhandled event type {}".format(type(data)))


if __name__ == "__main__":

    kl = KMCounter()

    try:
        # keep running only while the listener is alive
        kl.start()
        while kl.is_alive():
            glib.main_context_default().iteration()
    except KeyboardInterrupt:
        print("Error ", KeyboardInterrupt)
        kl.exit()
