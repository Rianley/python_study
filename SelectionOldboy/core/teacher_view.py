#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os
import sys
import time
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls

class Teacher(object):
    teacher_table = DatabasesCls("teachers")

    def __init__(self):
        super(Teacher,self).__init__()

    def view_classroom(self,teacher_id):
        print("查看班级学员--")
        cr_table = DatabasesCls("classroom")
        sc_table = DatabasesCls("student_classroom")
        course_table = DatabasesCls("courses")
        spc_table = DatabasesCls("student_purchase_course")
        cr_data = cr_table.open()
        sc_data = sc_table.open()
        course_data = course_table.open()
        spc_data = spc_table.open()
        classes = []
        while True:
            print("_" * 120)
            print("班级ID\t\t班级名称\t\t\t\t讲师ID\t\t\t课程ID\t\t课程名称\t\t\t学校ID\t\t班级人数\t\t\t创建时间")
            print("-" * 120)
            for class_id,class_value in cr_data.items():
                teacher = class_value["teacher_id"]
                if teacher == teacher_id:
                    classes.append(class_id)
                    class_name = class_value["class_name"]
                    course_id = class_value["course_id"]
                    course_name = course_data[course_id]["name"]
                    school_id = class_value["school_id"]
                    count = len(sc_data[class_id])
                    enroll_date = class_value["enroll_date"]
                    print("%s\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t\t%s\t\t\t%s" % \
                          (class_id,class_name,teacher,course_id,course_name,school_id,count,enroll_date))
            print("-" * 120)
            choice = input("输入选项: \n"
                           "1 查看学员\n"
                           "2 开始上课\n"
                           "3 返回\n"
                           "Enter your choice: ")
            if choice == "3":
                break
            if choice == "1":
                print("查看班级学员--")
                class_id2 = input("请输入班级ID: ")
                if class_id2 in classes:
                    while True:
                        print("_" * 80)
                        print("班级ID\t\t学生ID\t\t\t课程名称\t\t\t学习次数\t\t\t成绩")
                        print("-" * 80)
                        student_list = sc_data[class_id2]
                        if class_id2 in cr_data:

                            course_id = cr_data[class_id2]["course_id"]
                            course_name = course_data[course_id]["name"]


                            for student_id in student_list:
                                if student_id in spc_data:
                                    study_count = spc_data[student_id][course_id]["count"]
                                    study_grade = spc_data[student_id][course_id]["grade"]
                                    print("%s\t\t%s\t\t\t%s\t\t\t%s\t\t\t\t%s" % (
                                             class_id2, student_id, course_name, study_count, study_grade))
                            print("-" * 80)
                            choice = input("输入选项: \n"
                                           "1 修改学员成绩\n"
                                           "2 返回\n"
                                           "Enter your choice: ")
                            if choice == "2":
                                return
                            if choice == "1":
                                print("修改学员成绩--")
                                student = input("输入学员ID: ")
                                grade = input("输入学员成绩: ")
                                if student in student_list:
                                    if grade.isdigit():
                                        spc_data[student][course_id]["grade"] = grade
                                        spc_table.save(spc_data)
                                        print(spc_data)
                                        print("修改成功!")
                                        time.sleep(1)
                                    else:
                                        print("成绩格式错误!")
                                else:
                                    print("学员不存在!")
                else:
                    print("班级ID不存在!")
            if choice == "2":
                print("选择班级上课--")
                class_id3 = input("请输入班级ID: ")
                if class_id3 in classes:
                    print("开始上课----")
                    time.sleep(1)
                else:
                    print("班级ID不存在!")