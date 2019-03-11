import requests
import pandas as pd
import time
import threading

def httpGet():
    # 初始API的URL
    url = "https://restapi.amap.com/v3/traffic/status/rectangle?key=51e09b8a50bc85f3bbc85a40822d3abf&extensions=all&rectangle="

    # 设定整个网格左下角坐标的经纬度值
    baselng = 113.00
    baselat = 28.12
    # 设定每个网格单元的经纬度宽
    widthlng = 0.05
    widthlat = 0.04
    # 用于储存数据
    x = []
    # 用于标识交通态势线段
    num = 0

    try:
        # 循环每个网格进行数据爬取，在这里构建了4X4网格
        for i in range(0, 8):
            # 设定网格单元的左下与右上坐标的纬度值
            # 在这里对数据进行处理，使之保留6位小数（不保留可能会莫名其妙出错）
            startlat = round(baselat + i * widthlat, 6)
            endlat = round(startlat + widthlat, 6)
            for j in range(0, 8):
                # 设定网格单元的左下与右上坐标的经度值
                startlng = round(baselng + j * widthlng, 6)
                endlng = round(startlng + widthlng, 6)
                # 设置API的URL并进行输出测试
                locStr = str(startlng) + "," + str(startlat) + ";" + str(endlng) + "," + str(endlat)
                thisUrl = url + locStr
                print(thisUrl)
                # 爬取数据
                data = requests.get(thisUrl)
                s = data.json()
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
                # 若爬取网格较多，可使用time.sleep(秒数)来避免高德的单秒API调用次数的限制
    except Exception  as e:
        pass
    return x

# 抓取交通态势数据
def fectchTraffic(currentTime):

    cnt = 0
    x = []
    while cnt < 10:
        x = httpGet()
        if x:
            break
        cnt = cnt + 1

    # 将数据结构化存储至规定目录的CSV文件中
    c = pd.DataFrame(x)
    currentTime = time.strftime('%Y-%m-%d %X', time.localtime())
    fileName = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    dir = 'D://'+ fileName +'.csv'
    c.to_csv(dir, encoding='utf-8-sig', header=0)
    print('当前时间是: ' + currentTime + ', 已爬取交通态势信息, 存储的交通态势信息的文件路径是：' + dir)
    global timer
    timer = threading.Timer(600.0, fectchTraffic, [time.localtime()])
    timer.start()
    return

#main函数
if __name__=="__main__":
    # while True:
    #     fectchTraffic(time.localtime())  # 此处为要执行的任务
    #     time.sleep(60)
    timer = threading.Timer(1.0, fectchTraffic, [time.localtime()])
    timer.start()

