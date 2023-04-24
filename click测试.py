
import click

@click.command()
@click.option("-i", "--id", required=True, help="input an id")
@click.option("-n", "--num", type=int, help="input  a number", show_default=True)
def main(id, num):
    click.echo(f"your {id=} {num=}")


@click.command()
@click.option('-u', '--user_name', type=str, help='search user_name')
def main2(user_name):
    click.echo(f'search user:{user_name}')
    result = m.get_user_info(user_name) #数据库查询
    try:
        info = f"不好意思人太多了，让您久等了，您的信息来了！\n{'*' * 50}\n用户名: {result.get('user_name')}\n" \
            f"密码: {result.get('user_pwd')}\n登录网站: {result.get('url')}\n{'*' * 50}️\n目前密码唯一的不要修改哦！\n该条消息不用回复了，谢谢。"
    except Exception as e:
        info = "Not Found"
    click.echo(info)

def place(name:str) -> str:
    '''
    输入主业名称
    根据主业名称在的位置返回相应的区域
    没有确定的区域信息,即返回空
    '''
    _dg ="东城、南城、万江、莞城、石碣、石龙、茶山、石排、企石、横沥、桥头、谢岗、东坑、常平、寮步、樟木头、大朗、黄江、清溪、塘厦、凤岗、大岭山、长安、虎门、厚街、沙田、道滘、洪梅、麻涌、望牛墩、中堂、高埗、松山湖"
    dg = _dg.split("、")
    #name =input("请输入主业名称，以确定所在区域：").strip()
    o:str =""
    for p in dg:
        if p in name:
            o = p
            break;
    return o

if __name__ == '__main__':
    dg ="东城、南城、万江、莞城、石碣、石龙、茶山、石排、企石、横沥、桥头、谢岗、东坑、常平、寮步、樟木头、大朗、黄江、清溪、塘厦、凤岗、大岭山、长安、虎门、厚街、沙田、道滘、洪梅、麻涌、望牛墩、中堂、高埗、松山湖"
    dg = dg.split("、")
    inp =input("请输入主业名称，以确定所在区域：").strip()
    o:str =""
    for p in dg:
        if p in inp:
            o = p
            break;
 
    print("主业：%s，所在区域：%s"%(inp,o))
    #main()

