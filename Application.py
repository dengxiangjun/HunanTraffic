from tkinter import *
import tkinter.messagebox
from TrafficCrawer import TrafficCrawer
import time
import threading

#
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # self.nameInput = Entry(self)
        # self.nameInput.grid(row=0)
        # self.submitBtn = Button(self, text='确定', command=self.submit)
        # self.submitBtn.grid(row=1)

        self.keyLabel = Label(self, text="高德地图Web服务密钥").grid(row=0, column=0, sticky=W)
        self.keyValue = StringVar()
        self.keyValue.set("51e09b8a50bc85f3bbc85a40822d3abf")
        self.key = Entry(self, textvariable=self.keyValue, width=35)
        self.key.grid(row=0, column=1, columnspan=3)

        self.lngLabelStart = Label(self, text="经度(起)").grid(row=1, column=0, sticky=W)
        self.latLabelStart = Label(self, text="纬度(起)").grid(row=1, column=2, sticky=W)
        self.lngStart = Entry(self)
        self.lngStart.grid(row=1, column=1, padx=15, pady=15)
        self.latStart = Entry(self)
        self.latStart.grid(row=1, column=3, padx=15, pady=15)

        self.lngLabelEnd = Label(self, text="经度(终)").grid(row=2, column=0, sticky=W)
        self.latLabelEnd = Label(self, text="纬度(终)").grid(row=2, column=2, sticky=W)
        self.lngEnd = Entry(self)
        self.lngEnd.grid(row=2, column=1, padx=15, pady=15)
        self.latEnd = Entry(self)
        self.latEnd.grid(row=2, column=3)

        self.isHigeSpeedVal = IntVar()
        self.isHigeSpeed = Checkbutton(self, text="只要高速", variable=self.isHigeSpeedVal)
        self.isHigeSpeed.grid(row=3, column=1, sticky=W)
        self.frenquencyLabel = Label(self, text="频率(秒)").grid(row=3, column=2)
        self.frenquency = Entry(self)
        self.frenquency.grid(row=3, column=3, padx=15, pady=15)

        self.submitBtn = Button(self, text='开始爬取', command=self.submit).grid(row=4, columnspan=4, padx=15, pady=15)
        self.stopBtn = Button(self, text='停止爬取', command=self.stop).grid(row=5, columnspan=4, padx=15, pady=15)
        self.stopFlag = FALSE

        self.log = StringVar()
        self.logContainerLable = Label(self, textvariable=self.log, wraplength=700).grid(row=6, columnspan=60, rowspan=40)

    def submit(self):
        print(self.isHigeSpeedVal.get())
        self.log.set("正在爬取搞得地图数据...")
        self.stopFlag = FALSE
        lngStart = self.lngStart.get()
        latStart = self.latStart.get()
        frenquency = self.frenquency.get()
        lngEnd = self.lngEnd.get()
        latEnd = self.latEnd.get()
        key = self.key.get()

        print(lngStart.isdigit())
        print(latStart.isdigit())
        print(frenquency.isdigit())
        print(lngEnd.isdigit())
        print(latEnd.isdigit())
        if self.is_number(lngStart) and self.is_number(latStart) and self.is_number(frenquency) and self.is_number(lngEnd) and self.is_number(latEnd):
            level = 5

            if self.isHigeSpeedVal.get() == 1:
                level = 1 #高速公路
            trafficCrawer = TrafficCrawer(baselng=float(lngStart), baselat=float(latStart), finlng=float(lngEnd), finlat=float(latEnd), key=key, app=self, frenquency=int(frenquency), level=level)
            timer = threading.Timer(1.0, trafficCrawer.fectchTraffic)
            timer.start()
        else:
            self.log.set("请输入数字")

    def stop(self):
        self.stopFlag = TRUE
        self.log.set("已停止爬取，您可点击开始爬取按钮继续爬取交通态势信息")

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)

#main函数
if __name__=="__main__":
    app = Application()
    # 设置窗口标题:
    app.master.title('交通态势信息爬取')
    center_window(app.master, 800, 540)
    # 主消息循环:
    app.mainloop()