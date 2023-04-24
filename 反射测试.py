import url
'''
不用反射
import url

def run():
inp = input("请输入您想访问页面的url：  ").strip()
if inp == "login":
    url.login()
elif inp == "logout":
    url.logout()
elif inp == "home":
    url.home()
else:
    print("404")
    
def rep(s: str):
   print(s*10) #打印10次
if __name__ == '__main__':
    run()
'''


def run():
    '''
    用反射调用。
    '''
    inp = input("请输入您想访问页面的url：").strip()
    if not hasattr(url,inp):
        print("没有对应的方法")
        return None
    if inp =="rep":
        #func= setattr(url,inp,"A") 这个是设置一个新的方法和值
        ss =  input("请输入10次重复的字：").strip()
        func = getattr(url, inp)
        #func = getattr(url, inp)(ss) 不能用这个加参数，这个参数是两个函数同名不同参数的区别定位
        func(ss)
    else:
        func = getattr(url, inp)
        func()
    return "OK"

    
if __name__ == '__main__': 
    run()