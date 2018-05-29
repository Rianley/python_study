#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls


class ClassroomStaticCls(object):
    classroom_table = DatabasesCls("classroom")
    def __init__(self,class_id,class_name,course_id,school_id,teacher_id):
        super(ClassroomStaticCls, self).__init__()
        self.class_id = class_id
        self.class_name = class_name
        self.course_id = course_id
        self.school_id = school_id
        self.teacher_id = teacher_id
        self.classroom_obj = {}


    def create(self):
        school_table = DatabasesCls("schools")
        course_table = DatabasesCls("courses")
        teacher_table = DatabasesCls("teachers")
        class_data = self.classroom_table.open()
        course_data = course_table.open()
        school_data = school_table.open()
        teacher_data = teacher_table.open()
        if self.class_id not in class_data and self.class_id.isdigit():
            if self.class_name != "":
                if self.course_id in course_data:
                    if self.school_id in school_data:
                        if self.teacher_id in teacher_data:
                            try:
                                enroll_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                self.classroom_obj["class_name"] = self.class_name
                                self.classroom_obj["course_id"] = self.course_id
                                self.classroom_obj["teacher_id"] = self.teacher_id
                                self.classroom_obj["school_id"] = self.school_id
                                self.classroom_obj["enroll_date"] = str(enroll_date)
                                class_data[self.class_id] = self.classroom_obj
                                self.classroom_table.save(class_data)
                                return 0   #保存成功
                            except BaseException:
                                return 1   #保存失败
                        else:
                            return 2   #讲师ID不存在
                    else:
                        return 6   #学校不存在
                else:
                    return 3   #课程ID不存在
            else:
                return 4   #班级名字为空
        else:
            return 5   #班级ID已存在或为空

    def update(self):
        school_table = DatabasesCls("schools")
        course_table = DatabasesCls("courses")
        teacher_table = DatabasesCls("teachers")
        class_data = self.classroom_table.open()
        course_data = course_table.open()
        school_data = school_table.open()
        teacher_data = teacher_table.open()
        if self.class_id in class_data:
            if self.class_name != "":
                if self.course_id in course_data:
                    if self.school_id in school_data:
                        if self.teacher_id in teacher_data:
                            try:
                                enroll_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                self.classroom_obj["class_name"] = self.class_name
                                self.classroom_obj["course_id"] = self.course_id
                                self.classroom_obj["teacher_id"] = self.teacher_id
                                self.classroom_obj["school_id"] = self.school_id
                                self.classroom_obj["enroll_date"] = str(enroll_date)
                                class_data[self.class_id] = self.classroom_obj
                                self.classroom_table.save(class_data)
                                return 0  # 保存成功
                            except BaseException:
                                return 1  # 保存失败
                        else:
                            return 2  # 讲师ID不存在
                    else:
                        return 6  # 学校不存在
                else:
                    return 3  # 课程ID不存在
            else:
                return 4  # 班级名字为空
        else:
            return 5  # 班级ID不存在

    @classmethod  #修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    def delete(cls, class_id):
        data = cls.classroom_table.open()
        if class_id in data:
            try:
                del data[class_id]
                cls.classroom_table.save(data)
                return 0
            except KeyError:
                pass
        else:
            return 1



