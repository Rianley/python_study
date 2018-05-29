# Author:rianley cheng
'''
┏┓      ┏┓

┏┛┻━━━┛┻┓

┃      ☃      ┃

┃  ┳┛  ┗┳  ┃

┃      ┻      ┃

┗━┓      ┏━┛

┃      ┗━━━┓

┃  神兽保佑    ┣┓

┃　永无BUG！   ┏┛

┗┓┓┏━┳┓┏┛

┃┫┫  ┃┫┫

┗┻┛  ┗┻┛
'''
"""
ATM/
|-- bin/
|   |-- index.py         程序运行主体程序
|   |-- run.py           程序执行程序（入口文件）
|-- conf/
|   |-- settings.py      程序配置(加载公共部分调用)
|-- material             程序资源放置(公共素材存放处)
    |-- ...
|-- core/                程序主体模块存放
|   |-- __init__.py      包
|   |-- atm.py           银行卡中心模块
|   |-- cart.py          购物车中心模块
|-- ATM.png              项目一览图
|-- README.md            项目介绍 以及使用规范
|-- about.md             作者介绍            
"""
import sys,os,time
path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)

from bin import index

if __name__ =='__mian__':
    index.index()

