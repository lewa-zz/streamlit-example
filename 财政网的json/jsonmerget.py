#!/usr/bin/python3
# -*- coding: utf-8 -*-

#可以使用Python的`extend()`方法将两个JSON数据的"data"字段中的内容进行合并，示例代码如下：
def json_data_merge(json1,json2):
    '''
    合并Json中的DATA项
    输入:
        输入原始JSON数据
        json1 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}'
        json2 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 3, "name": "王五"}, {"id": 4, "name": "赵六"}]}'
    输出:   
        返回合并后的格式化的JSON
    输出结果为：
    {"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}, {"id": 3, "name": "王五"}, {"id": 4, "name": "赵六"}]}
    可以看到，两个JSON数据中的"data"字段中的内容已经被合并成一个新的JSON数组。
    Created by https://GPTGO.ai
    '''
    import orjson

    # 解析JSON数据,将json对象转化为dict对象
    data1 = orjson.loads(json1)
    data2 = orjson.loads(json2)

    # 合并数据
    data1["data"].extend(data2["data"])

    #们用到了json库的dumps方法，将Python对象转化为Json对象
    #json_data = json.dumps(data1, indent=2, separators=(",", " = "))
    json_data = orjson.dumps(data1, option=orjson.OPT_INDENT_2).decode()
    return json_data

json1 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}'
json2 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 3, "name": "王五"}, {"id": 4, "name": "赵六"}]}'

print(json_data_merge(json1,json2))