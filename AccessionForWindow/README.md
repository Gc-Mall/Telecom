# Accession For Windows

> 此为windows优化版，为方便pyinstaller打包为可执行exe程序在windows下运行进行了优化
> 

## 文件说明

[accession.py](https://github.com/Gc-Mall/Telecom/blob/main/AccessionForWindow/accession.py)校园电信网登录

[set_proxy.py](https://github.com/Gc-Mall/Telecom/blob/main/AccessionForWindow/set_proxy.py)修改windows代理

[telecom_account.py](https://github.com/Gc-Mall/Telecom/blob/main/AccessionForWindow/telecom_account.py)储存的账户信息

## 优化详情

- 将账户信息封装到telecom_account.py中，从而避免pyinstaller打包accession.py为exe程序后，需要将账户信息以文件形式保存在同目录下进行调用的情况，增加了实际使用过程中出错的概率
- 为解决在打开如clash等代理软件时无法访问登陆界面的问题，通过调用set_proxy.py修改注册表来修改windows的代理配置，实现程序正常运行

## 使用须知

- pyinstaller打包生成exe程序：切换至AccessionForWindows目录，运行以下命令（-F选项为将全部资源、依赖直接打包为exe）

```bash
pyinstaller -F accession.py
```
