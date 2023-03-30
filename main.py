import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import sqlite3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def get_department_namelists(schID, depID):
    camCode = str(schID).zfill(3) + str(depID).zfill(3)
    # print('校系代碼: ', camCode)
    url = f'https://www.cac.edu.tw/CacLink/apply112/112Apply_SieveW8n_H86sTvu/html_sieve_112_P5gW9x/ColPost/common/apply/{camCode}.htm'
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return None
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('span')
    li = []
    for tag in tags:
        if re.fullmatch(r'[A\d]\d{7}', tag.text):
            if tag.text.startswith('A'):
                # 青年儲蓄帳戶組開頭為 A 先做移除處理
                li.append(int(tag.text[1:]))
            else:
                li.append(int(tag.text))
        if tag.text.startswith('通過第一階段篩選人數'):
            count = int(re.findall(r'\d+', tag.text)[0])
        if tag.text.startswith(f'({camCode})'):
            name = tag.text.replace(f'({camCode})', '')
    if len(li) == 0:
        # print('Error: ', 'length is 0')
        return np.unique([]), name
    li = np.unique(li)
    # print(li)
    if len(li) != count:
        print('Error: ', len(li), count, 'length not equal')
        return None
    # print('\n通過第一階段篩選人數: ', len(li))
    # print('校系名稱: ', name)
    return li, name

def get_department(schID):
    schID = str(schID).zfill(3)
    url = f'https://www.cac.edu.tw/CacLink/apply112/112Apply_SieveW8n_H86sTvu/html_sieve_112_P5gW9x/ColPost/common/{schID}.htm'
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return None
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('a')
    li = []
    for tag in tags:
        if re.fullmatch(r'\d{6}', tag.text):
            li.append(int(tag.text[3:6]))
    li = np.unique(li)
    return li

def get_sch():
    url = 'https://www.cac.edu.tw/CacLink/apply112/112Apply_SieveW8n_H86sTvu/html_sieve_112_P5gW9x/ColPost/collegeList.htm'
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return None
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('span')
    li = {}
    for tag in tags:
        if re.fullmatch(r'\(\d{3}\).*', tag.text):
            li.update({int(tag.text[1:4]): tag.text[5:]})
            # print(tag.text[1:4], tag.text[5:])
    return li

def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, schID INTEGER, schName TEXT, depID INTEGER, depName TEXT, passList TEXT, passCount INTEGER)')
    conn.commit()
    sch_li = get_sch()
    for i in sorted(sch_li.keys()):
        # print('學校代碼: ', i)
        depID = get_department(i)
        for j in depID:
            print(str(i).zfill(3), str(j).zfill(3), sch_li[i], end = ' ')
            dep_li, name = get_department_namelists(i, j)
            print(name, len(dep_li))
            if dep_li is not None:
                c.execute('INSERT INTO data (schID, schName, depID, depName, passList, passCount) VALUES (?, ?, ?, ?, ?, ?)', (int(i), sch_li[i], int(j), name, str(dep_li.tolist()), len(dep_li)))
                conn.commit()
    conn.close()

if __name__ == '__main__':
    # schID = int(input('學校代碼: '))
    # depID = int(input('科系代碼: '))
    # li = get_department_namelists(schID, depID)
    # li = get_department(schID)
    # li = get_sch()
    # print(li)
    get_data()
