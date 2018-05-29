# Author:rianley cheng

from core.atm import atm
from core.cart import cart

#此处调用atm
def atm_init():
    atm_obj = atm()
    while True:
        print('万恶的分割线'.center(50, '-'))
        for index, v in enumerate(atm_obj.operation):
            print(index, v)
        while True:
            choice = input('请选择你的操作，输入序号即可:').strip()
            if choice == 'q': return True
            if not choice.isdigit() or int(choice) >= len(atm_obj.dict_list):
                print('输入有误')
                continue
            choice = int(choice)
            break
        print(('%s' % atm_obj.operation[choice]).center(50, '-'))
        res = atm_obj.dict_list[choice]()
        while not res:
            res = atm_obj.dict_list[choice]()
    return True
#此处调用商城
def cart_init():
    cart_obj = cart()
    while True:
        print('邪恶的分割线'.center(50, '-'))
        for index, v in enumerate(cart_obj.operation):
            print(index, v)
        while True:
            choice = input('请选择你的操作（对应序号即可）：').strip()
            if choice == 'q': return True
            if not choice.isdigit() or int(choice) >= len(cart_obj.operate_func):
                print('输入有误')
                continue
            choice = int(choice)
            break
        print(('%s' % cart_obj.operation[choice]).center(50, '-'))
        res = cart_obj.operate_func[choice]()
        while not res:
            res = cart_obj.operate_func[choice]()

    return True



def index():
    place=['银行（ATM）','商城（购物）']
    place_func=[atm_init,cart_init]
    while True:
        print('正义的分割线'.center(50, '-'))
        print('序号','去处')
        for index,v in enumerate(place):
            print(index,v)
        while True:
            choose = input('请选择你的去处（输入序号即可）：').strip()
            if choose=='q':return True
            if choose and choose.isdigit() and int(choose)<len(place):
                choose=int(choose)
                break
            print('在乱输入，劳资打死你个龟儿子@！')
        print()
        print(('%s' % place[choose]).center(50, '-'))
        print()
        res = place_func[choose]()
        while not res:
            res = place_func[choose]()


#开始

#用户分->银行用户和商城用户，有个功能：商城用户绑定信用卡功能，可直接结算购物车，1
# ，想想还有些复杂,对象换成用户就好。

index()

