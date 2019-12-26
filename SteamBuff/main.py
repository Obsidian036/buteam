#!/usr/bin/env python
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import requests as rq
import re
import tkinter.font as tkFont
from tkinter.font import Font
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome as Firefox
import time
import threading
from lxml import html as html_parser


class Window(tk.Frame):
    def __init__(self):

        self.select_sentence_index = []
        window = tk.Tk()
        font = Font(family="Courier", size=12, weight='normal')
        # font = tkFont.Font(font='TkDefaultFont')
        window.title('事件链 标注系统')
        window.geometry('1300x860')
        window.geometry('+150+0')
        # window.geometry('+0+0')
        window.resizable(width=False, height=False)
        self.window = window
        self.handlabel_index = 0
        self.hand_descp = []

        self.b_start = tk.Button(window, text='开始干活', width=18, height=1, command=self.starting)
        self.b_start.grid(row=1, column=0, padx=5, pady=5)

        b_exchange = tk.Button(window, text='切换排名', width=18, height=1, command=self.switching)
        b_exchange.grid(row=2, column=0, padx=5, pady=5)

        self.info_text = tk.Text(window, height=1, width=50, bg="White", font=font)
        # self.title_text.grid(row=5, column=1, columnspan =600, sticky = W + E + N + S, padx = 400, pady = 1)
        self.info_text.grid(row=1, column=1)

        self.title_text = tk.Text(window, height=1, width=100, bg="White", font=font)
        # self.title_text.grid(row=5, column=1, columnspan =600, sticky = W + E + N + S, padx = 400, pady = 1)
        self.title_text.grid(row=2, column=1)

        self.result_text = tk.Text(window, height=50, width=100, bg="LightGray", font=font)
        # self.result_text.grid(row=6, column=1, columnspan = 600, sticky = W + E + N + S, padx = 400, pady = 1)
        self.result_text.grid(row=3, column=1)

        self.driver1 = Firefox()
        # self.buff_login = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=1'
        self.buff_login = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num={}&min_price=100&sort_by=price.desc'
        # self.buff_nologin = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num={}&min_price=100'
        self.buff_nologin = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=1'
        self.steam_url = 'https://steamcommunity.com/market/search?appid=730'
        self.steam_url = 'https://steamcommunity.com/market/search?appid=730#p{}_price_desc'
        self.headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'DNT': '1',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        self.time_wati = 5
        self.login = True
        self.huilv = 7
        self.now_num = 0
        self.max_num = 100
        self.result_content = ''
        self.username = ''
        self.password = ''
        try:
            a = open('password.txt', 'r', encoding='utf-8').read().splitlines()
            self.username, self.password = a
        except:
            pass

        # self.username = '15629947209'
        # self.password = 'lv201314'
        self.min_freq = 20

        self.now_steam = 0
        self.max_steam = 400
        # self.get_steam_next()

        self.items = {}
        # self.start_work()
        # self.start_work_steam()

        self.count = [0, 0]
        self.order = 'di'
        self.insert_title()

        self.steam_url = 'https://steamcommunity.com/market/search/render/?' \
                         'query=&start={}&count=10&search_descriptions=0' \
                         '&sort_column=price&sort_dir=desc&appid=730'

    def starting(self):
        self.thread = threading.Thread(target=self.start_work)
        self.thread.setDaemon(True)
        self.thread.start()
        self.b_start['state'] = tk.DISABLED
        self.b_start['text'] = '正在工作'

    def switching(self):
        if self.order == 'di':
            self.order = 'qiu'
        else:
            self.order = 'di'
        self.insert_title()
        self.update_result()

    def do_login(self):

        time.sleep(self.time_wati)
        # self.driver1.find_element_by_xpath('/html/body/div[1]/div/div[3]/ul/li[2]/a').click()
        self.driver1.switch_to.frame(0)
        self.driver1.find_element_by_xpath('//a[@class="tab0"]').click()
        time.sleep(self.time_wati // 2)
        self.driver1.find_element_by_xpath('//input[@id="phoneipt"]').send_keys(self.username)
        time.sleep(self.time_wati // 3)
        self.driver1.find_element_by_xpath('//input[@type="password"][2]').send_keys(self.password)
        time.sleep(self.time_wati // 3)
        # self.driver1.find_element_by_xpath('//input[starts-with(@id, "auto-id")]').send_keys(self.password)
        # time.sleep(self.time_wati)
        while True:

            b = input()
            if b == 'ok':
                break
        self.driver1.switch_to.default_content()
        '''
        while True:
            self.driver1.find_element_by_xpath('//input[@id="phoneipt"]').send_keys(self.username)
            time.sleep(self.time_wati)
            self.driver1.find_element_by_xpath('//input[@type="password"]').send_keys(self.password)
            time.sleep(self.time_wati)
            b = input()
            if b == 'ok':
                break
        '''

    def get_steam_next(self):
        # self.now_num = (self.now_num + 1) % self.max_num + 1
        self.now_steam = (self.now_steam + 1) % self.max_steam

    def start_work(self):
        if self.login:
            self.driver1.get(self.buff_login.format(1))
            self.do_login()
        else:
            self.driver1.get(self.buff_nologin)

        self.driver1.get(self.buff_login.format(self.now_num))

        time.sleep(self.time_wati)
        while True:
            # self.driver1.get(self.buff_login.format(self.now_num))
            page_source = self.driver1.page_source
            root = html_parser.fromstring(page_source)
            lis = root.xpath('//ul[@class="card_csgo"]/li')
            open('res.html', 'w', encoding='utf-8').write(page_source)
            print("buff ", len(lis))
            for li in lis:
                # print(html_parser.tostring(li, pretty_print=True))
                res = [w for w in li.itertext()]
                res = [w.strip('\n ') for w in res]
                # res = [re.sub(r'\n| |￥', '', w) for w in res]
                name, price = res[4], (res[7] + res[8]).strip().replace('￥', '')

                num = int([w.replace('件在售', '') for w in res if '在售' in w][0].replace('+', ''))
                if num < self.min_freq:
                    continue
                if name in self.items:
                    self.items[name].update_buff(float(price), num)
                else:
                    self.count[1] += 1
                    self.init_info()
                    self.items[name] = Item(name, buff_price=price, buff_num=num)
                print(name)

            # if not self.login:
            # self.driver1.find_element_by_xpath('//a[@class="page-link next"]').click()
            if self.now_num > 400:
                self.driver1.get(self.buff_login.format(1))
            else:
                try:
                    time.sleep(self.time_wati * 2)
                    self.driver1.find_element_by_xpath('//a[@class="page-link next"]').click()
                    time.sleep(self.time_wati * 2)
                except:
                    print("wrong" * 20)
                    now_num = 1
                    self.driver1.get(self.buff_login.format(now_num))
                    self.driver1.refresh()

            time.sleep(self.time_wati / 3)
            print(self.steam_url.format(self.now_steam * 100))

            a = self.get_html(self.steam_url.format(self.now_steam * 10))
            if a == '':
                continue
            # a = rq.get(self.steam_url.format(self.now_steam * 10), headers=self.headers)
            try:
                a = (eval(a.replace('true', 'True')))['results_html']
            except:
                time.sleep(self.time_wati / 3)
                self.get_steam_next()
                time.sleep(self.time_wati / 3)
                continue


            page = html_parser.fromstring(a)

            divs = page.xpath(
                '//div[@class="market_listing_row market_recent_listing_row market_listing_searchresult"]')
            sub_link = page.xpath('//a[@class="market_listing_row_link"]')
            print([w.get('href').replace('\\', '') for w in sub_link])

            if len(divs) == 0:
                print("no")
            print("steam num", len(divs))

            for i, div in enumerate(divs):
                text = list(div.itertext())
                text = [w.strip('\n').strip() for w in text]
                if len(text) < 25:
                    continue
                print(text)
                name = text[14]
                num = text[5].replace(',', '')
                price_di = text[9]
                if 'USD' in price_di or '$' in price_di:
                    price_di = float(price_di.replace('$', '').replace('USD', '').replace(',', '').strip())
                    self.huilv = 7
                else:
                    price_di = float(price_di.replace('￥', '').replace('CNY', '').replace(',', '').strip())
                    self.huilv = 1
                price_di = price_di * self.huilv

                sub_url = sub_link[i].get('href').replace('\\', '')
                time.sleep(self.time_wati)
                price_qiu = self.get_steam_detail(sub_url)
                time.sleep(self.time_wati)
                if price_qiu == '':
                    continue

                if name in self.items:
                    self.items[name].update_steam(price_di, price_qiu, num)
                else:
                    self.count[0] += 1
                    self.init_info()
                    self.items[name] = Item(name, steam_price_di=price_di, steam_price_qiu=price_qiu, steam_num=num)

                print(name, num, price_di, price_qiu)

            time.sleep(self.time_wati / 3)
            self.get_steam_next()
            time.sleep(self.time_wati / 3)

            self.update_result()

    def get_html(self, url):
        i = 0
        while i < 3:
            try:
                html = rq.get(url, timeout=5, headers=self.headers).text
                return html
            except rq.exceptions.RequestException:
                i += 1
        return ''

    def get_steam_detail(self, url):
        source = self.get_html(url)
        if source == '':
            return source
        # a = rq.get(url, headers=self.headers)
        # source = a.text
        try:
            id = re.findall(r'Market_LoadOrderSpread\((.+?)\)', source)[0].strip('\n').strip()
        except:
            print("no id")
            return ''
        url = 'https://steamcommunity.com/market/itemordershistogram?country=TW&language=schinese&currency=1&item_nameid={}&two_factor=0'
        url = url.format(id)
        # a = rq.get(url, headers=self.headers)
        a = self.get_html(url)
        if a == '':
            return ''
        a = eval(a)
        a = a['buy_order_summary']
        if '$' in a or 'USD' in a:
            a = re.findall(r'market_commodity_orders_header_promote">(.+?)<', a)[-1].strip('$').replace('USD',
                                                                                                        '').replace(',',
                                                                                                                    '')
            self.huilv = 7
        else:
            a = re.findall(r'market_commodity_orders_header_promote">(.+?)<', a)[-1].strip('￥').replace('CNY',
                                                                                                        '').replace(',',
                                                                                                                    '')
            self.huilv = 1

        return float(a) * self.huilv

    def mainloop(self):
        self.window.mainloop()

    def layout(self, line):
        """
        22, 7 * 6
        :param line:
        :return:
        """
        lengths = [9, 11, 7, 9, 7, 8, 15]
        res = ''
        for i in range(6):
            item = line[i]
            res += (item + ' ' * 7)[:lengths[i]]
        res += line[-1]
        return res

    def insert_title(self):
        lengths = [9, 11, 7, 9, 7, 9, 15]
        line = ['rate_{}', 'steam_{}', 'num', 'buff', 'num', 'time', 'name']
        line = [w.format(self.order) for w in line]
        line = [(w + ' ' * 10)[:k] for w, k in zip(line, lengths)]
        res = ''.join(line)

        self.title_text.delete("0.0", tk.END)
        self.title_text.insert("0.0", res)

    def init_info(self):
        r = 'Steam count: {}, buff count: {}'.format(*self.count)
        self.info_text.delete("0.0", tk.END)
        self.info_text.insert('0.0', r)

    def update_result(self):
        if len(self.items) == 0:
            return
        res = ''
        # d = {k:v for k, v in self.items.items() if v.rate is not None}
        d1 = [(k, v) for k, v in self.items.items() if 'None' not in str(v.rate_qiu)]
        d2 = [(k, v) for k, v in self.items.items() if 'None' in str(v.rate_qiu)]

        if self.order == 'di':
            d1 = sorted(d1, key=lambda x: x[1].rate_di)[::-1]
        else:
            d1 = sorted(d1, key=lambda x: x[1].rate_qiu)
        d2 = sorted(d2, key=lambda x: x[1].update_time)[::-1]
        for item in d1:
            line = item[1].to_str(self.order)
            line = self.layout(line)
            print(line)
            res += line + '\n'

        for item in d2:
            line = item[1].to_str(self.order)
            line = self.layout(line)
            print(line)
            res += line + '\n'

        self.result_text.delete("0.0", tk.END)
        self.result_text.insert("0.0", res)


class Item:
    def __init__(self, name, buff_price=None, steam_price_di=None, steam_price_qiu=None, steam_num=None, buff_num=None):
        self.name = name
        self.buff_price = buff_price
        self.steam_price_qiu = steam_price_qiu
        self.steam_price_di = steam_price_di
        self.buff_time = time.time()
        self.steam_time = time.time()
        self.buff_num = buff_num
        self.steam_num = steam_num
        self.rate_di = 'None'
        self.rate_di = 'None'
        self.update_time = time.time()
        self.update_fold()

    def update_buff(self, price, num):
        self.buff_price = price
        self.buff_time = time.time()
        self.buff_num = num
        self.update_time = time.time()
        self.update_fold()

    def update_steam(self, price_di, price_qiu, num):
        self.steam_price_di = price_di
        self.steam_price_qiu = price_qiu
        self.steam_time = time.time()
        self.update_time = time.time()
        self.steam_num = num
        self.update_fold()

    def update_fold(self):
        try:
            self.rate_di = self.steam_price_di / self.buff_price
            self.rate_qiu = self.steam_price_qiu / self.buff_price
        except:
            self.rate_di = 'None'
            self.rate_qiu = 'None'

    def to_str(self, mode='qiu'):
        tim = max(self.steam_time, self.buff_time)
        steam_price_qiu = self.steam_price_qiu
        steam_price_di = self.steam_price_di
        steam_num = self.steam_num
        buff_price = self.buff_price
        buff_num = self.buff_num

        rate_di = self.rate_di
        rate_qiu = self.rate_qiu
        tim = int(time.time() - tim)
        hour = tim // 3600
        mins = (tim % 3600) // 60
        sec = tim % 60
        tim = '{}:{}:{}'.format(hour, mins, sec)

        try:
            steam_price_di = '{:.2f}'.format(steam_price_di)
            steam_price_qiu = '{:.2f}'.format(steam_price_qiu)
        except:
            pass

        try:
            buff_price = '{:.2f}'.format(buff_price)
        except:
            pass

        try:
            rate_qiu = float(rate_qiu)
            rate_di = float(rate_di)
            rate_qiu = '{:.4f}'.format(rate_qiu)
            rate_di = '{:.4f}'.format(rate_di)
        except:
            pass

        if mode == 'qiu':
            rate = rate_qiu
            steam_price = steam_price_qiu
        else:
            rate = rate_di
            steam_price = steam_price_di

        try:
            res = '{}*p*{}*p*{}*p*{}*p*{:.2f}*p*{}*p*{}'.format(rate, int(steam_price), steam_num, int(buff_price),
                                                                buff_num, tim, self.name)
        except:
            res = '{}*p*{}*p*{}*p*{}*p*{}*p*{}*p*{}'.format(rate, steam_price, steam_num, buff_price, buff_num, tim,
                                                            self.name)
        return res.split('*p*')


if __name__ == '__main__':
    window = Window()
    window.mainloop()
