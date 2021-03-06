
@[TOC](czh的开发笔记 - 微信朋友圈 - 模拟操作)

# 这个爬虫效率极其低下，仅供学习参考使用

## 朋友圈爬虫简介
模拟人工操作爬取朋友圈数据

## 防喷
1. 这个代码写的确实很烂，我暂时也没有优化的动力

## 个人要求
1. 需要会配置path
2. 需要一定的python基础
3. 需要有一定的前端调试经验
4. 然后要有点耐心，这个环境配置确实需要一点时间，我这里也仅提供了win10+安卓的环境配置经验。
## 环境配置（准备）
1. node+appium+adb 可以在下面的链接中下载 
   1. **node** <https://nodejs.org/zh-cn/>
   2. **adb** <https://www.androiddevtools.cn/> **这个是国内的安卓下载站，记得要找清楚是adb**
   3. **sdk Manager** <http://114.116.234.77:1234/android-sdk_r24.4.1-windows.zip> **这个是放在我的服务器上的,你也可以自己找**
   4. **appium** <http://appium.io/> **这个直接去官网上下载就好**
2. python环境 建议直接使用Anaconda <https://www.anaconda.com/>
3. 编辑器啥的自己搞定(**vsCode强烈安利**)

## 环境配置（安装）
1. 安装node(双击安装包即可)
   1. 安装结束后记得修改源(如下)
```
npm config set registry https://registry.npm.taobao.org
```
2. 安装appium和adb
   1. 安装完成后记得配置path,添加一条指向adb文件夹内的路径
3. 安装sdkManager(双击安装即可)
4. python环境(**我的源码用的是python3,记得注意版本**)

## 工作原理
原理很简单，如下
```mermaid
	graph LR
	A(python脚本) --通过端口发送--> B(appium) --转译指令--> C(真机)
```

## 源码自提
<https://github.com/czhmisaka/wxPYQspider_fake>

## 源码展示与讲解
1. 在桌面准备一个 nameList.txt(如下)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021012215015630.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L20wXzM4MTE5MjM5,size_16,color_FFFFFF,t_70)
2. 用usb线（需要稳定性较好，最好是type-C的全功能线）链接手机
   1. 手机需要打开开发者模式以及usb调试
3. 在终端中输入abd devices 检查设备是否链接成功
4. 运行python脚本
   1. 此时被操作手机中会出现一个新的应用(Appium setting),**需要给这个应用最高权限,以及避免被系统自动关闭(内存优化,后台搞耗电,自启动管理等设置需要调整)**
5. 重新运行脚本

```python

from appium import webdriver
import time
import re
import sys
import os
from appium.webdriver.common.touch_action import TouchAction
import json 
import numpy as np
import pathlib
import sys
from cv2 import cv2 as cv

driver = {}

def imgFormat(path):
    
    return True

def cv_imread(filePath):
    cv_img=cv.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

def change(path):
    path_str = path
    alpha = 0.02
    img = cv_imread(str(path))
    if img is None: 
        return 
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) / 255
    h_mid = img_gray.shape[0] // 2
    w_mid = img_gray.shape[1] // 2
    u = h_mid
    while u >= 0 and np.mean(img_gray[u]) > alpha: u -= 1
    b = h_mid
    while b < img_gray.shape[0] and np.mean(img_gray[b]) > alpha: b += 1
    l = w_mid
    while l >= 0 and np.mean(img_gray[:, l]) > alpha : l -= 1
    r = w_mid
    while r < img_gray.shape[1] and np.mean(img_gray[:, r]) > alpha: r += 1
    try:
        asd = 'a_'
        pathList = path.split('/')
        pathName = ''
        for x in range(len(pathList)):
            if x==0:
                pathName = pathList[x]
            elif x!=len(pathList):
                pathName = pathName+'/'+pathList[x]
            else:
                pathName = pathName+'/'+ 'a_'+pathList[x] + '.png'
        print(pathName)
        cv.imencode('.png', img[u + 1:b - 1, l + 1:r - 1])[1].tofile(f'{pathName}')
    except:
        print('e')



# 获取桌面路径
def getDesktopPath():
    return os.path.join(os.path.expanduser('~'),"Desktop")+'/'

# 创建文件夹
def mkdirFile(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return 'createFail'
    except:
        return 'existsFail'
    
# 创建json文件
def writeJson(path,data):
    with open(path+'/1.json','w') as fileObj:
        json.dump(data,fileObj)
        
    
def writeJson2(path,data):
    with open(path,'w') as fileObj:
        json.dump(data,fileObj)

# 截屏并保存
def SaveScreenShot(path,name=''):
    try:
        if name == '':
            for x in range(10):
                testPath = path+'/'+str(x)+'.png'
                print(testPath)
                if checkFile(testPath):
                    driver.get_screenshot_as_file(testPath)
                    change(testPath)
                    return x
            return "max"
        else:
            for x in range(10):
                testPath = path+'/'+str(name)+str(x)+'.png'
                if checkFile(testPath):
                    driver.get_screenshot_as_file(testPath)
                    change(testPath)
                    return x
            return "max"
    except:
        print('FUCK!!!!!!!!!!!!!!')

# 检查文件存在
def checkFile(path):
    if os.path.exists(path):
        return False
    else:
        return True

# 列表展示
def printList(lists):
    for x in lists:
        print(x)

#进入昵称为name的好友的朋友圈的点击逻辑
def enter_pengyouquan(name):
    driver.find_element_by_id('com.tencent.mm:id/f8y').click()  #点击搜索图标
    # driver.find_element_by_id('com.tencent.mm:id/cn_').click()
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(name)  #输入搜索文字
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/tm').click()  #点击第一个搜索结果
    time.sleep(1)
    driver.find_element_by_id('com.tencent.mm:id/cj').click()  #点击聊天界面右上角三个小点
    time.sleep(1)
    driver.find_element_by_id('com.tencent.mm:id/f3y').click() #点击头像
    time.sleep(1)
    driver.find_element_by_id('com.tencent.mm:id/coy').click() #点击朋友圈
    time.sleep(1)
    
#上拉方法
def swipe_up(distance, time):  #distance为滑动距离，time为滑动时间
    width = 1080
    height = 2150  # width和height根据不同手机而定
    driver.swipe(1 / 2 * width, 9 / 10 * height, 1 / 2 * width, (9 / 10 - distance) * height, time)

#获取当前朋友圈界面的文字
def get_onepage():
    eleLst = get_onepage_elementlist()
    pagetext = []
    for e in eleLst:
        try:
            pagetext.append(e.get_attribute('text'))
        except:
            pass
    return pagetext

#获取当前朋友圈界面的相关元素
def get_onepage_elementlist():
    # pict_list = driver.find_element_by_id('com.tencent.mm:id/cpu')
    pict_list = driver.find_elements_by_id('com.tencent.mm:id/fnn')  #带图朋友圈配文和视频朋友圈配文
    link_list = driver.find_elements_by_id('com.tencent.mm:id/kt')  #链接朋友圈配文和纯文字朋友圈
    elementlist = pict_list
    pic_list = driver.find_elements_by_xpath('//android.view.View[@content-desc="图片"]')
    printList(pic_list)
    return elementlist

#获取往前倒推year_count年到现在的所有朋友圈
def get_pages(year_count):
    pagestext = []
    # current_year = driver.find_element_by_id("com.tencent.mm:id/ekg").get_attribute("text") #获得当前年份
    while True:
        try:
            end_year = str(int(current_year[0:4]) - year_count) + "年"
            y = driver.find_element_by_id("com.tencent.mm:id/ekg").get_attribute("text")   #在页面中寻找显示年份的元素，没找到就会报错，继续上拉
            if y == end_year:   #到达结束年份
                break
            else:  #未到达结束年份，继续上拉
                pagetext=get_onepage()
                for t in pagetext:
                    if t not in pagestext:
                        pagestext.append(t)
                swipe_up(1 / 2, 2000)

        except:
            pagetext = get_onepage()
            for t in pagetext:
                if t not in pagestext:
                    pagestext.append(t)
            swipe_up(1 / 2, 2000)


    pagetext = get_onepage()
    for t in pagetext:
        if t not in pagestext:
            pagestext.append(t)
    while True:
        try:
            driver.find_element_by_id("com.tencent.mm:id/ekg")
            swipe_up(1/12,500)
        except:
            break
    #删除最后一页多获取的朋友圈文本
    lastPage=get_onepage()
    for t in lastPage:
        if t in pagestext:
            pagestext.remove(t)
    return pagestext

def store_PYQText(PYQ_list,store_path):  #将朋友圈文本存储到指定路径
    f = open(store_path, 'w', encoding='utf-8')
    for text in PYQ_list:
        f.write(text + '\n\n')
    f.close()

#去除表情文本
def remove_icondesc(list, storepath):
    f = open(storepath, 'w', encoding='utf-8')
    patten = re.compile('\w+(?![\u4e00-\u9fa5]*])')  #匹配除表情文本外的所有文本
    for s in list:
        splitted_sentences = re.findall(patten, s)
        for p in splitted_sentences:
            f.write(p + '\n')
    f.close()

def enter_pengyouquan_all():
    driver.find_element_by_id('com.tencent.mm:id/cnh').click()  #点击搜索图标
    time.sleep(2)

def tap(x,y,times=100):
    driver.tap([(x,y)],times)
    
def getScreenSize():
    size = driver.get_window_size()
    return size

def X(x):
    return x/100*size['width']

def Y(y):
    return y/100*size['height']

class Point:
    pass      
def swipe_down(fromP={},toP={},times=3000):
    if fromP:
        if toP:
            return driver.swipe(fromP.x, fromP.y, toP.x,toP.y,times)
    return driver.swipe(X(70),Y(80),X(30),Y(20),times)

def swipe_up2():
    return driver.swipe(X(70),Y(20),X(30),Y(80),1000)

def swipe_r2l():
    return driver.swipe(X(90),Y(50),X(10),Y(50),400)

def toPYQ():
    tap(676,2162)
    time.sleep(3)
    tap(454,296)
    time.sleep(3)    

def kick(times=0.5):
    time.sleep(times)

def main_saveByName(nameList):
    size = {'width':1,'height':1}
    deviceConfig = {
        'platformName':'Android'
    }

size = {'width':1,'height':1}
desired_caps = {
    'platformName': 'Android',
    'deviceName': '37KNW18710001152',
    'platformVersion': '9',
    'appPackage': 'com.tencent.mm',  # apk包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI',  # apk的launcherActivity
    'noReset': 'True',  # 每次运行脚本不用重复输入密码启动微信
    'unicodeKeyboard': 'True',  # 使用unicodeKeyboard的编码方式来发送字符串
    'resetKeyboard': 'True'  # 将键盘给隐藏起来
}

asd = {
    "platformName": "Android",
    "platformVersion": "10",
    "deviceName": "HA19RRAZ",
    "appPackage": "com.tencent.mm",
    "appActivity": "com.tencent.mm.ui.LauncherUI",
    "noReset": "true",
    "automationName":"uiautomator2"
}
driver = {}
pyq = {}

nameList = []
fr = open(getDesktopPath()+'nameList.txt', encoding='utf-8',errors='ignore')
nameList = fr.read().split('\n')
num = 0

# 防止文件夹名称重复
preName = '' 
preNum = 0
# 防止文件夹名称重复

for xx in nameList:
    try:
        if xx == "":
            continue
        x = str(xx)
        list = []
        print(nameList,x,'次数',str(num))
        try:
            driver.quit()
        except:
            print('开始')
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', asd)
        size = getScreenSize()
        kick(5)
        enter_pengyouquan(x) 
        kick(5)
        # toPYQ()
        
        timeNow = time.strftime("%Y-%m-%d", time.localtime())
        namePath = getDesktopPath()+'\\test\\'+str(x)+str(timeNow)
        mkdirFile(namePath)
        for x in range(10):
            swipe_down('','',1000)
            kick(1)
        for x in range(11):
            swipe_up2()
            kick(1)
        try:
            comeIn = driver.find_element_by_id('com.tencent.mm:id/cpu')
            comeIn.click()
            kick()
        except:
            try:
                comeIn = driver.find_element_by_id('com.tencent.mm:id/cpu')
                comeIn.click()
                kick()
            except:
                print('clickFail')
        # try:
        #     leak = driver.find_element_by_id('com.tencent.mm:id/g95')
        #     leak.click()
        #     kick()   
        # except:
        #     try:
        #         leak = driver.find_element_by_id('com.tencent.mm:id/g95')
        #         leak.click()
        #         kick()   
        #     except:
        #         print('fuck2')
        for y in range(10000):
            tap(X(50),Y(50),800)
            time.sleep(1)
            try:
                save = driver.find_elements_by_id('com.tencent.mm:id/gam')
            except:
                print('保存失败')
            else:
                for c in save:
                    if c.text == '保存图片' or c.text == '保存视频':
                        num = num + 1
                        print('当前轮数:'+str(y)+'    已保存图片数量:'+str(num))
                        c.click()
                        kick()
                        break
                kick()
            kick(2)
            name = str(y)+'_'
            try:
                contextObj = driver.find_element_by_class_name('android.widget.TextView')
                name = contextObj.text.replace('\n', '').replace('\r', '').strip()
                name = name.replace('\\','')
                timeObj = driver.find_element_by_id('android:id/text1')
                timesss = timeObj.text
                timesss = timesss.replace(':','').strip()
                print(timesss)
            except:
                print('context fail')
            if name in list:
                preName
            mkdirFile(namePath+'/'+timesss+name)    
            kick()
            maxNum = SaveScreenShot(namePath+'/'+timesss+name)
            if maxNum == 'max':
                break
            kick()
            try:
                swipe_r2l()
            except:
                kick()
                try:
                    swipe_r2l()
                except:
                    print('fail')
    except:
        nameList.append(xx)
        



```

## 后记
这个博文其实也没有讲的很细,之后再补充
