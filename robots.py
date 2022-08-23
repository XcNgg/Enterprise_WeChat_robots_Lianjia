from cixi_lianjia import spider
from concurrent.futures import ThreadPoolExecutor
import datetime
import gen_excel
from message import *
"""
{'title': '整租·剑兰苑1室1厅南', 
'url': '/zufang/NB1621831088567484416.html', 
'info_list': ['慈溪市-老城区-剑兰苑', 
'58.00㎡',
'南',
'1室1厅1卫', 
'高楼层（6层）'], 
'price': '1500', 
'img_src': 'https://image1.ljcdn.com/110000-inspection/pc1_xmjYZ1Kex.jpg!m_fill,w_250,h_182,l_flianjia_black,o_auto'}
"""

# 多线程爬取
lianjia= spider()
max_page = lianjia.get_max_page()
with ThreadPoolExecutor(10) as f:
    for page in range(1,max_page+1):
        f.submit(lianjia.run, page)

# 发送 开始提示
start()
# 生成excel
excel_data =[]
# 如果当前目录下没有data 这个文件夹则自动创建
if not os.path.exists('./data'):
    os.mkdir('./data')
#对数据中文编排
for data in lianjia.data_list:
    if len(data['info_list'])==5:
        d = {}
        d['标题'] =data['title']
        d['租金'] = data['price']
        d['所在地区'] = data['info_list'][0]
        d['占地大小'] =data['info_list'][1]
        d['朝向'] = data['info_list'][2]
        d['房屋类型'] = data['info_list'][3]
        d['楼层'] = data['info_list'][4]
        d['访问链接'] ="https://nb.lianjia.com"+ data['url']
        d['图片链接'] = data['img_src']
        excel_data.append(d)
# 对数据根据租金进行排序
excel_data.sort(key=lambda x: int(x['租金']))
# 生成Excel文件 并存储
filename = gen_excel.save_excel(excel_data)
print(f'{filename}文件生成成功')





# 对数据进行清洗
temp = []
for da in lianjia.data_list:
    # 如果有范围的价格则直接取最高范围
    if '-' in da['price']:
        da['price'] = da['price'].split('-')[1]
    # 如果价格低于1700 则加入列表
    if int(da['price']) <= 1700:
        temp.append(da)
# 使列表重新赋值
lianjia.data_list = temp

# 根据价格升序
lianjia.data_list.sort(key=lambda x: int(x['price']))
# 只截取前18
lianjia.data_list = lianjia.data_list[:18]
#
for index, d in enumerate(lianjia.data_list):
    # 如果信息列表为5
    # 则按照企业微信腾讯官方给出的模板格式
    if len(d['info_list'])==5:
        data = {
            "msgtype": "template_card",
            "template_card": {
                "card_type": "text_notice",
                "source": {
                    "icon_url": "https://nb.lianjia.com/favicon.ico",
                    "desc": "[链家爬虫] BY XCNGG",
                    "desc_color": 0
                },
                "main_title": {
                    "title": "慈溪房价",
                    "desc": "爬取房价范围 [1000-1700]",
                },
                "emphasis_content": {
                    "title": f"{d['price']}元/月",
                    "desc": "租金",
                },
                "quote_area": {
                    "type": 1,
                    "url":  "https://nb.lianjia.com" + d['url'],
                    "appid": "APPID",
                    "pagepath": "PAGEPATH",
                    "quote_text": f"{d['info_list'][0]}\n"
                                  f"{d['info_list'][4]}"
                },
                "sub_title_text": f"房屋类型: 【{d['info_list'][3]}】\n"
                                  f"房屋面积: 【{d['info_list'][1]}】\n"
                                  f"房屋朝向: 【{d['info_list'][2]}】\n",
                "horizontal_content_list": [
                    {
                        "keyname": "租房标题",
                        "value": d['title']
                    },
                    {
                        "keyname": "图片查看",
                        "value": "点击查看",
                        "type": 1,
                        "url": d['img_src'],
                    },
                ],
                "jump_list": [
                    {
                        "type": 1,
                        "url": "https://nb.lianjia.com" + d['url'],
                        "title": "跳转查看详细"
                    },
                ],
                "card_action": {
                    "type": 1,
                    "url": "https://nb.lianjia.com" + d['url'],
                    "appid": "APPID",
                    "pagepath": "PAGEPATH"
                }
            }
        }
        # 对对应的接口展示模板
        todo 修改为自己的webhook地址
        url = ""  # 机器人的webhook地址
        headers = {'Content-type': 'application/json'}
        result = requests.post(url, headers=headers, json=data)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') , "文本发送情况提示", result.text)

todo 修改为自己的KEY
sendfile(path=f'./data/{filename}.xlsx',key='')
