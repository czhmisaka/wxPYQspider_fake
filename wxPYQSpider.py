
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


# 

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
    time.sleep(3)
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
            print('重开')
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
        for x in range(20):
            swipe_down('','',1000)
            kick(1)
        for x in range(21):
            swipe_up2()
            kick(0.5)
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
            kick()
            name = str(y)+'_'
            try:
                contextObj = driver.find_element_by_class_name('android.widget.TextView')
                name = contextObj.text.replace('\n', '').replace('\r', '').strip()
                name = name.replace('\\','')
                name = name.replace('/',' ')
                kick()
                timeObj = driver.find_element_by_id('android:id/text1')
                timesss = timeObj.text
                timesss = timesss.replace(':','').strip()
                print(timesss)
            except:
                print('context fail')
            mkdirFile(namePath+'/'+timesss+name)    
            maxNum = SaveScreenShot(namePath+'/'+timesss+name)
            if maxNum == 'max':
                break
            tap(X(50),Y(50),800)
            kick()
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
        


