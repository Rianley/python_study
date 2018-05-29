#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls
from modules.databases import user_data

# user_data = {"user_id": None, "is_authenticated": False, "user_data": None}

class StudentsAccountCls(object):
    def __init__(self, cookie):
        super(StudentsAccountCls, self).__init__()
        self.cookie = cookie
        self.user_table = DatabasesCls("students")

    @staticmethod
    def login_required(func):  # 用户登录装饰器
        def wrapper(*args, **kwargs):
            cookie = user_data
            if cookie['is_authenticated']:
                return func(*args, **kwargs)
            else:
                print("帐号未登录验证！")
        return wrapper

    def set_session(self,user,account_data):
        try:
            self.cookie['user_id'] = user
            self.cookie['is_authenticated'] = True
            self.cookie['user_data'] = account_data
            return True
        except:
            pass

    def clear_session(self,user_data):
        try:
            user_data['user_id'] = None
            user_data['is_authenticated'] = False
            user_data['user_data'] = None
            return True
        except:
            pass

    def logout(self):
        StudentsAccountCls.clear_session(self,self.cookie)

    def login(self):
        print(self.cookie)
        accounts_dict = self.user_table.open()
        retry_count = 0
        while retry_count < 3:
            username = input("Username: ")
            password = input("Password: ")
            if username != "" and password != "":
                if username in accounts_dict:
                    user_pass = accounts_dict[username]["password"]
                    if password == user_pass:
                        print("验证成功！")
                        account_data = accounts_dict[username]
                        StudentsAccountCls.set_session(self,username,account_data)
                        return self.cookie
                    else:
                        print("帐号或密码错误!")
                        retry_count += 1
                else:
                    print("该用户名未注册!")
            else:
                print("帐号或密码不能为空!")
                retry_count += 1

    def forgot(self):
        accounts_dict = self.user_table.open()
        print("----重置密码----")
        retry_count = 0
        while retry_count < 3:
            username = input("请输入你的用户名: ")
            if username in accounts_dict:
                password = input("请输入新密码(3-18位字符): ")
                if password != "" and len(password) >= 3 and len(password) <= 18:
                    password2 = input("再次输入新密码: ")
                    if password2 == password:
                        accounts_dict[username]["password"] = password2
                        self.user_table.save(accounts_dict)
                        print("修改成功.")
                        break
                    else:
                        print("两次输入密码不匹配.")
                        retry_count += 1
                else:
                    print("密码不符合要求!")
                    retry_count += 1
            else:
                print("该用户不存在!")

    def registered(self):
        print("----注册帐号----")
        print("/" * 15 + "注册帐号 (*选项必填)" + "/" * 15)
        accounts_dict = self.user_table.open()
        while True:
            username = input("*输入您要注册的用户名: ").strip()
            password = input("*输入您要设置的密码(3-12位字符): ").strip()
            password2 = input("*再次输入新密码: ").strip()
            real_name = input("*输入您的姓名: ")
            gender = input("*输入您的性别: ").strip()
            dob = input("*输入您的出生年月日(0000-00-00): ").strip()
            phone = input("*请输入11位数字的手机号码(如:13100224466): ").strip()
            email = input("*输入您的电子邮箱: ").strip()

            if username.isalnum() and username not in accounts_dict:
                if password != "":
                    if password == password2:
                        if gender != "" and dob != "" and phone != "" and email != "" and real_name != "":
                            dict = {}
                            student_id = 10000 + len(accounts_dict) + 1
                            enroll_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            status = 0
                            dict["student_id"] = student_id
                            dict["name"] = real_name
                            dict["password"] = password
                            dict["gender"] = gender
                            dict["dob"] = dob
                            dict["phone"] = phone
                            dict["email"] = email
                            dict["enroll_date"] = enroll_date
                            dict["status"] = status
                            accounts_dict[username] = dict
                            choice = input("确定注册[Y|n]?")
                            if choice == "Y" or choice == "y":
                                self.user_table.save(accounts_dict)
                                print("注册成功!")
                                time.sleep(1)
                                break
                        else:
                            print("资料未完善!")
                            break
                    else:
                        print("两次输入密码不匹配!")
                        break
                else:
                    print("密码不能为空!")
                    break
            else:
                print("帐号格式不正确或已存在!")
                break


class AccountLoginCls(StudentsAccountCls):
    def __init__(self,cookie):
        super(AccountLoginCls,self).__init__(cookie)
        self.cookie = cookie

    def account_login(self):
        prompt = """
        -------登录页面-------
        1. 帐号登录
        2. 忘记密码
        3. 立即注册
        4. 返回首页
        ---------------------
        Enter your choice: """
        user = StudentsAccountCls(self.cookie)
        choice = ""
        while choice != "4":
            choice = input(prompt)
            menu_dic = {
                '1': user.login,
                '2': user.forgot,
                '3': user.registered
            }
            if choice in menu_dic:
                login = menu_dic[choice]()
                if login:
                    break

