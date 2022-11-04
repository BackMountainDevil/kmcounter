from Screenkey.inputlistener import *
import json


def load_data(fileName="kmdata.json"):
    try:  # 读取文件中 的数据
        dataFile = open(fileName, "r")
        KMDATA = json.load(dataFile)
        dataFile.close()
        return KMDATA
    except Exception as e:
        print(e)
        return {}


def save_data(data, fileName="kmdata.json"):
    try:  # 保存数据到文件
        dataFile = open(fileName, "w")
        json.dump(data, dataFile)
        dataFile.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    KMDATA = load_data()  # 尝试获取历史数据

    def callback(data):
        if isinstance(data, KeyData):  # keyboard event
            if data.symbol is None:
                # TODO: Investigate what causes this to happen.
                # I caught it once in pdb, but in this function, not in inputlistener,
                # and KeyData doesn't contain enough info.
                return
            symbol = data.symbol.decode()
            if data.pressed:
                print("Key pressed {:5}(ks): {}".format(data.keysym, symbol))

                if symbol in KMDATA:  # 更新数据
                    KMDATA[symbol] = KMDATA[symbol] + 1
                else:
                    KMDATA[symbol] = 1
                print(KMDATA)

        elif isinstance(data, ButtonData):  # mouse_btn event
            if data.pressed:
                print("Mouse button pressed %d" % (data.btn))

                # 鼠标的按键没有 keysym 和对应的 symbol，采取组合办法
                symbol = "mbtn" + str(data.btn)
                if symbol in KMDATA:  # 更新数据
                    KMDATA[symbol] = KMDATA[symbol] + 1
                else:
                    KMDATA[symbol] = 1
                print(KMDATA)

        else:
            print("unhandled event type {}".format(type(data)))

    kl = InputListener(callback, InputType.keyboard | InputType.button)

    try:
        # keep running only while the listener is alive
        kl.start()
        while kl.is_alive():
            glib.main_context_default().iteration()
    except KeyboardInterrupt:
        print("Error ", KeyboardInterrupt)

        save_data(KMDATA)   # 保存数据到文件中

    # check if the thread terminated unexpectedly
    if kl.is_alive():
        kl.stop()
        kl.join()
    elif kl.error:
        print("initialization error: {}".format(kl.error))
        if "__traceback__" in dir(kl.error):
            import traceback

            traceback.print_tb(kl.error.__traceback__)
        exit(1)
