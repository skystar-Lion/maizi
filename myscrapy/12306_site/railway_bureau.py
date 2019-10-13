#-*- coding=utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
from time import sleep
from public import chinese_str,http_get



def station_page(url):
    response = http_get(url)
    p = BeautifulSoup(response, 'lxml')
    
    station_list = []
    stations = p.select('.tb > tr, .tb > tbody > tr')[2:]
    for st in stations:
        s = st.find_all('td')
        station = {}
        station['name'] = s[0].text
        station['address'] = s[1].text
        if s[2].text:
            station['aboard'] = s[2].text
        else:
            station['aboard'] = "x"
        if s[3].text:
            station['luggage'] = s[3].text
        else:
            station['luggage'] = "x"
        if s[4].text:
            station['package'] = s[4].text
        else:
            station['package'] = "x"
        station_list.append(station)
    return station_list



if __name__ == '__main__':
    url = 'http://www.12306.cn/mormhweb/kyyyz/'
    response = http_get(url)
    b = BeautifulSoup(response, 'lxml')
    rail_bureau = b.select('#secTable > tbody > tr > td')
    rail_station = b.select('.submenu_bg > a[title="客运站数据(车站)"]')
    rail_multiplicative_drop = b.select('.submenu_bg > a[title="客运站数据(乘降所)"]')
    #f = open('rail_bureau.txt', 'w')
    for i in range(len(rail_bureau)):
        print(rail_bureau[i].text + ':')
        rail_station[i] = url + rail_station[i].get('href').replace('./', '')
        rail_multiplicative_drop[i] = url + rail_multiplicative_drop[i].get('href').replace('./', '')
        print("车站：", rail_station[i])
        station_info = station_page(rail_station[i])
        #print(station_info)
        print("---车站途经站点信息---")
        for info in station_info:
            #print(info)
            print("站名: {} | 车站地址: {} | 旅客乘降: {} | 行李:{} | 包裹:{}".
                format(chinese_str(info['name'], 20, 'left'), chinese_str(info['address'], 70, 'left'), 
                    chinese_str(info['aboard'], 3, 'left'), chinese_str(info['luggage'], 3, 'left'), chinese_str(info['package'], 3, 'left')))
        
        print("乘降所：", rail_multiplicative_drop[i])
        station_info = station_page(rail_multiplicative_drop[i])
        print("---乘降所途经站点信息---")
        for info in station_info:
            #print(info)
            print("站名: {} | 车站地址: {} | 旅客乘降: {} | 行李:{} | 包裹:{}".
                format(chinese_str(info['name'], 20, 'left'), chinese_str(info['address'], 70, 'left'),
                    chinese_str(info['aboard'], 3, 'left'), chinese_str(info['luggage'], 3, 'left'), chinese_str(info['package'], 3, 'left')))
        
        


