from urllib.parse import urlparse
import requests
import json
import os
#将账户数据保存在函数中，来避免pyinstaller打包时文件依赖问题
from telecom_account import telecom_account 

class Telecom():
    def __init__(self) -> None:
        """获取登录界面所需信息"""
        ###针对已登录情况进行了优化
        check_url = 'http://123.123.123.123/'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        check_headers= {
            "Host":"123.123.123.123",
            "User-Agent": agent,
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            }
        #采用try和except应对响应异常情况
        try:
            r0 =requests.get(check_url,headers=check_headers,allow_redirects=False,timeout=8)
            #self.url保存登录信息
            self.url = r0.headers['Location']
        except requests.exceptions.RequestException:
            #已登录情况，若存在之前登录信息，进行登出操作，若不存在，则报错，提醒用户手动断开网络
            if os.path.exists('login_info.txt'):
                file = open('login_info.txt')
                login_info = json.loads(file.read())
                for value in login_info.values():
                    self.logout(value)
                file.close()
                self.__init__()
            else:
                print('接入网络失败，请手动断开网络后重试！')
                os.system("PAUSE")
                exit()
    
    def logout(self, userIndex) -> str:
        """
        param: userIndex账户对于的用以登出的参数
        """
        logout_url = 'http://172.25.249.8/eportal/InterFace.do?method=logout'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        logout_headers= {
            "Host":"172.25.249.8",
            "Origin" : "http://172.25.249.8",
            "Referer" : "http://172.25.249.8/eportal/success.jsp?" + userIndex + "&keepaliveInterval=0",
            "User-Agent": agent,
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
            }
        logout_postdata = "userIndex=" + userIndex + "&keepaliveInterval=0"
        r1 =requests.post(logout_url,data=logout_postdata,headers=logout_headers)
        r1.encoding='utf-8'
        return r1.text

    def login(self, account, is_logout=False) -> str:
        """
        param: account登录账户
        param: is_logout用以控制是否在登陆后执行登出操作, 默认为否
        """
        login_url = 'http://172.25.249.8/eportal/InterFace.do?method=login'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        login_headers= {
            "Host":"172.25.249.8",
            "Origin" : "http://172.25.249.8",
            #"Referer" : "http://172.25.249.8/eportal/index.jsp?userip=100.66.80.46&wlanacname=&nasip=171.88.130.251&wlanparameter=9c-eb-e8-e4-c8-79&url=http://123.123.123.123/&userlocation=ethtrunk/3:361.16",
            "Referer" : self.url,
            "User-Agent": agent,
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
            }
        #urlparse解析登录网址
        login_postdata = 'userId=' + account + '&password=12345678&service=&queryString=' + urlparse(self.url).query
        r2 =requests.post(login_url,data=login_postdata,headers=login_headers)
        r2.encoding='utf-8'
        result = r2.json()
        if result['result'] == 'success':
            if is_logout == True:
                self.logout(result['userIndex'])
            return result['userIndex']
        else:
            return None
"""
#此处采用文件绝对路径是为方便打包成exe文件，自己调试时可以调用os.path.abspath(".")
os.path.abspath(".")
file = open('telecom_account.txt')
account = json.loads(file.read())
file.close()
"""
#通过调用函数方式导入数据
account = telecom_account()
Task_acce = Telecom()
for key in account.keys():
    return_value = Task_acce.login(key, is_logout=False)
    if return_value is not None:
        login_info = {key : account[key]}
        #转化为json文件进行保存成功登录的账户信息，以便下次启动时调用
        current_path = os.path.abspath(".")
        file = open('login_info.txt', "w")
        file.write(json.dumps(login_info))
        file.close()
        break
if return_value is not None:
    print("成功接入网络！")
else:
    print("接入网络失败，请稍后重试! ")
os.system("PAUSE")