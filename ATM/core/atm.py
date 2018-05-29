# Author: Alan
import pickle,time,random,os,re
#只能在主界面输入q退出，其它时候输入q 只结束本次操作
# 2个测试卡号->密码  1111->456   6937->123 6930->789
class atm:
    user=''
    repay_day='10'#还款日
    month_bill='22'#每月22号出账单 假的
    operation=[
        '申请信用卡或是注册账户',
        '登录',
        '取款',
        '存款',
        '还款',
        '转账',
        '当月操作记录',
        '查看信息',
        '冻结账户',
        '解冻账户',
        '上月账单',
        '退出登录'
    ]
    dict_list=[]

    def __init__(self):

        dict_list = [
             self.add_user,
             self.login,
             self.withdraw,
             self.deposit,
             self.repay,
             self.transfer,
             self.operate_log,
             self.check_user_info,
             self.freez_account,
             self.not_freez_account,
             self.bill,
             self.logout,

        ]
        self.dict_list=dict_list

    def auth(func):
        def wrapper(self,*args, **kwargs):
            if not self.user:
                print('请先登录!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                if  self.login():
                    return True
            return func( self,*args, **kwargs)
        return wrapper
    #申请银行卡或是添加用户
    def add_user(self):
        one_dict={}
        user_list=self.get_user_list()
        if not user_list:user_list={}

        id='1111'  #随机卡号，保证不重复，限额9000
        while id in user_list:
            id=random.randint(1000,10000)
        print('给你分配的卡号为：%s,请牢记或保存好它'%id)
        while True:
            name=input('请设置信用卡用户名：').strip()
            if not name:continue
            if name=='q':return  True
            break
        while True:
            pwd = input('请设置信用卡密码：').strip()
            if not pwd: continue
            if pwd == 'q':return True
            break
        while True:
            limit = input('请设置信用卡额度：').strip()
            if pwd == 'q':return True
            if not limit.isdigit():continue
            break
        limit=int(limit)
        id=str(id)
        one_dict['id']=id
        one_dict['name'] = name
        one_dict['pwd'] = pwd
        one_dict['balance'] = limit
        one_dict['debt'] = limit
        one_dict['interest'] = 0
        one_dict['status'] = 0 #是否冻结  1：表示冻结
        user_list[id]=one_dict
        self.update_user(user_list)
        print('申请信用卡成功！卡号：%s'%id)
        return True
    #取钱
    @auth
    def withdraw(self):
        user_info=self.get_user_list()
        print('%s用户你好！你的余额为：%s,当前欠款为：%s'%(self.user,user_info[self.user]['balance'],user_info[self.user]['debt']))
        while True:
            p=input('请输入你要取走的金额(5%的手续费)：').strip()
            if p=='q':return True
            if not p.isdigit():continue
            p=int(p)
            if p*1.05>user_info[self.user]['balance']:
                print('余额不足！')
                continue
            break
        user_info[self.user]['balance']-=p*1.05
        self.update_user(user_info)
        self.write_log('取款%s'%p,p,0.05*p)

        print('取款成功！当前余额为：%s'%user_info[self.user]['balance'])
        print('请继续你的操作！')
        return False

    #存钱
    @auth
    def deposit(self):
        user_info = self.get_user_list()
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user, user_info[self.user]['balance'], user_info[self.user]['debt']))
        while True:
            p = input('请输入你要存入的金额：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            if p<=0:
                print('金额够小！')
                continue
            break
        user_info[self.user]['balance'] += p
        self.update_user(user_info)
        self.write_log('存款%s' % p, 0-p)

        print('存款成功！当前余额为：%s' % user_info[self.user]['balance'])
        print('请继续你的操作！')
        return False

    #还款
    @auth
    def repay(self):
        user_info = self.get_user_list()
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user, user_info[self.user]['balance'], user_info[self.user]['debt']))
        while True:
            p = input('请输入你要还款的金额（从当前余额扣款）：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            if p <= 0:
                print('金额够小！')
                continue
            if p>user_info[self.user]['balance']:
                print('超过余额限制')
                continue
            break
        if p>user_info[self.user]['debt']:
            p=user_info[self.user]['debt']

        user_info[self.user]['balance'] -= p
        user_info[self.user]['debt']-=p
        self.update_user(user_info)
        self.write_log('还款%s' % p, p)
        if user_info[self.user]['debt']==0:
            print('已成功还请欠款！当前余额为：%s'%user_info[self.user]['balance'])
            return True
        print('还款成功！当前余额为：%s,欠款为：%s' % (user_info[self.user]['balance'],user_info[self.user]['debt']))
        return False

    #转账
    @auth
    def transfer(self):
        user_info = self.get_user_list()
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user, user_info[self.user]['balance'], user_info[self.user]['debt']))

        while True:
            name_x=input('请输入你要转账的账户的卡号：').strip()
            if name_x=='q':return True
            if not name_x.isdigit() or name_x not in user_info or name_x==self.user:
                print('卡号不存在或有误')
                continue
            break
        while True:
            p = input('请输入你要转账的金额（从当前余额扣款）：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            if p <= 0:
                print('金额够小！')
                continue
            if p > user_info[self.user]['balance']:
                print('超过余额限制')
                continue
            break
        user_info[self.user]['balance'] -= p
        user_info[name_x]['debt'] += p
        self.update_user(user_info)
        self.write_log('向%s转账%s' %( name_x,p), p)

        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(r'%s/log/log.txt'%os.path.dirname(os.path.dirname(__file__)), 'a', encoding='utf-8') as f:
            f.write('%s---%s---%s---%s---%s\n' % (name_x, local_time, '收到%s的转账%s'%(self.user,p), 0-p, 0))

        print('转账成功！当前余额为：%s,欠款为：%s' % (user_info[self.user]['balance'], user_info[self.user]['debt']))
        return True

    # 当月操作记录
    @auth
    def operate_log(self):
        print('用户名','时间','操作记录','涉及金额','手续费')
        local_mouth=time.strftime('%Y-%m')
        regex_str = '%s---%s'%(self.user,local_mouth)
        with open(r'%s/log/log.txt'%os.path.dirname(os.path.dirname(__file__)),'r',encoding='utf8') as f:
            for line in f:
                if regex_str in line:
                    for i in line.strip('\n').split('---'):
                        print( self.get_user_list()[self.user]['name'] if i==self.user else i,end=' ')#懒得改
                    print()
        return True

    @auth
    def check_user_info(self):
        id=self.user
        user_info=self.get_user_list()
        print('卡号','用户名', '余额', '欠款')
        print(id,user_info[id]['name'],user_info[id]['balance'],user_info[id]['debt'])
        return True
    #获取user列表
    def get_user_list(self):
        with open(r'%s/db/users.txt'%os.path.dirname(os.path.dirname(__file__)), 'rb') as f:
            res=pickle.load(f)
            if not res:return []
        return res

    #修改user
    def update_user(self,user_list):
        with open(r'%s/db/users.txt'%os.path.dirname(os.path.dirname(__file__)),'wb') as f:
            pickle.dump(user_list,f)
    #写入日志
    @auth
    def write_log(self,content,m=0,n=0):
        local_time=time.strftime('%Y-%m-%d %H:%M:%S')
        with open(r'%s/log/log.txt'%os.path.dirname(os.path.dirname(__file__)),'a',encoding='utf-8') as f:
            f.write('%s---%s---%s---%s---%s\n'%(self.user,local_time,content,m,n))

        return True
    #冻结账户
    def freez_account(self):
        user_info = self.get_user_list()
        while True:
            id = input('请输入要冻结卡号：').strip()
            if id == 'q': return True
            pwd = input('请输入密码：').strip()
            if  pwd == 'q': return True
            if id in user_info and user_info[id]['pwd'] == pwd:
                user_info[id]['status']=1
                self.update_user(user_info)
                self.user=''
                print('卡号%s冻结成功！'%id)
                return True
            print('卡号或密码错误')
        return True
    #解冻账户
    def not_freez_account(self):
        user_info = self.get_user_list()
        while True:
            id = input('请输入要解冻卡号(q退出操作)：').strip()
            if id == 'q': return True
            pwd = input('请输入密码：').strip()
            if  pwd == 'q': return True
            if id in user_info and user_info[id]['pwd'] == pwd:
                if user_info[id]['status']==0:
                    print('该账户未被冻结')
                    continue
                user_info[id]['status']=0
                self.update_user(user_info)
                self.user=''
                print('卡号%s解冻成功！'%id)
                return True
            print('卡号或密码错误')
        return True
    def login(self):
        user_info = self.get_user_list()
        if self.user:
            print('\033[0;32;40m用户%s已登录\033[0m'%user_info[self.user]['name'])
            return True
        while True:
            id = input('请输入卡号：').strip()
            if id == 'q':return True
            pwd = input('请输入密码：').strip()
            if pwd == 'q':return True
            if id in user_info and user_info[id]['pwd']==pwd:
                if user_info[id]['status']==1:
                    print('该账户已被冻结！')
                    return True
                print('登录成功')
                print()
                self.user=id
                user_info['login_time']=time.time()
                return False
            print('卡号或密码错误')
    @auth
    def logout(self):
        self.user=''
        print('退出登录成功')
        return  True
    #购物车用信用卡结账接口
    def cart_payfor_interface(self,p,str,user_cart):
        if not self.login():
            user_info = self.get_user_list()

            user_info[self.user]['balance'] -= p
            self.update_user(user_info)
            self.write_log('商城用户（%s）购买商品--%s' % (user_cart,str), p)
            print('结算成功！')
            return True
        return False

    #每月22号出账单 假的
    @auth
    def bill(self):
        local_date = time.strftime('%Y-%m-%d')

        if True:#local_date.split('-')[2] == self.month_bill
            zz = time.strptime(local_date, '%Y-%m-%d')
            yy = time.mktime(zz) - int(local_date.split('-')[2]) * 3601 * 24
            xx = time.strftime('%Y-%m', time.localtime(yy))
            res=self.get_user_list()
            print('用户名', '时间', '操作记录', '涉及金额', '手续费')
            with open(r'%s/log/log.txt'%os.path.dirname(os.path.dirname(__file__)), 'r', encoding='utf-8') as f:
                str='%s---%s'%(self.user,xx)
                for line in f:
                    if line.find(str)>-1:
                        for j in line.strip(' \n').split('---'):
                            print(res[j]['name'] if j==self.user else j,end=' ')
                        print()
                return True
        return True
     #计算未按时还款的利息,没想好
    def repay_interest(self):
        pass

