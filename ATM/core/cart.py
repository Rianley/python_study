# rianley cheng
import sys,os
from core.atm import atm
class cart:
    user=''#记录登录状态
    cart_all={}#购物车
    operation=[
        '注册',
        '登录',
        '购买商品',
        '查看购物车',
        '结算购物车',
        '申请银行卡',
        '退出登录'
    ]
    operate_func=[]
    def __init__(self):
        operate_func=[
            self.register,
            self.login,
            self.choose_goods,
            self.show_cart_list,
            self.payfor,
            self.apply_credit_cart,
            self.logout
        ]
        self.operate_func=operate_func
    def auth(func):
        def wrapper(self,*args, **kwargs):
            if not self.user:
                print('请先登录!!!!!!!')
                if self.login():return True
            return func( self,*args, **kwargs)
        return wrapper
    #注册
    def register(self):
        user_info=self.get_user_list()
        while True:
            name=input('请输入用户名：').strip()
            if not name:continue
            if name=='q':return  True
            # 注册时检测用户名是否唯一
            if name in user_info:
                print('用户名已存在！')
                continue
            break
        while True:
            pwd = input('请输入密码：').strip()
            if not pwd: continue
            if pwd == 'q':return True
            break
        self.append_user('%s,%s\n'%(name,pwd))
        print('用户%s注册成功'%name)
        print()
        return True
    def login(self):
        user_info = self.get_user_list()

        if self.user:
            print('不能重复登录!')
            return True
        while True:
            name=input('请输入用户名：').strip()
            if name=='q':return True
            if not name:continue
            break
        while True:
            pwd=input('请输入密码：').strip()
            if pwd=='q':return True
            if not pwd:continue
            break
        if name in user_info and user_info[name]==pwd:
            self.user=name
            print('登录成功!')
            print()
            return False
        print('用户名或密码错误')
        return True
    @auth
    def logout(self):
        self.user=''
        print('退出登录成功')
        return  True
    #购买商品
    @auth
    def choose_goods(self):
        goods_list=self.get_goods_list()
        print('商品列表如下：')
        print('编号','名称','单价')
        for i in goods_list:
            for j in goods_list[i]:
                print(j,end=' ')
            print()
        while True:
            input_goods =input('请选择商品（输入对应商品的编号即可,输q退出购买）：').strip()
            if input_goods=='q':return True
            if not input_goods:continue
            if input_goods not in goods_list:
                print('输入有误')
                continue
            break
        while True:
            num=input('请输入购买的商品（%s）的数量：'%goods_list[input_goods][1]).strip()
            if num == 'q': return True
            if not num: continue
            if not num.isdigit() and int(num)>0:
                print('输入错误')
                continue
            num=int(num)
            break

        if input_goods not in self.cart_all:
            cart_x={}
            cart_x['info']=goods_list[input_goods]
            cart_x['name']=goods_list[input_goods][1]
            cart_x['price'] = goods_list[input_goods][2]
            cart_x['num'] = num
            self.cart_all[input_goods]=cart_x
        else:
            self.cart_all[input_goods]['num']+=num
        print('添加购物车成功')
        self.show_cart_list()
        print('如需退出当前购买操作，请键入q!')
        return False

    @auth
    def show_cart_list(self):
        if not self.cart_all:
            print('购物车空空如已！请先去添加')
            return True
        print('当前购物车信息如下：')
        print('编号', '名称', '单价','数量','单一商品总价')
        all_price=0
        for i in self.cart_all:
            p = self.cart_all[i]['num'] * self.cart_all[i]['price']
            all_price+=p
            print(i,self.cart_all[i]['name'],self.cart_all[i]['price'],self.cart_all[i]['num'],p)
        print('购物车总价为：%s'%all_price)
        print()
        return True
    #结算购物车
    @auth
    def payfor(self):
        if not self.cart_all:
            print('购物车空空如已！请先去添加')
            return True
        all_price=0
        log_list=[]
        for i in self.cart_all:
            p = self.cart_all[i]['num'] * self.cart_all[i]['price']
            all_price+=p
            log_list.append('%s(%s)'%(self.cart_all[i]['name'],self.cart_all[i]['num']))
        log_str=','.join(log_list)
        atm_obj=atm()
        if atm_obj.cart_payfor_interface(all_price,log_str,self.user):
            self.cart_all = {}  # 清空购物车
        return  True
    #申请银行卡
    @auth
    def apply_credit_cart(self):
        #.apply_address()
        atm_obj=atm()
        return atm_obj.add_user()

    #商品列表
    @auth
    def get_goods_list(self ):
        res={}
        with open(r'%s/db/goods.txt'%os.path.dirname(os.path.dirname(__file__)),'r',encoding='utf-8') as f:
            for line in f:
                line_list=line.strip(' \n').split(',')
                line_list[-1]=int(line_list[-1])#单价转int
                res[line_list[0]]=line_list
        return res
    #获取user列表 其实是一个key=vaule(用户名：密码)的字典
    def get_user_list(self):
        res={}
        with open(r'%s/db/user.txt'%os.path.dirname(os.path.dirname(__file__)),'r',encoding='utf-8') as f:
            for line in f:
                line_list=line.strip(' \n').split(',')
                res[line_list[0]]=line_list[1]
        return res

    #追加user
    def append_user(self,user_list):
        with open(r'%s/db/user.txt'%os.path.dirname(os.path.dirname(__file__)), 'a', encoding='utf-8') as f:
            f.writelines(user_list)
        print('successfully')




