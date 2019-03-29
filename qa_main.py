#!/usr/bin/env python3
# coding: utf-8
# File: qa_based_on_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 19-3-29

import urllib.request
from urllib.parse import quote_plus
import json

class QA:
    def __init__(self):
        self.base_api = 'http://39.106.1.94:8080/api/search/'
        self.copyright = '广州数据地平线科技有限公司'
        self.use_with_comercial = 'forbidden'
        self.contact_mail = 'mkt@datahorizon.cn' or 'lhy_in_blcu@126.com'
        self.demo_address = 'http://39.106.1.94:8080'
        return

    '''获取搜索页'''
    def get_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        return html

    '''获取数据'''
    def get_data(self, event):
        good_effects = {}
        bad_effects = {}
        url = self.base_api + quote_plus(event)
        data = json.loads(self.get_html(url))
        item = data['msg']
        effects = item['influence']
        for effect in effects:
            e = effect[0]
            e_senti = effect[1]
            if e_senti > 0:
                good_effects[e] = e_senti
            else:
                bad_effects[e] = e_senti

        return good_effects, bad_effects

    '''问答'''
    def qa_main(self, event):
        good_effects, bad_effects = self.get_data(event)
        return good_effects, bad_effects


if __name__ == '__main__':
    handler = QA()
    while 1:
        event = input('请输入一个事件：').strip()
        good_effects, bad_effects = handler.qa_main(event)
        if good_effects:
            print('1) %s可能带来的有利影响有:'%event)
            print('\n'.join(list(good_effects.keys())[:20]))
        if bad_effects:
            print('2) %s可能带来的不利影响有:'%event)
            print('\n'.join(list(bad_effects.keys())[:20]))
        if not good_effects and not bad_effects:
            print('sorry，目前还预测不出来.')

