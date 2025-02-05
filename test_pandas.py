import openpyxl
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
import pyecharts
from pandas import DataFrame
import pandas as pd
import os


def read_excel():
    '''
    pandas读excel
    read_excel的原型：read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None)

    io：excel文件，如果命名为中文，在python2.7中，需要使用decode()来解码成unicode字符串，例如： pd.read_excel('示例'.decode('utf-8))
    sheet_name：返回指定的sheet，如果将sheet_name指定为None，则返回全表，如果需要返回多个表，可以将sheet_name指定为一个列表，例如['sheet1', 'sheet2']
    header：指定数据表的表头，默认值为0，即将第一行作为表头。
    usecols：读取指定的列，例如想要读取第一列和第二列数据：pd.read_excel("example.xlsx", sheet_name=None, usecols=[0, 1])

    '''
    file_path = r'/home/rico/桌面/task.xlsx'
    # sheet_name不指定时默认返回全表数据
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=0)

    # 打印表数据，如果数据太多，会略去中间部分#
    # print(df)
    # 打印列标题,即表头
   # print(df.columns)
    total_rows = len(df)
    print('总数:{0} 行数{1}', format(df.index.size), str(total_rows))

    # print(df.head)
    # print(df.index)

    # 显示项目名称列
    # print(df["项目名称"])
    # 显示项目名称第一条数据,
    # print(df["prjname"][0])
    '''
    # 描述数据
    # pandas有两个核心数据结构 Series和DataFrame，分别对应了一维的序列和二维的表结构。
    # 而describe()函数就是返回这两个核心数据结构的统计变量。其目的在于观察这一系列数据
    # 的范围、大小、波动趋势等等
    统计值变量说明：
            count：数量统计，此列共有多少有效值
            unipue：不同的值有多少个
            std：标准差
            min：最小值
            25%：四分之一分位数
            50%：二分之一分位数
            75%：四分之三分位数
            max：最大值
            mean：均值
    '''
    # print(df.describe())


def write_excel():
    '''
    写一个全新的文件也很简单：
    '''
    data = {'name': ['zs', 'ls', 'ww'], 'age': [
        11, 12, 13], 'gender': ['man', 'man', 'woman']}
    df = DataFrame(data)
    df.to_excel('new.xlsx')


def insert_excel():
    '''
    pandas增删Excel
    当需要增加一行时或一列时，可以使用下面的方法：
    新增行：df.loc[row_index] = [val1, val2, val3]
    新增列：df[colo_name] = None
    还是以上述文件为例，代码如下：
    '''
    # 新增一行
    # df.loc[6] = [5, 'Eric', 'male', 20, '2021-5-18']

    # 新增一列

    # df['favorite'] = None

    # 写入数据文件
    # DataFrame(df).to_excel(file_path, sheet_name='Sheet1', index=False, header=True)


def test_pyecharts2():
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.globals import ThemeType

    list2 = [
        {"value": 12, "percent": 12 / (12 + 3)},
        {"value": 23, "percent": 23 / (23 + 21)},
        {"value": 33, "percent": 33 / (33 + 5)},
        {"value": 3, "percent": 3 / (3 + 52)},
        {"value": 33, "percent": 33 / (33 + 43)},
    ]

    list3 = [
        {"value": 3, "percent": 3 / (12 + 3)},
        {"value": 21, "percent": 21 / (23 + 21)},
        {"value": 5, "percent": 5 / (33 + 5)},
        {"value": 52, "percent": 52 / (3 + 52)},
        {"value": 43, "percent": 43 / (33 + 43)},
    ]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([1, 2, 3, 4, 5])
        .add_yaxis("product1", list2, stack="stack1", category_gap="50%")
        .add_yaxis("product2", list3, stack="stack1", category_gap="50%")
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
        .render("stack_bar_percent.html")
    )


'''
实现追加或者覆盖数据
data:DataFramek类型数据
excelname:工作簿名（注意路径！！！）
sheetname:表名
insert_type：w 或者 a+      （当然可以自己定义啦）
'''


def append_excel(data, excelname, sheetname, insert_type):
    original_file = pd.DataFrame(pd.read_excel(
        excelname, sheet_name=sheetname))  # 读取原数据文件和表
    original_row = original_file.shape[0]  # 获取原数据的行数
    if insert_type == 'w':  # 选择写入excel数据方式，w为覆盖模式，a+为追加模式
        startrow = 1
    elif insert_type == 'a+':
        startrow = original_row + 1
    book = openpyxl.load_workbook(excelname)
    writer = pd.ExcelWriter(excelname, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    # 将data数据写入Excel中
    data.to_excel(writer, sheet_name=sheetname,
                  startrow=startrow, index=False, header=False)
    # writer.save()


def json_to_excel(file: str):
    fr = open(file, 'r', encoding='utf-8')
    json_info = fr.read()
    df = pd.read_json(json_info)
    # df.to_csv('json_info.csv', index=False, columns=["mac", "timestamp", "volt", "temp", "acc", "sampletime"])
    df.to_excel("jsonExcel.xlsx")
    print(df)
    # print(df.mac)


def json_to_excel2(fn: str):
    import json
    import os
    import pandas as pd
    from pandas.io.json import json_normalize

    file = open(fn, "r", encoding='utf-8')
    text = file.read()
    text = json.loads(text)
    df = pd.json_normalize(text, 'data', ['msg', 'code'])
    df.to_excel("jsonExcel.xlsx", encoding='utf-8')


if __name__ == "__main__":
    # read_excel()
    file = r"财政网的json/selectInfoMoreChannel-dg.json"
    # test_pyecharts2()
    json_to_excel2(file)  # 记得传入参数哦
