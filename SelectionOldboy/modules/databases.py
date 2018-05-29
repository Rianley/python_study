#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import pickle

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
datadir = os.path.join(base_dir, 'db')


login_prompt = {"login": "立即登录", "logout":"退出登录"}

user_data = {"user_id": None, "is_authenticated": False, "user_data": None}


class DatabasesCls(object):
    #表相关信息
    tables = (
        'supper', 'schools', 'students', 'teachers', 'courses', 'classroom',
        'student_purchase_course', 'student_study_record', 'student_classroom',
        'teacher_lecture_record', 'student_grade'
    )

    def __init__(self,table):
        super(DatabasesCls, self).__init__()
        self.table = table

    def open(self):
        table_path = os.path.join(datadir, self.table)
        if os.path.exists(table_path):
            with open(table_path, 'rb') as table_:
                data = pickle.loads(table_.read())
            return data

    def save(self,data):
        table_path = os.path.join(datadir, self.table)
        if self.table in self.tables:
            with open(table_path, 'wb') as table_:
                update = table_.write(pickle.dumps(data))
            return update


students_info = {
    'zhangsan': {'student_id': 10001, 'name': 'zhangsan', 'password': '123456',
                  'gender': 'M', 'dob': '1993-09-11', 'phone': '12311113333',
                  'email': 'zhangsan@abc.com', 'enroll_date': '2018-03-22 00:00:00', 'status': 0},
    'user01': {'student_id': 10002, 'name': 'xiaowang', 'password': '123',
                  'gender': 'M', 'dob': '1994-02-21', 'phone': '12311113332',
                  'email': 'xw@abc.com', 'enroll_date': '2018-03-22 00:00:00', 'status': 0}
}

d = {'user01': {2: {'purchase_time': '2018-04-23 17:44:58', 'status': 1, 'grade': 0, 'count': 1}, 1: {'purchase_time': '2018-04-23 17:48:53', 'status': 1, 'grade': '88', 'count': 3}}, 'user02': {2: {'purchase_time': '2018-04-25 09:34:54', 'status': 1, 'grade': 0, "count": 2}, 3: {'purchase_time': '2018-04-25 11:28:33', 'status': 0, 'grade': 0}, 1: {'purchase_time': '2018-04-28 16:20:06', 'status': 1, 'grade': 0, 'count': 2}}}

d2 = {'1801': ['user01'], '1803': ['user02'], '1802': ['user02', 'user01']}


