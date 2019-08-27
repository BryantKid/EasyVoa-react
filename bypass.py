from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import threading
import os
import shutil
import requests
from lxml import etree
import json
import random

brbppath = os.path.expanduser('~') + '/BRBP'
userspath = brbppath + '/USERS'
user0path = userspath + "/USER0/Chrome"

def crawler():
    atc_list = atc()  # {'':{},'':{}}
    shoe_key = list(atc_list.keys())  # ['','']
    while True:
        try:
            x = int(input("\n请选择选择鞋款："))
            while x < 1 or x > len(shoe_key):
                x = int(input("输入有误选择鞋款："))
            break
        except:
            pass
    x = x - 1
    shoe = shoe_key[x]
    atc_list[shoe]
    if len(list(atc_list[shoe].keys())) == 0:
        print("\n\n此鞋码暂无库存！")
        chose()
    else:
        while True:
            try:
                size = input("选择尺码：")
                atc_list[shoe][size]
                break
            except:
                print("输入错误请重新输入！")
                pass
            print(atc_list[shoe][size])
            browser(open_chromd, {'url': atc_list[shoe][size]})    #request 爬

def filter(path):
    pathlist = []
    for i in os.listdir(path):
        if i != "USER0" and i != ".DS_Store":
            try:
                int(i)
                if os.listdir(userspath+'/'+i) == []:
                    shutil.rmtree(userspath+'/'+i)
            except:
                pass
            pathlist.append(i)
    return pathlist

def batch():
    if filter(userspath) == []:
        print("\n\n请先创建pypass！")
        return chose()
    else:
        for index, item in enumerate(filter(userspath)):
            for v in filter(userspath + '/' + item):
                if not os.path.exists(userspath + '/' + item + '/' + v + '/Chrome/Default/yeezycookies'):
                    shutil.rmtree(userspath + '/' + item + '/' + v)
            print("第" + item + "批" , len(filter(userspath + '/' + item)) , '个')
        up = []
        i = input('选择第几批：(默认全部)\n')
        if i == "":
            return filter(userspath)
        else:
            while True:
                if i in filter(userspath):
                    up.append(i)
                    break
                else:
                    i = input('输入错误请重新输入，打开第几批：')
            return up

def savecookies(driver, cookiespath):
    cookies = driver.get_cookies()
    yeezycookies = ''
    for x in cookies:
        yeezycookies = yeezycookies + x['name'] + '=' + x['value'] + '; '
    yeezycookies = yeezycookies.rstrip('; ')
    with open(cookiespath + '/yeezycookies', 'w') as w:
        w.write(yeezycookies)

def yeezy_request(data):
    if 'cookies' in data:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            "cookie": data['cookies'],
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        if data['status'] == 'add':
            print(data['ij'] + '成功加车商品：' + json.loads(requests.post(url=data['url'], headers=headers, json=data['json']).text)["title"])
        if data['status'] == 'clear':
            requests.get(url=data['url'], headers=headers)
            print('clear done!')
        if data['status'] == 'cart':
            items = json.loads(requests.get(url=data['url'], headers=headers).text)['items']
            if items != []:
                for c in items:
                    print(data['ij'] + c['title'])
            else:
                print(data['ij'] + '购物车为空')
        if data['status'] == 'check':
            if json.loads(requests.get(url=data['url'], headers=headers).text)['token'] == json.loads(requests.get(url=data['url'], headers=headers).text)['token']:
                print(data['ij'] + '未过期')
    else:
        print(data['ij']+'无效bp')

def atc():
    url = 'https://yeezysupply.com'
    res = requests.get(url)
    idtest = etree.HTML(res.text).xpath('//script[@class="js-product-json"]/text()')
    dict_act = {}
    for idx,i in enumerate(idtest):
        atc = {}
        print("\n",idx+1  ,json.loads(i)["handle"],'可选尺码为：', end=" - ")
        for index, j in enumerate(json.loads(i)["variants"]):
            if str(j["id"]) != '161803398875' and j["available"] != False:
                print(j["option1"], end=" - ")
                atc_url = "https://yeezysupply.com/cart/" + str(j["id"]) + ":1"
                atc[j["option1"]] = atc_url
        dict_act[json.loads(i)["handle"]] = atc
    return dict_act

def fe(xp, driver):
    i = 0
    while True:
        i = i+1
        try:
            ebx = driver.find_element_by_xpath(xp)
            return ebx
        except:
            pass

def bypass(data):
    os.system('rm -f ' + user0path + '/Default/Cookies')
    if not os.path.exists(data['chromepath']):
        shutil.copytree(user0path, data['chromepath'])
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument("headless")
    option.add_argument("--user-data-dir=" + data['chromepath'])
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=option)
    if data['status'] == 'mrk':
        driver.quit()
        print(data['ij'])
        return 1
    driver.set_page_load_timeout(120)
    try:
        driver.get(data['randomurl'])
        print(data['ij'] + "正在加载页面")
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="SIZE"]/option[2]')
                break
            except:
                # print('...')
                pass
        opts = ['last()','2']
        driver.find_element_by_xpath('//*[@id="SIZE"]/option[' + random.choice(opts) + ']').click()
        driver.find_element_by_xpath('//input[@value="PURCHASE"]').send_keys(Keys.ENTER)
        while driver.find_element_by_xpath('//span[contains(@class,"H__cart_count")]').text == "":
            pass
        while True:
            try:
                driver.find_element_by_xpath('//input[@name="checkout"]').click()
                break
            except:
                # print('...')
                pass
        while True:
            if 'queue?' in driver.current_url:
                pass
            else:
                break
        if 'checkouts' in driver.current_url:
            current_url = driver.current_url
            # driver.get("https://yeezysupply.com/cart/clear")
            savecookies(driver, data['default'])
            driver.quit()
            with open(data['default'] + '/bpurl', 'w') as w:
                w.write(current_url)
            print(data['ij'] + "bypass制作成功")
        else:
            driver.quit()
            print(data['ij'] + "页面加载差超时！请切换网络尝试。")
    except TimeoutException:
        driver.quit()
        print(data['ij'] + "页面加载差超时！请切换网络尝试。")

def open_chromd(data):
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    with open(data['default'] + '/bpurl', 'r') as r:
        current_url = r.read()
    option.add_argument("--user-data-dir=" + data['chromepath'])
    driver = webdriver.Chrome(chrome_options=option)
    if 'url' in data:
        url = data['url']
    else:
        url = current_url
    if data['status'] == 'checkout':
        driver.get(current_url)
    else:
        driver.get('chrome://bookmarks/')
        title = 'bypass'
        if 'ga' in current_url:
            title = 'ga_bypass'
        if 'ctd' in current_url:
            title = 'ctd_bypass'
        driver.execute_script(
            "chrome.bookmarks.create({parentId: '1',title: '" + title + "',url: '" + current_url + "'});")
        driver.get(url)




def browser(ft, data={'status': ''}):
    threads = []
    pathlist = []
    if data['status'] == 'make' or data['status'] == 'mrk':

        num = input("请输入数量：(默认5个)")
        if num == "":
            num = 5
        num = int(num)
        if num > 10:
            num = 10
        a = 1
        mpath = userspath + '/' + str(a)
        while os.path.exists(mpath):
            a = a + 1
            mpath = userspath + '/' + str(a)
        for b in range(num):
            c = '/user' + str(b+1)
            pathlist.append(mpath + c)
        collections_url = []
        print('正在爬取可用商品url如果加载超时可以手动关闭')
        url = 'https://yeezysupply.com/collections/new-arrivals'
        res = requests.get(url)
        idtest = etree.HTML(res.text).xpath('//*[@id="js-new-arrivals-json"]/text()')
        for i in idtest:
            for j in json.loads(i)['products']:
                if j['available'] == True:
                    jurl = 'https://yeezysupply.com' + j['url'] + '?c=%2Fcollections%2Fnew-arrivals'
                    print(jurl)
                    collections_url.append(jurl)
    else:
        for d in batch():
            for e in filter(userspath + "/" + str(d)):
                pathlist.append(userspath + "/" + str(d) + '/' + e)
    for p in pathlist:
        data[p] = {}
        if data['status'] == 'make' or data['status'] == 'mrk':
            data[p]['randomurl'] = random.choice(collections_url)
        data[p]['cpath'] = p
        data[p]['chromepath'] = p + '/Chrome'
        data[p]['default'] = p + '/Chrome/Default'
        if os.path.exists(data[p]['default'] + '/yeezycookies'):
            with open(data[p]['default'] + '/yeezycookies', 'r') as r:
                data[p]['cookies'] = r.read()
        data[p]['ij'] = '第' + p.split('/')[-2] + '批' + p.split('/')[-1] + ': '
        if 'url' in data:
            data[p]['url'] = data['url']
        if 'status' in data:
            data[p]['status'] = data['status']
        if 'json' in data:
            data[p]['json'] = data['json']
        t = threading.Thread(target=ft, args=(data[p],))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def changeinfo():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument("--user-data-dir=" + userspath + '/USER0/Chrome')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    try:
        driver = webdriver.Chrome(chrome_options=option)
        driver.get("chrome://settings")
        return chose(driver=driver)
    except:
        print('\n\n缺少chromedriver\n请下好与浏览器对应版本的chromedriver详情参考：https://blog.csdn.net/BinGISer/article/details/88559532\n并将chromedriver放进' + '/usr/local/bin' + '目录下')
        import time
        time.sleep(1000)


def bookmark():
    with open(userspath + '/USER0/Chrome/Default/Preferences', 'r') as r:
        lines = r.read()
        if '"bookmark_bar":{"show_on_all_tabs":true}' in lines:
            pass
        elif '"bookmark_bar":{"show_on_all_tabs":false}' in lines:
            lines = lines.replace('"bookmark_bar":{"show_on_all_tabs":false}',
                                  '"bookmark_bar":{"show_on_all_tabs":true}')
            with open(userspath + '/USER0/Chrome/Default/Preferences', 'w') as w:
                w.write(lines)
        else:
            lines = lines.replace('{"account_id_migration_state"',
                                  '{"bookmark_bar":{"show_on_all_tabs":true},"account_id_migration_state"')
            with open(userspath + '/USER0/Chrome/Default/Preferences', 'w') as w:
                w.write(lines)

def chose(driver=""):
    selection_number = input('\n\n1:制作Bypass\n2:清除购物车并打开制作好Bypass的浏览器\n3:删除所有Cookie\n4:打开浏览器更新信息\n5:初始化\n6:爬取atc加车\n7:检查bypass是否过期\n8:打开浏览器更新bypass\n9:加车\n10:清除购物车\n11:查看购物车\n12:打开浏览器结算\n输入其他退出\n请输入:')
    if driver != "":
        driver.quit()
    bookmark()
    if selection_number == '1':
        browser(bypass, {'url': 'https://yeezysupply.com/', 'status': 'make'})   #selenium
        chose()
    elif selection_number == '2':
        browser(open_chromd, {'url':'https://yeezysupply.com/cart/clear', 'status': ''})
        chose()
        #selenium
    elif selection_number == "3":
        while True:
            try:
                for i in filter(userspath):
                    if os.path.exists(userspath + '/' + i):
                        shutil.rmtree(userspath + "/" + i)
                    else:
                        pass
                if os.path.exists(brbppath + "/data"):
                    shutil.rmtree(brbppath + "/data")
                else:
                    pass
                break
            except:
                pass
        chose()
    elif selection_number == "4":
        changeinfo()    #更新
    elif selection_number == "5":
        shutil.rmtree(userspath)   #初始化
        changeinfo()
    elif selection_number == "6":
        crawler()   #爬atc
    elif selection_number == '7':
        browser(yeezy_request,{'url': 'https://yeezysupply.com/cart.json', 'status': 'check'})
        chose()
    elif selection_number == '8':
        browser(bypass)
        chose()
    elif selection_number == '9':
        shoeid = input("请输入V码:")
        browser(yeezy_request, {'url': 'https://yeezysupply.com/cart/add.js', 'json': {"id": shoeid, "quantity": 1}, 'status': 'add'}) #request
        chose()
    elif selection_number == '10':
        browser(yeezy_request, {'url': 'https://yeezysupply.com/cart/clear', 'status': 'clear'})  #request
        chose()
    elif selection_number == '11':
        browser(yeezy_request,{'url': 'https://yeezysupply.com/cart.json', 'status': 'cart'})
        chose()
    elif selection_number == '12':
        browser(open_chromd,{'status': 'checkout'})
        chose()#selenium
    else:
        print("已退出")
        return 1

cmd = "/usr/sbin/system_profiler SPHardwareDataType | fgrep 'Serial' | awk '{print $NF}'"
output = os.popen(cmd).read()

def mianf():

    keyjson = json.loads(requests.get('http://tdleon.com/br/api/bypass.json').text)
    if key in keyjson:
        if keyjson[key]+'\n' == output:
            print('\n\n欢迎使用bp测试脚本，本脚本完全免费，版权归Brick Republic所有，\n请勿用作商业用途，违者必究！\n请关注微信公众号：Brick Republic，你的中文抢购群组！')
            if os.path.exists(userspath + '/USER0'):
                chose()
            else:
                changeinfo()
        else:
            print("激活码有误请联系管理员")
            os.system('rm -rf ' + brbppath + '/key')
    else:
        print("激活码有误请联系管理员")
        os.system('rm -rf ' + brbppath + '/key')




if os.path.exists(brbppath + '/key'):
    with open(brbppath + '/key', 'r') as r:
        key = r.read()
    mianf()
else:
    if not os.path.exists(brbppath):
        os.system('mkdir -p ' + brbppath)
    inum = input("\n\n请将微店购买的激活码和 " + output + '\n发送给dc脚本频道管理员再进行下一步要进入下一步请输入1+回车键 任意键+回车退出:')
    if inum == '1':
        key = input("请输入激活码：")
        with open(brbppath + '/key', 'w') as w:
            w.write(key)
        mianf()
    else:
        print('已退出')