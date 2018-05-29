#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls
from modules.databases import user_data
from include.course import CourseStaticCls

# user_data = {"user_id": None, "is_authenticated": False, "user_data": None}


class Student(object):
    def __init__(self,name):
        super(Student,self).__init__()
        self.name = name
        self.student_purchase_course = DatabasesCls("student_purchase_course")

    def course_list(self):
        data = CourseStaticCls.course_table.open()
        purchase_dict = self.student_purchase_course.open()
        user_name = user_data["user_id"]

        while True:
            print("_" * 100)
            print("课程编号\t\t  课程名称\t\t\t课程价格\t\t\t课程周期\t\t课程大纲")
            print("-" * 100)
            for k, v in data.items():
                id, name, price, period, outline = \
                    k, v["name"], v["price"], v["period"], v["outline"]
                name = name.center(10, " ")
                print("<< %s >>\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s" % \
                      (id, name, price, period, outline))
            print("-" * 100)
            choice = input("请输入课程编号进行选课购买[B返回]: ").strip()
            if choice == "B" or choice == "b":
                break
            try:
                choice = int(choice)
            except:
                pass
            if choice in data:
                enter = input("确认购买?[Y|n]")
                if enter == "Y" or enter == "y":
                    if user_name not in purchase_dict:
                        dict1 = {}
                        dict2 = {}
                        purchase_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        dict1["purchase_time"] = purchase_time
                        dict1["status"] = 0
                        dict1["grade"] = 0
                        dict1["count"] = 0
                        dict2[choice] = dict1
                        purchase_dict[user_name] = dict2
                        self.student_purchase_course.save(purchase_dict)
                        print("购买成功!")
                        time.sleep(1)
                    else:
                        dict1 = {}
                        dict2 = purchase_dict[user_name]
                        if choice not in purchase_dict[user_name]:
                            purchase_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            dict1["purchase_time"] = purchase_time
                            dict1["status"] = 0
                            dict1["grade"] = 0
                            dict1["count"] = 0
                            dict2[choice] = dict1
                            purchase_dict[user_name] = dict2
                            self.student_purchase_course.save(purchase_dict)
                            print("购买成功!")
                            time.sleep(1)
                        else:
                            print("您已购买该课程, 快开始学习吧!")
                else:
                    print("取消购买.")
            else:
                print("课程ID不存在!")


    def my_course(self):
        print("我的课程--")
        user_name = user_data["user_id"]
        sc_table = DatabasesCls("student_classroom")
        cr_table = DatabasesCls("classroom")
        courses_table = DatabasesCls("courses")
        spc_table = DatabasesCls("student_purchase_course")
        spc_data = spc_table.open()
        courses_data = courses_table.open()
        sc_data = sc_table.open()
        cr_data = cr_table.open()
        print(sc_data)
        print(cr_data)
        print(courses_data)
        print(spc_data)
        while True:
            print("_" * 50)
            print("课程ID\t\t\t课程名称\t\t\t课程大纲")
            print("-" * 50)
            course_dict = spc_data[user_name]
            for id,value in course_dict.items():
                course_id = id
                course_name = courses_data[course_id]["name"]
                course_outline = courses_data[course_id]["outline"]
                print("%s\t\t\t\t%s\t\t\t%s" %(course_id,course_name,course_outline))
            print("-" * 50)
            choice = input("选择课程ID进入学习[B返回]: ")
            print(course_dict)
            if choice == "B" or choice == "b":
                    break
            try:
                choice = int(choice)
            except:
                pass
            if choice in course_dict:
                course = courses_data[choice]["name"]
                try:
                    course_dict[choice]["count"] += 1
                except:
                    course_dict[choice]["count"] = 0
                finally:
                    spc_data[user_name] = course_dict
                    spc_table.save(spc_data)
                    print("正在学习课程%s, 已学习%s次..." % (course, course_dict[choice]["count"]))
                    time.sleep(1)


    def my_classroom(self):
        print("我的班级--")
        user_name = user_data["user_id"]
        sc_table = DatabasesCls("student_classroom")
        cr_table = DatabasesCls("classroom")
        sc_data = sc_table.open()
        cr_data = cr_table.open()
        while True:
            print("_" * 50)
            print("班级ID\t\t\t班级名称\t\t\t\t讲师")
            print("-" * 50)
            print(sc_data)
            for class_id,student_list in sc_data.items():
                if user_name in student_list:
                    class_name = cr_data[class_id]["class_name"]
                    teacher = cr_data[class_id]["teacher_id"]
                    print("%s\t\t\t%s\t\t\t%s" % (class_id,class_name,teacher))
            print("-" * 50)
            choice = input("[B|b返回]: ")
            if choice == "B" or choice == "b":
                break


    def study_record(self):
        print("上课记录--")
        user_name = user_data["user_id"]
        spc_table = DatabasesCls("student_purchase_course")
        courses_table = DatabasesCls("courses")
        spc_data = spc_table.open()
        course_data = courses_table.open()
        while True:
            print("_" * 50)
            print("课程ID\t\t\t课程名称\t\t\t学习次数")
            print("-" * 50)
            course_dict = spc_data[user_name]
            for course_id,value in course_dict.items():
                course_name = course_data[course_id]["name"]
                try:
                    study_count = value["count"]
                except:
                    study_count = 0
                print("%s\t\t\t\t%s\t\t\t%s" % (course_id,course_name,study_count))
            print("-" * 50)
            choice = input("[B|b返回]: ")
            if choice == "B" or choice == "b":
                break

    def view_grade(self):
        print("查询成绩--")
        user_name = user_data["user_id"]
        spc_table = DatabasesCls("student_purchase_course")
        courses_table = DatabasesCls("courses")
        spc_data = spc_table.open()
        course_data = courses_table.open()
        while True:
            print("_" * 50)
            print("课程ID\t\t\t课程名称\t\t\t学习成绩")
            print("-" * 50)
            course_dict = spc_data[user_name]
            for course_id, value in course_dict.items():
                course_name = course_data[course_id]["name"]
                study_grade = value["grade"]
                print("%s\t\t\t\t%s\t\t\t%s分" % (course_id, course_name, study_grade))
            print("-" * 50)
            choice = input("[B|b返回]: ")
            if choice == "B" or choice == "b":
                break


