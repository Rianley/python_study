#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from include.school import SchoolStaticCls
from include.teacher import TeacherStaticCls
from modules.databases import DatabasesCls

class Admin(object):
    def __init__(self):
        super(Admin, self).__init__()

    def school_list(self):
        print("学校列表--")
        data = SchoolStaticCls.school_table.open()
        while True:
            print("_" * 50)
            print("学校代码\t\t\t学校名字\t\t\t\t学校地址")
            print("-" * 50)
            for k, v in data.items():
                code, name, city = k, v["name"], v["city"]
                print("【%s】\t\t\t%s\t\t\t\t%s" % (code, name, city))
            print("-" * 50)
            choice = input("请输入选项[A创建|C修改|D删除|B返回]: ")
            if choice == "A" or choice == "a":
                Admin.create_school(self)
            elif choice == "C" or choice == "c":
                Admin.modify_school(self)
            elif choice == "D" or choice == "d":
                Admin.delete_school(self)
            elif choice == "B" or choice == "b":
                break

    def create_school(self):
        print("创建学校--")
        print("/" * 15 + "创建学校 (*选项必填)" + "/" * 15)
        school_code = input("*学校代码(格式:101): ").strip()
        school_name = input("*学校名称: ").strip()
        school_city = input("*学校地址: ").strip()
        school = SchoolStaticCls(school_code, school_name, school_city)
        new_school = school.create()
        if new_school == 0:
            print("创建成功!")
        elif new_school == 1:
            print("创建失败! 无法保存.")
        elif new_school == 2:
            print("创建失败! 名字或城市输入错误.")
        elif new_school == 3:
            print("创建失败! 学校代码错误或已存在.")
        else:
            print("创建失败! 未知错误.")
        print(school.school_obj)


    def modify_school(self):
        print("修改学校--")
        print("/" * 15 + "修改学校资料 (*选项必填)" + "/" * 15)
        school_code = input("*学校代码: ").strip()
        school_name = input("*学校名称: ").strip()
        school_city = input("*学校地址: ").strip()
        school = SchoolStaticCls(school_code, school_name, school_city)
        result = school.update()
        if result == 0:
            print("修改成功!")
        elif result == 1:
            print("修改失败! 无法保存.")
        elif result == 2:
            print("修改失败! 名字或城市输入错误.")
        elif result == 3:
            print("修改失败! 学校代码错误或不存在.")
        else:
            print("修改失败! 未知错误.")
        print(school.school_obj)

    def delete_school(self):
        print("删除学校--")
        data = SchoolStaticCls.school_table.open()
        school_code = input("*请输入要删除的学校代码: ").strip()
        if school_code in data:
            enter = input("确认删除学校%s的所有资料？[Y|n]" % school_code)
            if enter == "Y" or enter == "y":
                try:
                    del data[school_code]
                    SchoolStaticCls.school_table.save(data)
                    print("删除成功.")
                except KeyError:
                    pass
            else:
                print("返回!")
        else:
            print("学校代码不存在!")


    def teacher_list(self):
        print("讲师列表--")
        teacher_data = TeacherStaticCls.teacher_table.open()
        school_data = SchoolStaticCls.school_table.open()
        while True:
            print("_" * 150)
            print("-" * 150)
            for k, v in teacher_data.items():
                t_id, t_name, t_school, t_title, t_salary, t_phone, t_email = \
                    k, v["name"], v["school_id"], v["title"], v["salary"], v["phone"], v["email"]
                account = k.center(10, " ")
                t_name = t_name.center(10, " ")
                t_title = t_title.center(12, " ")
                t_school = school_data[v["school_id"]]["name"]
                print("讲师ID: %s\t 讲师名称: %s\t 所属学校: %s\t 讲师职务: %s\t 讲师薪资: %s\t 手机号码: %s\t 邮箱: %s" % \
                      (account, t_name, t_school, t_title, t_salary, t_phone, t_email))
            print("-" * 150)
            choice = input("请输入选项[A创建|C修改|D删除|B返回]: ")
            if choice == "A" or choice == "a":
                Admin.create_teacher(self)
            elif choice == "C" or choice == "c":
                Admin.modify_teacher(self)
            elif choice == "D" or choice == "d":
                Admin.delete_teacher(self)
            elif choice == "B" or choice == "b":
                break


    def create_teacher(self):
        print("创建讲师--")
        print("/" * 15 + "创建讲师 (*选项为必填)" + "/" * 15)
        account = input("*讲师登录帐号: ").strip()
        password = input("*讲师登录密码: ").strip()
        teacher_name = input("*讲师的姓名: ").strip()
        teacher_phone = input("*手机号码: ").strip()
        teacher_school = input("*所在的学校编号: ").strip()
        teacher_title = input("*讲师职务: ").strip()
        teacher_salary = input("*讲师薪资: ").strip()
        teacher_email = input("-电子邮箱: ").strip()
        teacher = TeacherStaticCls(
            account, password, teacher_name, teacher_phone, teacher_school,
            teacher_title, teacher_salary, teacher_email
        )
        new_teacher = teacher.create()
        if new_teacher == 0:
            print("创建成功!")
        elif new_teacher == 1:
            print("帐号不能为空或已存在!")
        elif new_teacher == 2:
            print("资料未完善!")
        elif new_teacher == 3:
            print("学校代码不存在!")
        else:
            print("创建失败!")
        print(teacher.teacher_obj)

    def modify_teacher(self):
        print("修改讲师--")
        data = TeacherStaticCls.teacher_table.open()
        print("/" * 15 + "修改讲师资料 (*选项必填)" + "/" * 15)
        account = input("*请输入要修改的讲师的帐号: ").strip()
        if account in data:
            print("输入要修改的资料: ")
            password = data[account]["password"]
            teacher_name = input("*讲师的姓名: ").strip()
            teacher_phone = input("*手机号码: ").strip()
            teacher_school = input("*所在的学校编号: ").strip()
            teacher_title = input("*讲师职务: ").strip()
            teacher_salary = input("*讲师薪资: ").strip()
            teacher_email = input("-电子邮箱: ").strip()
            teacher = TeacherStaticCls(
                account, password, teacher_name, teacher_phone, teacher_school,
                teacher_title, teacher_salary, teacher_email
            )
            result = teacher.update()
            if result == 0:
                print("修改成功!")
            elif result == 1:
                print("帐号不存在!")
            elif result == 2:
                print("资料未完善!")
            elif result == 3:
                print("学校代码不存在!")
            else:
                print("修改失败!")
            print(teacher.teacher_obj)
        else:
            print("帐号不存在!")


    def delete_teacher(self):
        print("删除讲师--")
        account = input("*请输入要删除的讲师的帐号: ").strip()
        enter = input("确认删除讲师%s的所有资料？[Y|n]" % account)
        if enter == "Y" or enter == "y":
            result = TeacherStaticCls.delete(account)
            if result == 0:
                print("删除成功.")
            else:
                print("找不到讲师帐号.")


    def student_list(self):
        print("学员列表--")
        student_pc_table = DatabasesCls("student_purchase_course")
        course_table = DatabasesCls("courses")
        data = student_pc_table.open()
        course_data = course_table.open()
        print(data)
        while True:
            print("_" * 100)
            print("学员ID\t\t\t购买的课程\t\t\t课程名称\t\t\t购买时间\t\t\t\t\t班级关联状态")
            print("-" * 100)
            for k,v in data.items():
                for i,j in v.items():
                    student_id = k
                    course_id = i
                    course_name = course_data[course_id]["name"]
                    purchase_time = j["purchase_time"]
                    status = j["status"]
                    status_com = ""
                    if status == 0:
                        status_com = "未关联"
                    elif status == 1:
                        status_com = "已关联"
                    print("%s\t\t\t%s\t\t\t\t\t%s\t\t\t%s\t\t\t%s" % (student_id,course_id,course_name,purchase_time,status_com))
            print("-" * 100)
            choice = input("请输入选项[A关联班级|B|b返回]: ").strip()
            if choice == "B" or choice == "b":
                break
            elif choice == "A" or choice == "a":
                Admin.join_student(self)

    def join_student(self):
        student_table = DatabasesCls("students")
        classroom_table = DatabasesCls("classroom")
        student_classroom = DatabasesCls("student_classroom")
        student_pc_table = DatabasesCls("student_purchase_course")
        student_data = student_table.open()
        classroom_data = classroom_table.open()
        sc_data = student_classroom.open()
        pc_data = student_pc_table.open()
        print("关联班级--")
        print("/" * 15 + "学员关联班级 (*选项为必填)" + "/" * 15)
        student_id = input("*请输入学员的ID: ").strip()
        student_class_id = input("*请输入该学员关联的班级ID: ").strip()
        print(sc_data)
        if student_id in student_data:
            if student_id in pc_data:
                if student_class_id in classroom_data:
                    try:
                        s_list = sc_data[student_class_id]
                    except:
                        s_list = []

                    if student_id not in s_list:
                        s_list.append(student_id)
                        print(s_list)
                        sc_data[student_class_id] = s_list
                        student_classroom.save(sc_data)

                        course_id = classroom_data[student_class_id]["course_id"]
                        pc_data[student_id][course_id]["status"] = 1
                        student_pc_table.save(pc_data)
                        print("关联成功!")
                        time.sleep(1)

                    else:
                        print("学员%s已经关联到该班级." % student_id)
                    print(sc_data)
                else:
                    print("班级ID不存在!!")
            else:
                print("该学员未购买该课程!!")
        else:
            print("学员ID不存在!!")










