import ctypes
from winreg import OpenKey, QueryValueEx, SetValueEx
from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS

class Proxy():
    def __init__(self) -> None:
        #读取INTERNET_SETTINGS信息
        self.INTERNET_SETTINGS = OpenKey(HKEY_CURRENT_USER, 
                                   r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                   0, KEY_ALL_ACCESS)
        self.PROXIES = {
            'off' : {
                'enable': 0,
                'override': u'-',
                'server': u'-'
                },
            'clash' : {
                'enable': 1,
                #123.123.123.123为accession.py中requests.get的地址
                #最后添加<local>实现本地地址不使用代理
                'override': u'localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*;127.0.0.1;123.123.123.123;<local>',
                'server': u'127.0.0.1:7890'
                }
            }

    def set_key(self, name, value):
        SetValueEx(self.INTERNET_SETTINGS, name, 0, 
                   QueryValueEx(self.INTERNET_SETTINGS, name)[1], value)
    
    def set_proxy(self):
        #直接在替换代理名单，不管原本代理设置
        self.set_key('ProxyOverride', self.PROXIES['clash']['override'])
        """
        #默认代理关闭
        if is_proxyon == False:
            proxy = 'off'
        else:
            proxy = 'clash'
        self.set_key('ProxyEnable', self.PROXIES[proxy]['enable'])
        self.set_key('ProxyOverride', self.PROXIES[proxy]['override'])
        self.set_key('ProxyServer', self.PROXIES[proxy]['server'])
        """
        # granting the system refresh for settings take effect
        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, 37, 0, 0)  # refresh
        internet_set_option(0, 39, 0, 0)  # settings changed