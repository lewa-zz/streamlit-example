类的方法

    # @classmethod
    # def from_dict(cls, request_dict):
    #     for key, value in request_dict.items():
    #         if isinstance(value, bytes):  # 反序列化 如item
    #             request_dict[key] = utils.tools.loads_obj(value)

    #     return cls(**request_dict)

    # def copy(self):
    #     return self.__class__.from_dict(copy.deepcopy(self.to_dict))





#amo      = int(re.findall(r'\d+(\.\d+)?',page_amo)[0]
    i=0
    j=1
    #循环取出记录,打开页面.
    while i < rec_total:
    #for j in range(0,page_amo):
        #每页的记录 id为procurementAnnouncementShowList下级的li中的a标签
        #li = page.locator('//*[@id="procurementAnnouncementShowList"]/li/a')
        li = page.locator('#procurementAnnouncementShowList').locator("a")
        #print(li.text_content())


        #每页做完,点下一页继续.
        #ID为pagination下面的<li>></li> text是精准,不用has_text
        print("记录i: %d , 第J页 is %d"%(i,j))
        #if j <= page_amo-1: #最后一页不用点
        if i < rec_total: 
            page.locator('#pagination').locator('li:text(">")').click()
            page.wait_for_timeout(2000)
            #page.wait_for_load_state()
            j += 1


def test_normalize():
    json_obj = {
        'school': 'ABC primary school',
        'location': 'London',
        'ranking': 2,
        'info': {
            'president': 'John Kasich',
            'contacts': {
                'email': {
                    'admission': 'admission@abc.com',
                    'general': 'info@abc.com'
                },
                'tel': '123456789',
            }
        }
    }
    pd.json_normalize(json_obj)




class TabBa(BaseModel):
    id = BigAutoField()
    data_id = CharField(null=True)
    add_time = CharField(null=True)
    apply_organ = CharField(null=True)
    begin_date = DateField(null=True)
    expiry_date = DateField(null=True)
    finish_date = DateField(null=True)
    full_name = CharField(null=True)
    has_start = IntegerField(null=True)
    is_validity = CharField(null=True)
    note = CharField(null=True)
    over_date = DateField(null=True)
    place = CharField(null=True)
    project_name = CharField(null=True)
    proof_or_serial_code = CharField(null=True)
    scope = TextField(null=True)
    sfjz = CharField(null=True)
    state_flag_name = CharField(null=True)
    submit_date = CharField(null=True)
    total_invest = IntegerField(null=True)
    update_time = CharField(null=True)
    

        # self.page.get_by_role("link", name="更多>").first.click()
        # self.page.get_by_role("combobox").select_option("441900")
        # self.page.get_by_role("button", name="查询").click()
        # self.page.wait_for_load_state("networkidle")
        # print("++++++++++")
        # self.page.pause()
        # self.page.get_by_role("button", name="查询").click()
        # self.page.get_by_role("button", name="查询").click()
        # self.page.get_by_role("button", name="查询").click()
        # self.page.get_by_role("definition").filter(has_text="2304-441900-04-01-254812 东莞市茶山镇塘角水围花园新村别墅住宅区雨污分流改造工程 办结（通过） 2023-04-17 详情").get_by_role("link", name="详情").click()
        # self.page.get_by_role("cell", name="项目为东莞市茶山镇塘角水围花园新村别墅住宅区雨污分流改造工程：项目占地面积11330平方米，建筑面积2125平方米。机械锯混凝土地面缝、建筑排水立管改造、拆除和破除巷道路面、埋地接驳排水管、塑料管（污水接驳管）,其中（PVC-U）管DN150共122米，（PVC-U）管DN100共4810米。").click()
        # self.page.get_by_role("cell", name="45万元").click()
        # self.page.get_by_role("button", name="返回列表").click()
        # self.page.get_by_text("9545").click()
        # self.page.get_by_text("637").click()
        # self.page.get_by_text("共637页共9545条记录当前第1页").click()
        # self.page.get_by_text("下一页").click()
        # self.page.get_by_text("下一页").click()
        # self.page.get_by_role("definition").filter(has_text="2304-441900-04-01-838783 东城街道 温塘社区温塘砖窑一横路23号60.5kW户用分布式光伏发电项目 办结（通过） 2023-04-14 ").get_by_role("link", name="详情").click()
        # self.page.get_by_text("项目信息").click()
        # self.page.get_by_role("button", name="返回列表").click()
        # self.page.locator("a").filter(has_text="公示信息").click()
        # self.page.locator("a").filter(has_text="公示信息").click()
        # self.page.get_by_text("办理结果公示").click()
        # self.page.get_by_text("项目公示").first.click()
        # self.page.get_by_role("link", name="更多>").nth(1).click()
        # self.page.get_by_role("combobox").select_option("441900")
        # self.page.get_by_role("button", name="查询").click()
        # self.page.get_by_role("button", name="查询").click()
        # self.page.get_by_role("button", name="返回列表").click()
        # self.page.get_by_role("link", name="更多>").nth(2).click()
        # self.page.get_by_role("combobox").select_option("441900")
        # self.page.get_by_role("button", name="查询").click()