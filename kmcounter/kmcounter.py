from Screenkey.inputlistener import *


if __name__ == "__main__":

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

        elif isinstance(data, ButtonData):  # mouse_btn event
            if data.pressed:
                print("Mouse button pressed %d" % (data.btn))
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
