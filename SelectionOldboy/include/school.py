#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from modules.databases import DatabasesCls

class SchoolStaticCls(object):
    school_table = DatabasesCls("schools")
    def __init__(self, school_code, school_name, school_city):
        super(SchoolStaticCls, self).__init__()
        self.school_code = school_code
        self.school_name = school_name
        self.school_city = school_city
        self.school_obj = {}

    def create(self):
        data = self.school_table.open()
        if self.school_code not in data and self.school_code.isdigit():
            if self.school_name != "" or self.school_city != "":
                try:
                    self.school_obj["name"] = self.school_name
                    self.school_obj["city"] = self.school_city
                    data[self.school_code] = self.school_obj
                    self.school_table.save(data)
                    return 0
                except (KeyError, ValueError) as e:
                    return 1
            else:
                return 2
        else:
            return 3

    def update(self):
        data = self.school_table.open()
        if self.school_code in data:
            if self.school_name != "" or self.school_city != "":
                try:
                    self.school_obj["name"] = self.school_name
                    self.school_obj["city"] = self.school_city
                    data[self.school_code] = self.school_obj
                    self.school_table.save(data)
                    return 0
                except (KeyError, ValueError) as e:
                    return 1
            else:
                return 2
        else:
            return 3