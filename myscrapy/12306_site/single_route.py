# -*- coding=utf-8 -*-

from public import chinese_str,https_get
import json
import datetime


def train_stop(train_no, from_telecode, to_telecode, date):
    url_format = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode={}&to_station_telecode={}&depart_date={}'
    url = url_format.format(train_no, from_telecode, to_telecode, date)
    #print("途经站点：", url)
    response = https_get(url)
    data = json.loads(response)
    #print(data)
    if not data['data']:
        print("data['data'] is empty")
        return -1
    else:
        stop_info = data['data']['data']
    print("途经站点：")
    for stop in stop_info:
        print("{:<2s} | {} | {:<5s} | {:<5s} | {:<6s}".format(stop['station_no'], chinese_str(stop['station_name'], 15, 'left'),
            stop['arrive_time'], stop['start_time'], stop['stopover_time']))


def train_price(train_no, from_no, to_no, seat_type, date):
    url_format = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'
    url = url_format.format(train_no, from_no, to_no, seat_type, date)
    #print("票价:",url)
    response = https_get(url)
    data = json.loads(response)
    if not data['data']:
        print("data['data'] is empty")
        return -1
    else:
        price_info = data['data']
    price = {}

    if 'A9' in price_info:
        price['A9'] = price_info['A9']
    else:
        price['A9'] = '--'
    if 'P' in price_info:
        price['P'] = price_info['P']
    else:
        price['P'] = '--'
    if 'M' in price_info:
        price['M'] = price_info['M']
    else:
        price['M'] = '--'
    if 'O' in price_info:
        price['O'] = price_info['O']
    else:
        price['O'] = '--'
    if 'A6' in price_info:
        price['A6'] = price_info['A6']
    else:
        price['A6'] = '--'
    if 'A4' in price_info:
        price['A4'] = price_info['A4']
    else:
        price['A4'] = '--'
    if 'A3' in price_info:
        price['A3'] = price_info['A3']
    else:
        price['A3'] = '--'
    if 'A2' in price_info:
        price['A2'] = price_info['A2']
    else:
        price['A2'] = '--'
    if 'A1' in price_info:
        price['A1'] = price_info['A1']
    else:
        price['A1'] = '--'
    print("票价： {:<10}|{:<10}|{:<10}|{:<10}|{:<15}|{:<10}|{:<10}|{:<10}|{:<10}".format(price['A9'], price['P'], 
        price['M'], price['O'], price['A6'], price['A4'], price['A3'], price['A2'], price['A1']))


def train_num(from_station, to_station, date):
    #这里想查询2017-03-18，从北京西BXP到西安XAY的车票
    url_format = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT"
    url = url_format.format(date, from_station, to_station)
    #print("车次：",url)
    response = https_get(url)
    #print(response)
    datas = json.loads(response)
    if not datas['data']:
        print("datas['data'] is empty")
        return -1
    for Left_N in datas['data']:
        """
        #出发站，到达站的站名，站编号，站次代码
        data['station_train_code']:"G651"  ;车次
        data['train_no'] ;列车编号
        data['start_station_name']:"北京西" ;
        data['start_station_telecode']：BXP
        data['from_station_no']: 01       
        data['to_station_name']:"西安北" ;
        data['to_station_telecode']:EAY
        data['to_station_no']:13
        data['seat_types'] ;座位类型
        #发车时间，到达时间，历时
        data['lishi']:05:52
        data['start_time']:06:58
        data['arrive_time']:12:50
        #各个座位类型的数量(票价编号)
        data['swz_num']    #商务座(A9)
        data['tz_num']     #特等座(P)
        data['zy_num']     #一等座(M)
        data['ze_num']     #二等座(O)
        data['gr_num']     #高级软卧(A6)
        data['rw_num']     #软卧(A4)
        data['yw_num']     #硬卧(A3)
        data['rz_num']     #软座(A2)
        data['yz_num']     #硬座(A1)
        data['wz_num']     #无座
        data['qt_num']     #其他
        """
        data = Left_N['queryLeftNewDTO']
        #print(data)
        print("--" * 50)
        print("出发日期：{} 车次：{} 出发站：{} 目的站：{}".format(date, data['station_train_code'], data['start_station_name'], data['to_station_name']))
        print("座位： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str("商务座", 10, 'left'),chinese_str("特等座", 10, 'left'),
            chinese_str("一等座", 10, 'left'),chinese_str("二等座", 10, 'left'),chinese_str("高级软卧", 15, 'left'),
            chinese_str("软卧", 10, 'left'),chinese_str("硬卧", 10, 'left'),chinese_str("软座", 10, 'left'),
            chinese_str("硬座", 10, 'left'),chinese_str("无座", 10, 'left'),chinese_str("其他", 10, 'left')))
        print("票数： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str(data['swz_num'], 10, 'left'),
            chinese_str(data['tz_num'], 10, 'left'), chinese_str(data['zy_num'], 10, 'left'), chinese_str(data['ze_num'], 10, 'left'), 
            chinese_str(data['gr_num'], 15, 'left'), chinese_str(data['rw_num'], 10, 'left'), chinese_str(data['yw_num'], 10, 'left'), chinese_str(data['rz_num'], 10, 'left'),
            chinese_str(data['yz_num'], 10, 'left'), chinese_str(data['wz_num'], 10, 'left'), chinese_str(data['qt_num'], 10, 'left')))
        #打印票价信息
        train_price(data['train_no'], data['from_station_no'], data['to_station_no'], data['seat_types'], date)
        #打印途经站点信息
        train_stop(data['train_no'], data['start_station_telecode'], data['to_station_telecode'], date)

        
if __name__ == '__main__':
    start_no = 'BXP'
    to_no = 'XAY'
    date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=3), "%Y-%m-%d")
    #print(date)
    train_num(start_no, to_no, date)