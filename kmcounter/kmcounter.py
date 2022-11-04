from Screenkey.inputlistener import *
import json


KMDATA = {}  # 暂存数据的全局变量


if __name__ == "__main__":
    try:  # 读取文件中 的数据
        dataFile = open("kmdata.json", "r")
        KMDATA = json.load(dataFile)
        dataFile.close()
    except Exception as e:
        print(e)
        dataFile.close()

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

        try:  # 保存数据到文件
            dataFile = open("kmdata.json", "w")
            json.dump(KMDATA, dataFile)
            dataFile.close()
        except Exception as e:
            print(e)
            dataFile.close()

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
