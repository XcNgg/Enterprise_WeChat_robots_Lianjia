# encoding:utf-8
# !/usr/bin/python3
# @AUTHOR : XcNgg



import requests
import time
import os
from copy import copy
from urllib3 import encode_multipart_formdata


# 初步 message
def start():
    # 仅用于告知爬虫已经开始
    data = {
        "msgtype": "text",
        "text": {
            "content": "链家慈溪爬虫 展示低价前18房价\n"
                    f"开始时间戳 【{time.time()}】"
        }
    }
    # TODO 机器人的webhook地址
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=TODO 机器人的webhook地址"
    headers = {'Content-type': 'application/text'}
    r = requests.post(url=url,headers=headers,json=data)
    print(r.text)


# file_path: e.g /root/data/test_file.xlsx
# 如果D:\\windows\\ 下面file_name的split需要调整一下
# upload_file 是为了生成 media_id， 供消息使用
def upload_file(file_path, wx_upload_url):
    # 上传文件
    file_name = file_path.split("/")[-1]
    with open(file_path, 'rb') as f:
        length = os.path.getsize(file_path)
        data = f.read()
    headers = {"Content-Type": "application/octet-stream"}
    params = {
        "filename": file_name,
        "filelength": length,
    }
    file_data = copy(params)
    file_data['file'] = (file_path.split('/')[-1:][0], data)
    encode_data = encode_multipart_formdata(file_data)
    file_data = encode_data[0]
    headers['Content-Type'] = encode_data[1]
    r = requests.post(wx_upload_url, data=file_data, headers=headers)
    media_id = r.json()['media_id']
    return media_id


def sendfile(path,key): # # 这个地方传入key
    # 发送文件
    wx_api_key = key
    wx_upload_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={}&type=file".format(wx_api_key)
    wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(wx_api_key)
    # # upload_file 是为了生成 media_id， 供消息使用
    media_id = upload_file(path, wx_upload_url)
    #
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    # 发送文件
    requests.post(
        url=wx_url,headers=headers, json=data)
    print("文件发送成功!")





