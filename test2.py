import threading
import ctypes
import time
from time import sleep
import time
from datetime import datetime, date
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor


# カスタムスレッドクラス
class twe(threading.Thread):
    def __init__(self, group=None, target=None, name=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        return

    # def run(self):
    #     self._target(*self.args, **self.kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # 強制終了させる関数
    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            print('Failure in raising exception')

def task():
    model = YOLO("yolov8n.pt")
    try:
        while True:
            # リアルタイム人物検出    
            results = model.predict(source="0", show=True, save_crop=True, save_txt=True, save_conf=True, classes=[0], conf=0.50)
            print(results)
            sleep(5)
    finally:
          print('ended')


def main():
    # nameは任意
    # targetは対象となる関数
    # args, kwargsには関数に渡す引数
    x = twe(name = 'Thread A', target=task)
    # 対象の関数を別スレッドで実行する
    x.start()

    # スレッドが終了するか、指定秒間経過(タイムアウト)するか、いずれかまで待機
    x.join(300)
    # x.join(43200) #9時-21時
    # スレッドが終了していない場合、強制終了処理を実行
    if x.is_alive(): x.raise_exception()

    # 終了しているのでもう待機しないはず
    x.join()
    # スレッドが生きていないことを確認
    print(x.is_alive())

main()