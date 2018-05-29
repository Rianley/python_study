#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls
from include.course import CourseStaticCls
from include.classroom import ClassroomStaticCls
from include.teacher import TeacherStaticCls
from include.school import SchoolStaticCls


class School(object):
    def __init__(self):
        super(School, self).__init__()

    def course_list(self):
        print("课程列表--")
        data = CourseStaticCls.course_table.open()
        while True:
            print("_" * 100)
            print("课程编号\t\t  课程名称\t\t\t课程价格\t\t\t课程周期\t\t课程大纲")
            print("-" * 100)
            for k, v in data.items():
                id,name,price,period,outline = \
                    k,v["name"],v["price"],v["period"],v["outline"]
                name = name.center(10, " ")
                print("<< %s >>\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s" % \
                      (id,name,price,period,outline))
            print("-" * 100)
            choice = input("请输入选项[A创建|C修改|D删除|B返回]: ")
            if choice == "A" or choice == "a":
                School.create_course(self)
            elif choice == "C" or choice == "c":
                School.modify_course(self)
            elif choice == "D" or choice == "d":
                School.delete_course(self)
            elif choice == "B" or choice == "b":
                break

    def create_course(self):
        print("创建课程--")
        print("/" * 15 + "创建课程 (*选项必填)" + "/" * 15)
        course_name = input("*课程名称: ").strip()
        course_price = input("*课程价格: ").strip()
        course_period = input("-课程周期: ").strip()
        course_outline = input("-课程大纲: ")
        course = CourseStaticCls(course_name,course_price,course_period,course_outline)
        new_course = course.create()
        if new_course == 0:
            print("创建成功! ")
        elif new_course == 1:
            print("创建失败! 课程名字不能为空.")
        elif new_course == 2:
            print("创建失败! 课程价格格式错误.")
        elif new_course == 3:
            print("创建失败! 无法保存.")
        else:
            print("创建失败! 未知错误.")
        print(course.course_obj)

    def modify_course(self):
        print("修改课程--")
        print("/" * 15 + "修改课程资料 (*选项必填)" + "/" * 15)
        course_id = input("*请输入要修改的课程编号(ID): ").strip()
        try:
            course_id = int(course_id)
        except ValueError:
            print("请输入课程ID,或返回课程列表查看.")
        course_name = input("*课程名称: ").strip()
        course_price = input("*课程价格: ").strip()
        course_period = input("-课程周期: ").strip()
        course_outline = input("-课程大纲: ")
        course = CourseStaticCls(course_name, course_price, course_period, course_outline)
        result = course.update(course_id)
        if result == 0:
            print("修改成功! ")
        elif result == 1:
            print("修改失败! 课程ID不存在.")
        elif result == 2:
            print("修改失败! 课程名字不能为空.")
        elif result == 3:
            print("修改失败! 课程价格格式错误.")
        else:
            print("修改失败! 无法保存.")

    def delete_course(self):
        print("删除课程--")
        course_id = input("*请输入要删除的课程编号: ").strip()
        try:
            course_id = int(course_id)
        except ValueError:
            pass
        enter = input("确认删除课程编号%s的所有资料？[Y|n]" % course_id)
        if enter == "Y" or enter == "y":
            result = CourseStaticCls.delete(course_id)
            if result == 0:
                print("删除成功.")
            else:
                print("找不到课程编号.")


    def classroom_list(self):
        classroom_data = ClassroomStaticCls.classroom_table.open()
        course_data = CourseStaticCls.course_table.open()
        teacher_data = TeacherStaticCls.teacher_table.open()
        school_data = SchoolStaticCls.school_table.open()
        sc_table = DatabasesCls("student_classroom")
        sc_data = sc_table.open()
        print(sc_data)
        while True:
            print("_" * 130)
            print("-" * 130)
            for k, v in classroom_data.items():
                class_id, class_name, course_id, school_id, teacher_id = \
                    k, v["class_name"], v["course_id"], v["school_id"], v["teacher_id"]
                course_name = course_data[course_id]["name"]
                school_name = school_data[school_id]["name"]
                teacher_name = teacher_data[teacher_id]["name"]

                count = len(sc_data[class_id])
                print("班级ID: %s\t\t班级名字: %s\t\t课程ID: %s\t\t课程名字: %s\t\t所在学校: %s\t\t授课讲师: %s\t\t学生人数: %s" % \
                      (class_id, class_name, course_id, course_name, school_name, teacher_name,count))
            print("-" * 130)
            choice = input("输入班级ID查看班级学员(B返回): ")
            if choice == "B" or choice == "b":
                break
            School.view_classroom(self,choice)


    def view_classroom(self,class_id):
        sc_table = DatabasesCls("student_classroom")
        classroom_table = DatabasesCls("classroom")
        course_table = DatabasesCls("courses")
        school_table = DatabasesCls("schools")
        school_data = school_table.open()
        sc_data = sc_table.open()
        classroom_data = classroom_table.open()
        course_data = course_table.open()
        if class_id in sc_data:
            while True:
                print("_" * 100)
                print("班级ID\t\t学生ID\t\t\t讲师ID\t\t\t班级名称\t\t\t\t课程名称\t\t学校")
                print("-" * 100)
                student_list = sc_data[class_id]
                for student in student_list:
                    teacher_id = classroom_data[class_id]["teacher_id"]
                    class_name = classroom_data[class_id]["class_name"]
                    course_id = classroom_data[class_id]["course_id"]
                    course_name = course_data[course_id]["name"]
                    school_id = classroom_data[class_id]["school_id"]
                    school_name = school_data[school_id]["name"]
                    print("%s\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t%s" % \
                          (class_id,student,teacher_id,class_name,course_name,school_name))
                print("-" * 100)
                choice = input("[B|b返回]: ")
                if choice == "B" or choice == "b":
                    break
        else:
            print("该班级还没有学员!!")
            time.sleep(1)

    #创建班级了！
    def create_classroom(self):

        print("/" * 15 + "创建班级 (*选项为必填)" + "/" * 15)
        class_id = input("*输入要创建的班级ID(如:1801): ").strip()
        class_name = input("*输入要创建的班级名字: ").strip()
        course_id = input("*输入该班级开设(关联)的课程ID: ").strip()
        school_id = input("*输入该班级所在的学校ID: ").strip()
        teacher_id = input("*输入该班级的授课(关联)讲师的ID帐号: ").strip()
        try:
            course_id = int(course_id)
        except ValueError:
            pass
        classroom = ClassroomStaticCls(class_id,class_name,course_id,school_id,teacher_id)   # 初始化 对象中的数据
        new_classroom = classroom.create()   # 在初始化数据后 调用 create方法
        #==============================================
        # 增加一个为空的班级对应学生的信息的存放着
        sc_table = DatabasesCls("student_classroom")
        sc_data = sc_table.open()  #读取学生班级信息
        sc_data[class_id] =[]
        sc_table.save(sc_data)

        if new_classroom == 0:
            print("创建成功!")
        elif new_classroom == 1:
            print("创建失败! 无法保存.")
        elif new_classroom == 2:
            print("讲师不存在或讲师ID错误!")
        elif new_classroom == 3:
            print("课程不存在或课程ID错误!")
        elif new_classroom == 4:
            print("班级名字不能为空!")
        elif new_classroom == 5:
            print("班级ID已存在!")
        elif new_classroom == 6:
            print("学校不存在!")
        else:
            print("创建失败!")
        print(classroom.classroom_obj)
    #修改班级
    def modify_classroom(self):
        print("修改班级--")
        print("/" * 15 + "修改班级资料 (*选项必填)" + "/" * 15)
        class_id = input("*请输入要修改的班级编号ID: ").strip()
        class_name = input("*输入新的班级名字: ").strip()
        course_id = input("*输入该班级开设(关联)的课程ID(1-9): ").strip()
        school_id = input("*输入该班级的学校ID(100-109): ").strip()
        teacher_id = input("*输入该班级的授课(关联)讲师的ID帐号: ").strip()
        try:
            course_id = int(course_id)
        except ValueError:
            pass
        classroom = ClassroomStaticCls(class_id,class_name,course_id,school_id,teacher_id)
        new_classroom = classroom.update()
        if new_classroom == 0:
            print("修改成功!")
        elif new_classroom == 1:
            print("修改失败! 无法保存.")
        elif new_classroom == 2:
            print("讲师不存在或讲师ID错误!")
        elif new_classroom == 3:
            print("课程不存在或课程ID错误!")
        elif new_classroom == 4:
            print("班级名字不能为空!")
        elif new_classroom == 5:
            print("班级ID不存在!")
        elif new_classroom == 6:
            print("学校不存在!")
        else:
            print("修改失败!")
        print(classroom.classroom_obj)
    def delete_classroom(self):
        print("删除班级--")
        class_id = input("*请输入要删除的班级编号: ").strip()
        enter = input("确认删除班级编号%s的所有资料？[Y|n]" % class_id)
        if enter == "Y" or enter == "y":
            result = ClassroomStaticCls.delete(class_id)
            if result == 0:
                print("删除成功.")
            else:
                print("找不到班级编号.")









