# -*- coding=utf-8 -*-

from public import chinese_str,https_get
import json
import datetime
import logging


global train_station
global trains


def train_stop(train_no, from_telecode, to_telecode, date, num):
    #获取经停站点的信息
    url_format = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode={}&to_station_telecode={}&depart_date={}'
    url = url_format.format(train_no, from_telecode, to_telecode, date)
    #print("途经站点：", url)
    response = https_get(url)
    data = json.loads(response)
    #print(data)
    if 'data' not in data:
        print("data['data'] is empty")
        return -1
    else:
        stop_info = data['data']['data']
    
    logging.info("#" * 100)
    logging.info("{} 车次路线站点：".format(num))
    
    print("#" * 150)
    print("{} 车次路线站点：".format(num))
    for stop in stop_info:
        
        logging.info("{:<2s} | {} | {:<5s} | {:<5s} | {:<6s}".format(stop['station_no'], chinese_str(stop['station_name'], 15, 'left'),
            stop['arrive_time'], stop['start_time'], stop['stopover_time']))
        
        print("{:<2s} | {} | {:<5s} | {:<5s} | {:<6s}".format(stop['station_no'], chinese_str(stop['station_name'], 15, 'left'),
            stop['arrive_time'], stop['start_time'], stop['stopover_time']))


def train_price(train_no, from_no, to_no, seat_type, date):
    #获取票价信息实现代码
    url_format = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'
    url = url_format.format(train_no, from_no, to_no, seat_type, date)
    #print("票价:",url)
    response = https_get(url)
    data = json.loads(response)
    if 'data' not in data:
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
    if 'WZ' in price_info:
        price['WZ'] = price_info['WZ']
    else:
        price['WZ'] = '--'
    if 'OT' in price_info:
        price['OT'] = price_info['OT']
    else:
        price['OT'] = '--'
    """
    logging.info("票价： {:<10}|{:<10}|{:<10}|{:<10}|{:<15}|{:<10}|{:<10}|{:<10}|{:<10}|{:<10}".format(price['A9'], price['P'],
        price['M'], price['O'], price['A6'], price['A4'], price['A3'], price['A2'], price['A1'], price['WZ']))
    """
    print("票价： {:<10}|{:<10}|{:<10}|{:<10}|{:<15}|{:<10}|{:<10}|{:<10}|{:<10}|{:<10}".format(price['A9'], price['P'], 
        price['M'], price['O'], price['A6'], price['A4'], price['A3'], price['A2'], price['A1'], price['WZ']))


def train_num(from_station, to_station, date):
    #根据指定日期，查询车票的数量和票价信息
    url_format = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT"
    url = url_format.format(date, from_station, to_station)
    #print("车次：",url)
    response = https_get(url)
    #print(response)
    global trains
    datas = json.loads(response)
    if 'data' not in datas:
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
        
        if data['station_train_code'] not in trains:
            #打印途经站点信息
            train_stop(data['train_no'], data['start_station_telecode'], data['to_station_telecode'], date, data['station_train_code'])
            trains.append(data['station_train_code'])
        
        print("-" * 150)
        print("车次：{} 出发站：{} 目的站：{}".format(data['station_train_code'], data['start_station_name'], data['to_station_name']))
        print("座位： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str("商务座", 10, 'left'),chinese_str("特等座", 10, 'left'),
            chinese_str("一等座", 10, 'left'),chinese_str("二等座", 10, 'left'),chinese_str("高级软卧", 15, 'left'),
            chinese_str("软卧", 10, 'left'),chinese_str("硬卧", 10, 'left'),chinese_str("软座", 10, 'left'),
            chinese_str("硬座", 10, 'left'),chinese_str("无座", 10, 'left'),chinese_str("其他", 10, 'left')))
        print("票数： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str(data['swz_num'], 10, 'left'),
            chinese_str(data['tz_num'], 10, 'left'), chinese_str(data['zy_num'], 10, 'left'), chinese_str(data['ze_num'], 10, 'left'), 
            chinese_str(data['gr_num'], 15, 'left'), chinese_str(data['rw_num'], 10, 'left'), chinese_str(data['yw_num'], 10, 'left'), chinese_str(data['rz_num'], 10, 'left'),
            chinese_str(data['yz_num'], 10, 'left'), chinese_str(data['wz_num'], 10, 'left'), chinese_str(data['qt_num'], 10, 'left')))
        
        logging.info("-" * 100)
        logging.info("车次：{} 出发站：{} 目的站：{}".format(data['station_train_code'], data['start_station_name'], data['to_station_name']))
        logging.info("座位： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str("商务座", 10, 'left'),chinese_str("特等座", 10, 'left'),
            chinese_str("一等座", 10, 'left'),chinese_str("二等座", 10, 'left'),chinese_str("高级软卧", 15, 'left'),
            chinese_str("软卧", 10, 'left'),chinese_str("硬卧", 10, 'left'),chinese_str("软座", 10, 'left'),
            chinese_str("硬座", 10, 'left'),chinese_str("无座", 10, 'left'),chinese_str("其他", 10, 'left')))
        logging.info("票数： {}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(chinese_str(data['swz_num'], 10, 'left'),
            chinese_str(data['tz_num'], 10, 'left'), chinese_str(data['zy_num'], 10, 'left'), chinese_str(data['ze_num'], 10, 'left'), 
            chinese_str(data['gr_num'], 15, 'left'), chinese_str(data['rw_num'], 10, 'left'), chinese_str(data['yw_num'], 10, 'left'), chinese_str(data['rz_num'], 10, 'left'),
            chinese_str(data['yz_num'], 10, 'left'), chinese_str(data['wz_num'], 10, 'left'), chinese_str(data['qt_num'], 10, 'left')))
        
        #打印票价信息
        train_price(data['train_no'], data['from_station_no'], data['to_station_no'], data['seat_types'], date)



def get_station_code():
    #获取车站对应的编码并且存储在全局变量train_station字典中
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001'
    response = https_get(url)
    station_codes = response.split('@')
    #print(station_codes[1:10])
    global train_station
    train_station = {}
    print("start writing the train name and number mapping...")
    with open('record/station_codes.txt', 'w') as f:
        f.write("{} {}\n".format(chinese_str("站名", 10, 'left'), chinese_str("车站编号", 10, 'left')))
        for code in station_codes[1:]:
            name = code.split('|')[1]
            num = code.split('|')[2]
            train_station[name] = num
            f.write("{} {}\n".format(chinese_str(name, 10, 'left'), chinese_str(num, 10, 'left')))


def get_trains_num(date):
    #根据指定日期获取所有的车次信息
    url_format = 'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date={}'
    url = url_format.format(date)
    response = https_get(url)
    global train_station
    global trains
    trains = []
    datas = json.loads(response)['data']
    infos = []
    print("start writing train from station,destination station and number info...")
    
    #这里讲原始页面获取的信息先排序然后重新存储到infos列表，目的只有一个：1.按照（出发站，目的站）顺序打印列车的停经地点，车票数量，车票价格；2.同车次只打印一次停经点信息
    for info in datas:
        tmp = {}
        train_no = info['train_no']
        from_station = info['station_train_code'].split('(')[1].split(')')[0].split('-')[0]
        to_station = info['station_train_code'].split('(')[1].split(')')[0].split('-')[1]
        code = info['station_train_code'].split('(')[0] 
        #from_station 是出发站，to_station是目的站，train_no是车次编号，code是车次代码，例如：
        #{'from_station': '哈尔滨', 'to_station': '北京', 'train_no': '0100000Z1608', 'code': 'Z16'}
        tmp['from_station'] = from_station
        tmp['to_station'] = to_station
        tmp['train_no'] = train_no
        tmp['code'] = code
        infos.append(tmp)
        
    #sort更改原来的无序列表,线按照车次，出发站，目的站顺序排序
    infos.sort(key = lambda x: (x['code'], x['from_station'], x['to_station']))
    
    #sorted 返回修改的列表副本，源列表内容不受影响
    #print(sorted(infos, key = lambda x: (x['from_station'], x['to_station'])))
    #print(infos)
    print("begin writing train_query ...")
    with open("record/train_query.txt", 'w') as f:
        for info in infos:
            f.write("出发站：{} 目的站：{} 车次：{}\n".format(chinese_str(info['from_station'], 15, 'left'), chinese_str(info['to_station'], 15, 'left'), info['code']))
    
    for info in infos:
        #print(info)
        
        from_station = info['from_station']
        to_station = info['to_station']
        train_no = info['train_no']
        code = info['code']
        
        #print("出发日期：{} 车站编码：{:<15} 车次：{:<5} 出发站：{} 出发站编码：{:<5} 目的站：{} 目的站编码：{:<5}".format(date, train_no, code,
        #    chinese_str(from_station, 10, 'left'), train_station[from_station], chinese_str(to_station, 10, 'left'), train_station[to_station]))
        #这里将infos按照车次，出发站，目的站排序，但是在调用的时候需要（出发站，目的站）这样两个参数，有可能会覆盖后面的车次信息，有没有好的办法达到车次打印一次
        #出发站，目的站多次组合
        train_num(train_station[from_station], train_station[to_station], date)
            
    


def init():
    """
    logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(filename)s [line :%(lineno)d] %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%s', filename = 'record/routes.txt', filemode = 'w')
    """
    logging.basicConfig(level = logging.DEBUG, format = '%(message)s',datefmt = '%Y-%m-%d %H:%M:%s', filename = 'record/routes.txt', filemode = 'w')



if __name__ == '__main__':
    date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days = 3), "%Y-%m-%d")
    init()
    get_station_code()
    get_trains_num(date)