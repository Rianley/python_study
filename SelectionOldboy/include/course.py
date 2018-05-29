#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls

def myisnum(num):
    try:
        float(num)
        return True
    except ValueError:
        if num.isdigit():
            return True
    return False

def myisdate(date):
    try:
        re.search(r'(\d){4}-([0][1-9]|[1][0-2])-([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])',date).group()
        return True
    except AttributeError:
        pass
    return False


class CourseStaticCls(object):
    course_table = DatabasesCls("courses")
    def __init__(self,course_name,course_price,course_period,course_outline,course_id=None):
        super(CourseStaticCls, self).__init__()
        self.course_id = course_id
        self.course_name = course_name
        self.course_price = course_price
        self.course_period = course_period
        self.course_outline = course_outline
        self.course_obj = {}

    def create(self):
        data = self.course_table.open()
        self.course_id = len(data) + 1
        if self.course_name == "":
            return 1  #课程名称不能为空
        elif not myisnum(self.course_price):
            return 2  #课程价格非数字
        else:
            try:
                self.course_obj["name"] = self.course_name
                self.course_obj["price"] = self.course_price
                self.course_obj["period"] = self.course_period
                self.course_obj["outline"] = self.course_outline
                data[self.course_id] = self.course_obj
                self.course_table.save(data)    # 存储
                return 0
            except (KeyError, ValueError) as e:
                return 3  #保存失败

    def update(self,course_id):
        data = self.course_table.open()
        if course_id in data:
            if self.course_name == "":
                return 2  #课程名称不能为空
            elif not myisnum(self.course_price):
                return 3  #课程价格非数字
            else:
                try:
                    self.course_obj["name"] = self.course_name
                    self.course_obj["price"] = self.course_price
                    self.course_obj["period"] = self.course_period
                    self.course_obj["outline"] = self.course_outline
                    data[course_id] = self.course_obj
                    self.course_table.save(data)
                    return 0
                except (KeyError, ValueError) as e:
                    return 4  #保存失败
        else:
            return 1   #课程ID不存在

    @classmethod           #修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    def delete(cls,course_id):
        data = cls.course_table.open()
        if course_id in data:
            try:
                del data[course_id]
                cls.course_table.save(data)
                return 0
            except KeyError:
                pass
        else:
            return 1
