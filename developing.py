from urllib.parse import urlparse
import requests
import json
import os

class Telecom():
    def __init__(self) -> None:
        #获取登录信息(ip,mac,loction...)
        check_url = 'http://123.123.123.123/'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        check_headers= {
            "Host":"123.123.123.123",
            "User-Agent": agent,
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            }
        r0 =requests.get(check_url,headers=check_headers,allow_redirects=False)
        #self.url保存登录信息
        self.url = r0.headers['Location']
    
    def logout(self, userIndex) -> str:
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

Task_test = Telecom()
print(Task_test.url)