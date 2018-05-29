#/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = 'rianley cheng'
__blog__ ='https://www.cnblogs.com/rianley'
'''
left is too short , I use python !

数据规范化， 正则拆分，结合运算  打印运算表达式及运算步骤
'''
import re,time
from PIL import Image

def math_legal(num):   #判断输入公式是否合法，如包含字符或者特殊字符，做特殊处理
    try:
        num = float(num)
        return True
    except (ValueError,TypeError) as diag:
        pass

def calc_formula(formula):  #替换多余的加减操作
    formula = formula.replace("++", "+")
    formula = formula.replace("+-", "-")
    formula = formula.replace("-+", "-")
    formula = formula.replace("--", "+")
    return formula

def match_calc_formula(parenthesises_formula):  #匹配加减操作符和加减表达式列表
    # 取出圆括号表达式中所有的"+-"号，保存为列表形式，如['-', '+', '+']
    # 用"+-"号作为分隔符，将圆括号中的乘除表达式取出，保存为列表形式，如['9', '2*5/3', '7/3*99/4*2998', '10*568/14']
    parenthesises_formula = re.sub("[()]", "", parenthesises_formula)
    plusminus_operator_list = re.findall("[+-]", parenthesises_formula)
    plusminus_expression_list = re.split("[+-]", parenthesises_formula)
    if plusminus_expression_list[0] == "":
        #圆括号表达式列表中，如果第一个元素为空，则表明第一个元素为一个负数，则"-"号开头，将第一个"-"号合并到列表第一个元素
        plusminus_expression_list[1] = plusminus_operator_list[0] + plusminus_expression_list[1]
        del plusminus_expression_list[0]
        del plusminus_operator_list[0]

    for i, e in enumerate(plusminus_expression_list):
        #处理成正确的结果：['1 * -2', '3 * -5', '6/-3']
        e = e.strip()
        if e.endswith("*") or e.endswith("/"):
            try:
                plusminus_expression_list[i] = plusminus_expression_list[i] + plusminus_operator_list[i] + plusminus_expression_list[i + 1]
                del plusminus_expression_list[i + 1]
                del plusminus_operator_list[i]
            except IndexError as diag:
                pass
    return plusminus_operator_list,plusminus_expression_list

def matching_multiply_divide_operator(plusminus_equations):  #匹配乘除操作符和乘除表达式列表
    operator_list = re.findall("[*/]", plusminus_equations)
    value_list = re.split("[*/]", plusminus_equations)
    return operator_list,value_list

def plus_minus_calc(plusminus_operator_list,plusminus_expression_list):  #加减运算
    '''对运算公式进行加减运算，返回加减结果'''
    plusminus_result = None
    for i, e in enumerate(plusminus_expression_list):
        match = math_legal(e)
        if match == True:
            if plusminus_result:
                if plusminus_operator_list[i - 1] == "+":
                    plusminus_result += float(e)
                elif plusminus_operator_list[i - 1] == "-":
                    plusminus_result -= float(e)
            else:
                plusminus_result = float(e)
        else:
            print("\33[33;0m输入的公式中包含非数字字符!\33[0m")
            print("\33[33;0m尝试运算: %s\33[0m" % e)
            e = re.sub("\D", "", e)
            if e == "": e = 0
            if plusminus_result:
                if plusminus_operator_list[i - 1] == "+":
                    plusminus_result += float(e)
                elif plusminus_operator_list[i - 1] == "-":
                    plusminus_result -= float(e)
            else:
                try:
                    plusminus_result = float(e)
                except ValueError as diag:
                    print("\33[33;1m无效输入！\33[0m")
    return plusminus_result
def multiply_divide_calc(multiply_divide_operator_list,multiply_divide_value_list):  #乘除运算
    '''对运算公式进行乘除运算，返回乘除结果'''
    multiply_divide_result = None
    for i, num in enumerate(multiply_divide_value_list):
        match = math_legal(num)
        if match == True:
            if multiply_divide_result:
                if multiply_divide_operator_list[i - 1] == "*":
                    multiply_divide_result *= float(num)
                elif multiply_divide_operator_list[i - 1] == "/":
                    try:
                       multiply_divide_result /= float(num)
                    except ZeroDivisionError as diag:
                        multiply_divide_result = 0
                        print("\33[33;0m输入的公式中存在除数为0，重新输入！\33[0m")
            else:
                 multiply_divide_result = float(num)
        else:
            print("\33[33;0m输入的公式中存在无法识别的内容!\33[0m")
            print("\33[33;0m尝试为您运算: %s\33[0m" % num)
            num = re.sub("\D", "", num)
            if num == "": num = 1
            if multiply_divide_result:
                if multiply_divide_operator_list[i - 1] == "*":
                    multiply_divide_result *= float(num)
                elif multiply_divide_operator_list[i - 1] == "/":
                    multiply_divide_result /= float(num)
            else:
                try:
                    multiply_divide_result = float(num)
                except ValueError as diag:
                    print("\33[33;1m无效输入！\33[0m")
    return multiply_divide_result
def calculating_priority_formulas(priority_formula):  #计算圆括号表达式
    """"""
    plusminus_operator_list, plusminus_expression_list = match_calc_formula(priority_formula)
    print("-----------")
    print("\33[31;1m步骤\33[0m")
    print(plusminus_operator_list, plusminus_expression_list)
    for index, equations in enumerate(plusminus_expression_list):
        if "*" in equations or "/" in equations:
            """"""
            multiply_divide_operator_list, multiply_divide_value_list = matching_multiply_divide_operator(equations)
            multiply_divide_result = multiply_divide_calc(multiply_divide_operator_list, multiply_divide_value_list)  #取出乘除表达式进行乘除运算
            plusminus_expression_list[index] = multiply_divide_result
    plus_minus_result = plus_minus_calc(plusminus_operator_list, plusminus_expression_list)   #将乘除的结果进行加减运算
    print("%s 运算结果: %s" % (priority_formula, plus_minus_result))
    return plus_minus_result

def start_operation(formula):
    """ 运算主程序入口，对输入的数学公式进行处理，匹配最底层圆括号表达式，并交给乘除函数计算返回结果，替换圆括号表达式"""
    formula = formula.replace(" ", "")    #去掉表达式多余的空格
    formula = calc_formula(formula)  #去掉表达式里重复的"+-"号
    print(formula)
    parenthesises_flag = True
    while parenthesises_flag:
        formula = calc_formula(formula)
        parenthesis_formula = re.search(r"\(([^()]+)\)", formula)
        if parenthesis_formula:
            parenthesis_formula = parenthesis_formula.group()
            parenthesis_calc_result = calculating_priority_formulas(parenthesis_formula)
            formula = formula.replace(parenthesis_formula, str(parenthesis_calc_result))
            print("parenthesis_calc_result: %s" % formula)
        else:
            calc_result = calculating_priority_formulas(formula)
            parenthesises_flag = False
            print("最后的运算结果: \33[31;1m%s\33[0m" % calc_result)

def myCalcMain():
    prompt = '''
请输入你的计算公式, 计算器会将计算结果输出到屏幕上(此处会打印步骤); 退出（exit/quit）
示例公式: 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
'''
    print(prompt)
    while True:
        formula = input("MyCalc> ").strip()
        if formula == "exit" or formula == "quit":
            print('欢迎下次使用，欢迎在3秒后扫描二维码，关注作者博客！更多资讯敬请期待')
            time.sleep(3)
            I = Image.open('blog.png')
            I.show()
            exit("Bye.Bye...")
        elif formula == "":
            continue
        else:
            start_operation(formula)
if __name__ == '__main__':
    myCalcMain()