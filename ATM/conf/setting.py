#__Author__ = rianley cheng
#定义统一的登录状态
import time,pickle,os
class setting():

    user =''
    def auth(func):
        def wrapper(self,*args, **kwargs):
            if not self.user:
                print('请先登录!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                if  self.login():
                    return True
            return func( self,*args, **kwargs)
        return wrapper

    def get_user_list(self):
        with open(r'%s/db/users.txt' % os.path.dirname(os.path.dirname(__file__)), 'rb') as f:
            res = pickle.load(f)
            print(res)
            if not res: return []
        return res
    def login(self):
        user_info = self.get_user_list()
        if self.user:
            print('\033[0;32;40m用户%s已登录\033[0m' % user_info[self.user]['name'])
            return True
        while True:
            id = input('请输入卡号：').strip()
            if id == 'q': return True
            user = input('请输入用户名')
            if user == 'q': return True

            pwd = input('请输入密码：').strip()
            if pwd == 'q': return True

            if id in user_info and user_info[id]['pwd'] == pwd and user_info[id]['name'] == user:
                if user_info[id]['status'] == 1:
                    print('\033[0;32;40m该账户已被冻结！\033[0m')
                    return True
                print('\033[0;33;41m登录成功\033[0m')
                print()
                self.user = id
                user_info['login_time'] = time.time()
                return False
            print('请填写正确的卡号,用户名或密码')
#     @auth
#     def index(self):
#         print('this is func')
# index = setting()
#
# index.index()








