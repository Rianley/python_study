#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core.admin_view import Admin
from core.school_view import School
from core.student_view import Student
from core.teacher_view import Teacher

from modules.UserAuth import AccountLoginCls
from modules.databases import user_data
from modules.databases import login_prompt



class StudentView(object):  #学员视图
    def __init__(self,cookie):
        super(StudentView, self).__init__()
        self.cookie = cookie
        self.username = cookie["user_id"]
        self.login = AccountLoginCls(cookie)
        self.student = Student(self.username)


    def student_menu(self):
        prompt_s = '''
----------------[Student View - {0}]----------------
                1. 进入选课
                2. 学习中心
                3. 个人中心
                4. {1}
                5. 帐号注册
                6. 返回上级
-----------------------------------------------------
Enter your choice: '''
        menu_dict = {
            '1': StudentView.courses_center,
            '2': StudentView.study_center,
            '3': StudentView.personal_center,
            '4': StudentView.account_center,
            '5': StudentView.account_enroll
        }
        choice = ''
        prompt_menu = ""
        login_s = False
        while choice != '6':
            username = self.cookie["user_id"]
            if self.cookie["is_authenticated"] == False:
                prompt_menu = prompt_s.format(username,login_prompt.get("login"))
                login_s = False
            elif self.cookie["is_authenticated"] == True:
                prompt_menu = prompt_s.format(username,login_prompt.get("logout"))
                login_s = True
            choice = input(prompt_menu)

            if choice in menu_dict:
                if choice == '4':
                    if login_s == True:
                        StudentView.logout(self)
                        return True
                menu_dict[choice](self)


    @AccountLoginCls.login_required
    def courses_center(self):
        print("选课中心--")
        self.student.course_list()

    @AccountLoginCls.login_required
    def study_center(self):
        print("学习中心--")
        prompt = '''
        ----------------学习中心----------------
            1. 我的课程
            2. 我的班级
            3. 上课记录
            4. 我的成绩
            5. 返回上级
        ----------------------------------------
        Enter your choice: '''
        menu_dict = {
            '1': self.student.my_course,
            '2': self.student.my_classroom,
            '3': self.student.study_record,
            '4': self.student.view_grade
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in menu_dict:
                menu_dict[choice]()
            elif choice == '5':
                exit_flag = False


    @AccountLoginCls.login_required
    def personal_center(self):
        print("个人中心--")

    def account_center(self):
        print("帐号中心--")
        self.login.account_login()

    def account_enroll(self):
        print("帐号注册--")
        self.login.registered()

    def logout(self):
        print("退出登录")
        self.login.logout()



class TeacherView(object):
    teacher_data = Teacher.teacher_table.open()
    def __init__(self):
        super(TeacherView, self).__init__()
        self.teacher_id = ""

    def login(self):
        username = input("输入讲师帐号: ")
        password = input("输入讲师密码: ")
        if username in self.teacher_data:
            passwd = self.teacher_data[username]["password"]
            if password == passwd:
                print("登录验证成功！")
                self.teacher_id = username
                return True

    def menu(self):
        prompt = '''
        -----------------[Teacher View]-----------------
                        1. 查看班级
                        2. 返回上级
        ------------------------------------------------
        Enter your choice: '''
        menu = {
            '1': Teacher.view_classroom

        }
        login = self.login()
        if login:
            choice = ''
            while choice != "2":
                choice = input(prompt)
                if choice in menu:
                    menu[choice](self,self.teacher_id)
        else:
            print("登录失败！")




class ManagementView(Admin):
    username, password = "admin", "admin"
    def __init__(self):
        super(ManagementView, self).__init__()

    def login(self):
        username = input("输入管理员帐号: ")
        password = input("输入管理员密码: ")
        if username == self.username and password == self.password:
            print("登录验证成功！")
            return True

    def menu(self):
        prompt = '''
        ------------------[Admin View]------------------
                        1. 校区管理
                        2. 课程管理
                        3. 讲师管理
                        4. 班级管理
                        5. 学员管理
                        6. 返回首页
        ------------------------------------------------
        Enter your choice: '''
        login = self.login()
        menu_dict = {
            '1': ManagementView.school_manage,
            '2': ManagementView.course_manage,
            '3': ManagementView.teacher_manage,
            '4': ManagementView.classes_manage,
            '5': ManagementView.student_manage
        }
        if login:
            choice = ''
            while choice != "6":
                choice = input(prompt)
                if choice in menu_dict:
                    menu_dict[choice](self)
        else:
            print("登录失败！")

    def school_manage(self):
        print("校区管理---")
        prompt = '''
        ----------------校区管理----------------
        1. 查看校区
        2. 创建校区
        3. 修改校区
        4. 返回上级
        ----------------------------------------
        Enter your choice: '''
        menu_dict = {
            '1': Admin.school_list,
            '2': Admin.create_school,
            '3': Admin.modify_school
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in menu_dict:
                menu_dict[choice](self)
            elif choice == '4':
                exit_flag = False


    def course_manage(self):
        print("课程管理---")
        prompt = '''
        ----------------课程管理----------------
            1. 查看课程
            2. 创建课程
            3. 修改课程
            4. 返回上级
            ----------------------------------------
        Enter your choice: '''
        menu_dict = {
            '1': School.course_list,
            '2': School.create_course,
            '3': School.modify_course
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in menu_dict:
                menu_dict[choice](self)
            elif choice == '4':
                exit_flag = False


    def teacher_manage(self):
        print("讲师管理---")
        prompt = '''
        ----------------讲师管理----------------
            1. 查看讲师
            2. 创建讲师
            3. 修改讲师
            4. 返回上级
        ----------------------------------------
        Enter your choice: '''
        menu_dict = {
            '1': Admin.teacher_list,
            '2': Admin.create_teacher,
            '3': Admin.modify_teacher
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in menu_dict:
                menu_dict[choice](self)
            elif choice == '4':
                exit_flag = False


    def classes_manage(self):
        print("班级管理---")
        prompt = '''
        ----------------班级管理----------------
            1. 查看班级
            2. 创建班级
            3. 修改班级
            4. 返回上级
        ----------------------------------------
        Enter your choice: '''
        memu_dict = {
            '1': School.classroom_list,
            '2': School.create_classroom,
            '3': School.modify_classroom
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in memu_dict:
                memu_dict[choice](self)
            elif choice == '4':
                exit_flag = False



    def student_manage(self):
        print("学员管理---")
        prompt = '''
        ----------------学员管理----------------
                1. 查看学员
                2. 关联班级
                3. 返回上级
        ----------------------------------------
        Enter your choice: '''
        memu_dict = {
            '1': Admin.student_list,
            '2': Admin.join_student
        }
        exit_flag = True
        while exit_flag:
            choice = input(prompt)
            if choice in memu_dict:
                memu_dict[choice](self)
            elif choice == '3':
                exit_flag = False



class HomeMenu(object):
    def __init__(self):
        super(HomeMenu, self).__init__()


    def student_view(self):  #学员视图
        print("学员视图--")
        self.student_instance = StudentView(user_data)
        self.student_instance.student_menu()

    def teacher_view(self):  #讲师视图
        self.teacher_instance = TeacherView()
        self.teacher_instance.menu()

    def management_view(self):  #管理视图
        self.admin_instance = ManagementView()
        self.admin_instance.menu()

    def exit_option(self):
        exit("Bye.")


def run():
    prompt = '''
----------------欢迎进入选课系统!----------------
1. 学员视图
2. 讲师视图
3. 管理视图
4. 退出程序
------------------------------------------------
Enter your choice: '''
    obj = HomeMenu()
    while True:
        choice = input(prompt)
        menu_dic = {
            '1': obj.student_view,
            '2': obj.teacher_view,
            '3': obj.management_view,
            '4': obj.exit_option
        }
        if choice in menu_dic:
            menu_dic[choice]()
