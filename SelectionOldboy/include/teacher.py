#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls

class TeacherAccountBase(object):
    def __init__(self,id,password,name,phone):
        super(TeacherAccountBase,self).__init__()
        self.id = id
        self.password = password
        self.name = name
        self.phone = phone

#继承上述的父类
class TeacherStaticCls(TeacherAccountBase):
    teacher_table = DatabasesCls("teachers")
    def __init__(self,id,password,name,phone,teacher_school,teacher_title,teacher_salary,teacher_email):
        super(TeacherStaticCls,self).__init__(id,password,name,phone)
        self.teacher_school = teacher_school
        self.teacher_title = teacher_title
        self.teacher_salary = teacher_salary
        self.teacher_email = teacher_email
        self.teacher_obj = {}

    def create(self):
        school_table = DatabasesCls("schools")
        school_list = school_table.open()
        data = self.teacher_table.open()
        if self.id not in data and self.id.isalnum():
            if self.password != "" and self.name != "" and self.phone != "" and self.teacher_title \
                    != "" and self.teacher_salary != "":
                if self.teacher_school in school_list:
                    try:
                        self.teacher_obj["password"] = self.password
                        self.teacher_obj["name"] = self.name
                        self.teacher_obj["phone"] = self.phone
                        self.teacher_obj["school_id"] = self.teacher_school
                        self.teacher_obj["title"] = self.teacher_title
                        self.teacher_obj["salary"] = self.teacher_salary
                        self.teacher_obj["email"] = self.teacher_email
                        data[self.id] = self.teacher_obj
                        self.teacher_table.save(data)
                        return 0   #保存成功
                    except BaseException:
                        return 4   #保存失败
                else:
                    return 3  #学校代码不存在
            else:
                return 2  #账号密码、名字、手机、职务、薪资不能为空
        else:
            return 1  #讲师账号已存在或输入错误

    def update(self):
        school_table = DatabasesCls("schools")
        school_list = school_table.open()
        data = self.teacher_table.open()
        if self.id in data and self.id.isalnum():
            if self.password != "" and self.name != "" and self.phone != "" and self.teacher_title \
                    != "" and self.teacher_salary != "":
                if self.teacher_school in school_list:
                    try:
                        self.teacher_obj["password"] = self.password
                        self.teacher_obj["name"] = self.name
                        self.teacher_obj["phone"] = self.phone
                        self.teacher_obj["school_id"] = self.teacher_school
                        self.teacher_obj["title"] = self.teacher_title
                        self.teacher_obj["salary"] = self.teacher_salary
                        self.teacher_obj["email"] = self.teacher_email
                        data[self.id] = self.teacher_obj
                        self.teacher_table.save(data)
                        return 0   #保存成功
                    except BaseException:
                        return 3   #保存失败
                else:
                    return 3  #学校代码不存在
            else:
                return 2  #账号密码、名字、手机、职务、薪资不能为空
        else:
            return 1  #讲师账号已存在或输入错误

    @classmethod    #修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    def delete(cls,account):
        data = cls.teacher_table.open()
        if account in data:
            try:
                del data[account]
                cls.teacher_table.save(data)
                return 0
            except KeyError:
                pass
        else:
            return 1




