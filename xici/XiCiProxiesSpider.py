# -*- coding: utf-8 -*-
__author__ = 'KemixKoo'

import urllib3
from bs4 import BeautifulSoup


class XiCiProxiesSipder:
    def __init__(self, region='国内普通'):
        self.__regions = {'国内高匿': 'nn/', '国内普通': 'nt/', '国内HTTPS': 'wn/', '国内HTTP': 'wt/'}

        self.__url = 'http://www.xicidaili.com/' + self.__regions[region]
        self.__header = {}
        self.__header[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'

    def get_proxies(self):
        http = urllib3.PoolManager()
        req = http.request('GET', self.__url, headers=self.__header)
        html_data = req.data.decode('utf-8')
        req.release_conn()

        self.list = []

        contents = BeautifulSoup(html_data, 'html.parser')
        h_ip_list = contents.find('table', id='ip_list')
        if h_ip_list:
            # h_header = h_ip_list.tbody.children[0]

            for h_line in h_ip_list.findAll('tr', recursive=False):
                if h_line.has_attr('class'):  # except header
                    line = {}

                    self.list.append(line)

                    h_line_chilren = h_line.findAll('td', recursive=False)

                    # country
                    h_country = h_line_chilren[0]
                    h_country_img = h_country.img
                    if h_country_img:
                        country = {}
                        line['country'] = country
                        country['pic_uri'] = h_country_img['src']
                        country['name'] = h_country_img['alt']

                    line['ip'] = h_line_chilren[1].string
                    line['port'] = int(h_line_chilren[2].string)

                    # place
                    h_place = h_line_chilren[3]
                    h_place_a = h_place.a
                    if h_place_a:
                        place = {}
                        line['place'] = place
                        place['uri'] = h_place_a['href']
                        place['name'] = h_place_a.string

                    line['connect'] = h_line_chilren[4].string
                    line['type'] = h_line_chilren[5].string

                    # speed
                    h_speed = h_line_chilren[6]
                    h_speed_bar = h_speed.find('div', class_='bar')
                    if h_speed_bar and h_speed_bar['title']:
                        line['speed'] = h_speed_bar['title'][:-1]

                    # time
                    h_time = h_line_chilren[7]
                    h_time_bar = h_time.find('div', class_='bar')
                    if h_time_bar and h_time_bar['title']:
                        line['time'] = h_time_bar['title'][:-1]

                    line['days'] = h_line_chilren[8].string
                    line['update'] = h_line_chilren[9].string

        return self.list

    def save_proxies(self):
        with open('proxies.json', 'w') as f:
            proxies = {}

            http_list = []
            https_list = []
            for one in self.list:
                if float(one['speed']) < 1:
                    type = one['type'].lower()
                    line = str(one['ip'] + ':' + str(one['port']))
                    if 'http' == type:
                        http_list.append(line)
                    if 'https' == type:
                        https_list.append(line)

            if len(http_list) > 0:
                proxies['http'] = http_list
            if len(https_list) > 0:
                proxies['https'] = https_list

            f.write(str(proxies))
            f.flush()


if __name__ == '__main__':
    spider = XiCiProxiesSipder(region='国内HTTPS')
    data = spider.get_proxies()
    spider.save_proxies()

    print len(data)

    import json

    data = json.dumps(data, indent=2)
    print data
