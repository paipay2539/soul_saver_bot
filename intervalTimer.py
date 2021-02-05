import threading


class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function


stopFlag = threading.Event()
thread = MyThread(stopFlag)
thread.start()
# this will stop the timer
stopFlag.set()
