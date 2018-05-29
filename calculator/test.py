import re

'''
测试文件 作业测试demo
'''
'''
^  匹配开始  
$  匹配行尾  
. 匹配出换行符以外的任何单个字符，使用-m选项允许其匹配换行符也是如此  
[...] 匹配括号内任何当个字符（也有或的意思）  
[^...] 匹配单个字符或多个字符不在括号内  
*  匹配0个或多个匹配前面的表达式  
+  匹配1个或多个前面出现的表达式  
？ 匹配0次或1次前面出现的表达式  
{n} 精确匹配前面出现的表达式的数量  
{n,m} 匹配至少n次到m次  
a | b 匹配a或b  
*？，+？，??,{m,n}? 这样在*，+，？，{m,n} 变成非贪婪模式  
(re) 组正则表达式并及时匹配的文本  
（？imx） 暂时切换上i,m或x震泽表达式的选项，如果括号中，仅该地区受到影响  
(?: re) 组正则表达式而匹配的记住文字  
(?#....) 注释  
(?=re) 指定使用的模式位置，没有一个范围  
(?!re) 使用指定模式取反位置，没有一个范围  
(?<n1>..) 用列表的方式匹配  

 url(r'^abc/(?P<name>\w+/)$',views.cccc), http://127.0.0.1:8000/adfadfasdf213/    得到值adfadfasdf213/
(r"/index/(?P<page>\d*)", home.IndexHandler),
\d 数字[0-9] digit 
\D 非数字 == [^0-9] or [^\d] 
\s 空白字符 
\S 非空白字符 
\w 字母数字下划线 word 
\W 非字母数字下划线

'''
from tkinter import *
import threading
import queue
import time
import random


class GUI(Tk):
    '''class GUI use to create the gui'''

    def __init__(self, queue):
        Tk.__init__(self)
        self.queue = queue
        self.is_game_over = False
        self.canvas = Canvas(self, width=495, height=305, bg='#000000')
        self.canvas.pack()
        self.snake = self.canvas.create_line((0,0),(0,0), fill='#FFFF00', width=10)
        self.food = self.canvas.create_rectangle(0,0,0,0, fill='#00FF00', outline='#00FF00')
        self.point_score = self.canvas.create_text(455, 15, fill='white', text='score:0')
        self.queue_handler()

    def restart(self):
        self.destroy()
        main()

    def queue_handler(self):
        try:
            while True:
                task = self.queue.get(block=False)
                if task.get('game_over'):
                    self.game_over()
                elif task.get('move'):
                    points = [x for point in task['move'] for x in point]
                    self.canvas.coords(self.snake, *points)
                elif task.get('food'):
                    self.canvas.coords(self.food, *task['food'])
                elif task.get('points_score'):
                    self.canvas.itemconfigure(self.point_score,
                                              text='score:{}'.format(task['points_score']))
                    self.queue.task_done()
        except queue.Empty:
            if not self.is_game_over:
                self.canvas.after(100, self.queue_handler)

    def game_over(self):
        self.is_game_over = True
        self.canvas.create_text(220, 150, fill='white',text='Game Over!')
        quitbtn = Button(self, text='Quit', command=self.destroy)
        retbtn = Button(self, text='Resume', command=self.restart)
        self.canvas.create_window(230, 180, anchor=W, window=quitbtn)
        self.canvas.create_window(200, 180, anchor=E, window=retbtn)


class Food():
    '''class Food use to make food'''

    def __init__(self, queue):
        self.queue = queue
        self.make_food()

    def make_food(self):
        x = random.randrange(5, 480, 10)
        y = random.randrange(5, 295, 10)
        self.position = x,y
        self.exppos = x-5,y-5,x+5,y+5
        self.queue.put({'food':self.exppos})

class Snake(threading.Thread):
    '''class Snake use to create snake and response action'''

    def __init__(self, gui, queue):
        threading.Thread.__init__(self)
        self.gui = gui
        self.queue = queue
        self.daemon = True
        self.points_score = 0
        self.snake_points = [(495,55),(485,55),(475,55),(465,55),(455,55)]
        self.food = Food(queue)
        self.direction = 'Left'
        self.start()

    def run(self):
        if self.gui.is_game_over:
            self._delete()
        while not self.gui.is_game_over:
            self.queue.put({'move':self.snake_points})
            time.sleep(0.2)
            self.move()

    def key_pressed(self,e):
        self.direction = e.keysym

    def move(self):
        new_snake_point = self.calculate_new_coordinates()
        if self.food.position == new_snake_point:
            add_snake_point = self.calculate_new_coordinates()
            self.snake_points.append(add_snake_point)
            self.points_score += 1
            self.queue.put({'points_score':self.points_score})
            self.food.make_food()
        else:
            self.snake_points.pop(0)
            self.check_game_over(new_snake_point)
            self.snake_points.append(new_snake_point)

    def calculate_new_coordinates(self):
        last_x,last_y = self.snake_points[-1]
        if self.direction == 'Up':
            new_snake_point = last_x,last_y-10
        elif self.direction == 'Down':
            new_snake_point = last_x,last_y+10
        elif self.direction == 'Left':
            new_snake_point = last_x-10,last_y
        elif self.direction == 'Right':
            new_snake_point = last_x+10,last_y
        return new_snake_point

    def check_game_over(self, snake_point):
        x,y = snake_point[0],snake_point[1]
        if not -5 < x < 505 or not -5 < y < 315 or snake_point in self.snake_points:
            self.queue.put({'game_over':True})


def main():
    q = queue.Queue()
    gui = GUI(q)
    gui.title("贪吃蛇")
    snake = Snake(gui, q)
    gui.bind('<Key-Left>', snake.key_pressed)
    gui.bind('<Key-Right>', snake.key_pressed)
    gui.bind('<Key-Up>', snake.key_pressed)
    gui.bind('<Key-Down>', snake.key_pressed)
    gui.mainloop()


if __name__ == '__main__':
    main()