
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/9
# @Author  : Fitch
# @File    : smzdm_web_sign.py
# @Software: PyCharm
# smzdm_cookies 环境变量名称多个cookie请用@连接，例：cookie1@cookie2
# 1、什么值得买web端cookie获取方法
# 首先使用chrome浏览器，访问什么值得买官网， 登陆账号
# Windows系统可按 F12 快捷键打开开发者工具, Mac 快捷键 option + command + i
# 选择开发者工具Network，刷新页面 ,选择第一个www.smzdm.com, 找到Requests Headers里的Cookie。

'''
cron:  0 6 * * * smzdm_web_sign.py
new Env('什么值得买web签到');
'''
import requests,os,json

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://www.smzdm.com/',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
    """
    对请求 盖乐世社区 返回的数据进行进行检查
    1.判断是否 json 形式
    """
    def __json_check(self, msg):

        try:
            result=msg.json()
            return True
        except Exception as e:
            print(f'Error : {e}')
            return False

    """
    起一个什么值得买的，带cookie的session
    cookie 为浏览器复制来的字符串
    :param cookie: 登录过的社区网站 cookie
    """
    def load_cookie_str(self, cookies):
        self.session.headers['Cookie'] = cookies

    """
    签到函数
    """
    def checkin(self):
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

if __name__ == '__main__':
    sb = SMZDM_Bot()
    smzdm_cookies = os.getenv("smzdm_cookies") #获取环境变量

    # smzdm_cookies ='__ckguid=CjA49yNCqwe7Pi7QfAPBQi7; device_id=213070643316529226901726671dcb145f0fb8df61432b7086955d4e2c; homepage_sug=d; r_sort_type=score; sajssdk_2015_cross_new_user=1; __jsluid_s=2a4e88d3a1a676a6fa4a491b5a5849c2; sess=AT-yyCOS3zK+5zGMgniIaHAYOvl730ni9S7bh+QCF3+VwGdi25yqV3VPxYxoV1y2e7vkh0RsOp5US5HKwFBmsuSfsWtK7ETBFBos4zmwNTeYw3qX4ddsqR4pVz8; user=user:4210526591|4210526591; smzdm_id=4210526591; DISABLE_APP_TIP=1; _zdmA.uid=ZDMA.OYUcjumnA.1652958595.2419200; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1652922699,1652958596; smzdm_user_view=CA4C24A3D73B6BC6FF534EB75848E555; smzdm_user_source=89ACB723A5431F5FADD8BF8F158E5499; sensorsdata2015jssdkcross={"distinct_id":"4210526591","first_id":"180d9deb33233b-0a3d0edba00e73-14333270-2073600-180d9deb333159","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$latest_landing_page":"https://www.smzdm.com/"},"$device_id":"180d9deb33233b-0a3d0edba00e73-14333270-2073600-180d9deb333159"}; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1652958611'
    datas = smzdm_cookies.split('@')
    for cookie in datas:
        sb.load_cookie_str(cookie.encode("utf-8"))
        res = sb.checkin()
        if(res['error_code'] != '0'):
            print(res['error_msg'])
        else:
            print('签到执行完毕')
        print('返回信息:', res)
