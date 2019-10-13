#-*- coding=utf-8 -*-

from bs4 import BeautifulSoup
from public import chinese_str,https_get
import json
import urllib
import pymysql

def get_province():
    #获取所有的省份名称
    url = 'https://kyfw.12306.cn/otn/userCommon/allProvince'
    response = https_get(url)
    #print(response)
    datas = json.loads(response)
    province_list = []
    
    for province in datas['data']:
        province_list.append(province['chineseName'])
    
    print(province_list)
    return(province_list)


def get_agency_info(list = []):
    url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/query?province={}&city=&county='
    db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
    cursor = db.cursor()
    with open('record/ticket_agency.txt', 'w') as f:
        for provinces in list:
            p = urllib.parse.quote(provinces)
            url_p = url.format(p)
            print('url:', url_p)

            response = https_get(url_p)
            datas = json.loads(response)
            #print(datas)
            f.write("省份：{}".format(provinces))
            f.write("-" * 100)
            f.write("\n")
            for info in datas['data']['datas']:
                infos = {}
                infos['province'] = info['province'].strip()
                infos['city'] = info['city'].strip()
                infos['county'] = info['county'].strip()
                infos['agency_name'] = info['agency_name'].strip()
                infos['address'] = info['address'].strip()
                infos['start_time'] = info['start_time_am'].strip()
                infos['stop_time'] = info['stop_time_pm'].strip()
                infos['windows_quantity'] = info['windows_quantity'].strip()
                #print(infos)
                #将代理信息写入到mysql
                sql = """ INSERT  ticket_agency(province, city, country, agency_name, address, start_time, end_time, windows_quality) 
                VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
                """
                sql_data = (infos['province'], infos['city'], infos['county'], infos['agency_name'],
                    infos['address'], infos['start_time'], infos['stop_time'], infos['windows_quantity'])
                try:
                    print(sql % sql_data)
                    cursor.execute(sql % sql_data)
                    db.commit()
                    #print("inert sql record success...")
                except Exception as e:
                    db.rollback()
                    print("sql rollback ...", e)

                f.write("省份：{} | 城市：{} | 区县：{} | 代售点：{} | 代售点地址：{} | 营业时间：{}-{} | 窗口数量：{}".
                    format(chinese_str(infos['province'], 10, 'left'), chinese_str(infos['city'], 10, 'left'),
                    chinese_str(infos['county'], 15, 'left'), chinese_str(infos['agency_name'], 60, 'left'), 
                    chinese_str(infos['address'], 80, 'left'), chinese_str(infos['start_time'], 5, 'left'), 
                    chinese_str(infos['stop_time'], 5, 'left'), chinese_str(infos['windows_quantity'], 2, 'left'),))
                f.write("\n")
        db.close()




if __name__ == '__main__':

     province_list = get_province()
     get_agency_info(province_list) 