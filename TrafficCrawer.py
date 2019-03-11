import requests
import pandas as pd
import time
import threading
import os

class TrafficCrawer():
    def __init__(self, baselng, baselat, finlng, finlat, app, key, widthlng=0.05, widthlat=0.04, frenquency=600.0, level=5):
        self.baselng = baselng
        self.baselat = baselat
        self.finlng = finlng
        self.finlat = finlat
        self.key = key
        # self.widthlng = widthlng
        # self.widthlat = widthlat
        self.frenquency = frenquency
        self.app = app
        self.level = level

    def httpGet(self):
        # 初始API的URL
        url = "https://restapi.amap.com/v3/traffic/status/rectangle?key="+ self.key +"&extensions=all&level="+ str(self.level) +"&rectangle="

        # 设定整个网格左下角坐标的经纬度值
        baselng = self.baselng
        baselat = self.baselat
        # 设定每个网格单元的经纬度宽
        widthlng = 0.05
        widthlat = 0.04

        # endlng = self.finlng
        # endlat = self.finlat

        # 用于储存数据
        x = []
        # 用于标识交通态势线段
        num = 0

        startlat = baselat

        try:
            # 循环每个网格进行数据爬取，在这里构建了4X4网格
            while startlat <= self.finlat:
                # 设定网格单元的左下与右上坐标的纬度值
                # 在这里对数据进行处理，使之保留6位小数（不保留可能会莫名其妙出错）
                endlat = round(startlat + widthlat, 6)

                startlng = baselng
                while startlng <= self.finlng:
                    # 设定网格单元的左下与右上坐标的经度值
                    endlng = round(startlng + widthlng, 6)
                    # 设置API的URL并进行输出测试
                    locStr = str(startlng) + "," + str(startlat) + ";" + str(endlng) + "," + str(endlat)
                    thisUrl = url + locStr
                    print(thisUrl)
                    # 爬取数据
                    data = requests.get(thisUrl)
                    s = data.json()
                    print(s['infocode'])
                    if s['status'] is '1':
                        a = s["trafficinfo"]["roads"]
                        # 注意，提取数值需要使用XXX.get()的方式来实现，如a[k].get('speed')
                        # 若使用a[k]['speed']来提取，或会导致KeyError错误
                        for k in range(0, len(a)):
                            s2 = a[k]["polyline"]
                            s3 = s2.split(";")
                            for l in range(0, len(s3)):
                                s4 = s3[l].split(",")
                                x.append(
                                    [a[k].get('name'), a[k].get('status'), a[k].get('speed'), num, float(s4[0]), float(s4[1])])
                            num = num + 1
                    startlng = round(startlng + widthlng, 6)
                    time.sleep(0.1)
                startlat = round(startlat + widthlat, 6)
                    # 若爬取网格较多，可使用time.sleep(秒数)来避免高德的单秒API调用次数的限制
        except Exception  as e:
            #self.app.log.set("查询超过当日次数限制")
            pass
        return x

    # 抓取交通态势数据
    def fectchTraffic(self):

        cnt = 0
        x = []
        while cnt < 10:
            x = self.httpGet()
            if x:
                break
            cnt = cnt + 1

        # 将数据结构化存储至规定目录的CSV文件中
        c = pd.DataFrame(x)

        timestamp = time.localtime()
        currentTime = time.strftime('%Y-%m-%d %X', timestamp)
        fileName = time.strftime('%Y-%m-%d %H-%M-%S', timestamp) +'.csv'
        path = 'D://交通态势信息//'
        if not os.path.exists(path):
            os.mkdir(path)
        dir = path + fileName
        c.to_csv(dir, encoding='utf-8-sig', header=0)

        hint = '当前时间是: ' + currentTime + ', 已爬取交通态势信息, 存储的交通态势信息的文件路径是：' + dir
        print(hint)

        if not self.app.stopFlag:
            self.app.log.set(hint)
            global timer
            timer = threading.Timer(int(self.frenquency), self.fectchTraffic)
            timer.start()
        return
#
# #main函数
# if __name__=="__main__":
#     # while True:
#     #     fectchTraffic(time.localtime())  # 此处为要执行的任务
#     #     time.sleep(60)
#     timer = threading.Timer(1.0, fectchTraffic, [time.localtime()])
#     timer.start()

