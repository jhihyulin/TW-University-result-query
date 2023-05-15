import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import sqlite3
import os

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

def get_star_department_namelists(schID, depID):
    camCode = str(schID).zfill(3) + str(depID).zfill(2)
    # print('校系代碼: ', camCode)
    url = f'https://www.cac.edu.tw/CacLink/star112/112pstar_W2_result_RW64tXZ3qa/html_112_K3tg/ColReport/one2seven/common/star/{camCode}.htm'
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
        if tag.text.startswith('錄取人數'):
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

def get_star_department(schID):
    schID = str(schID).zfill(3)
    url = f'https://www.cac.edu.tw/CacLink/star112/112pstar_W2_result_RW64tXZ3qa/html_112_K3tg/ColReport/one2seven/common/{schID}.htm'
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return None
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('a')
    li = []
    for tag in tags:
        if re.fullmatch(r'\d{5}', tag.text):
            li.append(int(tag.text[3:5]))
    li = np.unique(li)
    return li

def get_star_sch():
    url = 'https://www.cac.edu.tw/CacLink/star112/112pstar_W2_result_RW64tXZ3qa/html_112_K3tg/ColReport/one2seven/collegeList.htm'
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

def get_tu_sch():
    url = 'https://ent01.jctv.ntut.edu.tw/applys1result/college.html'
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return None
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('option')
    li = {}
    for tag in tags:
        if len(tag.text) > 1:
            data = str(tag.text).replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').split('-')
            li.update({int(data[0]): data[1]})
    return li

def get_tu_dep():
    sch_li = get_tu_sch()
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    wc = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tudata (id INTEGER PRIMARY KEY, schName TEXT, depName TEXT, passList TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS pnamedata (id INTEGER PRIMARY KEY, name TEXT)')
    for i in sorted(sch_li.keys()):
        url = f'https://ent01.jctv.ntut.edu.tw/applys1result/college.html?doit=view&code={i}'
        r = requests.post(url, headers = headers)
        if r.status_code != 200:
            print('Error: ', r.status_code)
        else:
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            tags = soup.find_all('tr', {'align': 'center', 'class': 'even'})
            tags = tags + soup.find_all('tr', {'align': 'center', 'class': 'odd'})
            for tag in tags:
                num = tag.findAll('td')[0].text
                name = tag.findAll('td')[1].text
                pname, id = tag.findAll('td')[2].text.replace(
                    '	', '').replace(')', '').replace('\r', '').replace('\n', '').split('(')
                print(num, sch_li[i], name, pname, id)
                if c.execute('SELECT * FROM pnamedata WHERE id = ?', (int(id),)).fetchone() is None:
                    c.execute('INSERT INTO pnamedata (id, name) VALUES (?, ?)', (int(id), pname))
                if wc.execute('SELECT * FROM tudata WHERE id = ?', (num,)).fetchone() is None:
                    passList = []
                    passList.append(int(id))
                    c.execute('INSERT INTO tudata (id, schName, depName, passList) VALUES (?, ?, ?, ?)', (num, sch_li[i], name, str(passList)))
                else:
                    passList = []
                    passList = wc.execute('SELECT passList FROM tudata WHERE id = ?', (num,)).fetchone()[0]
                    passList = passList.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
                    passList.append(int(id))
                    passList = np.unique(passList)
                    c.execute('DELETE FROM tudata WHERE id = ?', (num,))
                    c.execute('INSERT INTO tudata (id, schName, depName, passList) VALUES (?, ?, ?, ?)', (num, sch_li[i], name, str(passList.tolist()).replace('\'', '')))
                conn.commit()
    print('科技大學資料取得完成')

def deal_tudata():
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM tudata')
    wc = conn.cursor()
    wc.execute('CREATE TABLE IF NOT EXISTS tupdata (id INTEGER PRIMARY KEY, schdepID TEXT)')
    count = 0
    for row in c:
        passList = row[3].replace('[', '').replace(']', '').split(', ')
        if passList[0] == '':
            passList = []
        else:
            passList = [int(i) for i in passList]
        for i in passList:
            al_data = wc.execute('SELECT schdepID FROM tupdata WHERE id = ?', (i,)).fetchone()
            print(i, end=' ')
            if al_data is None:
                pass_li = []
                # TODO here is the problem
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            else:
                pass_li = al_data[0].replace('[', '').replace(']', '').split(', ')
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    if type(pass_li[j]) == str:
                        pass_li[j] = pass_li[j].replace('\'', '')
                    else:
                        pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            count += 1
            wc.execute('DELETE FROM tupdata WHERE id = ?', (int(i),))
            wc.execute('INSERT INTO tupdata (id, schdepID) VALUES (?, ?)', (int(i), str(pass_li)))
            conn.commit()
    print(f'科技大學資料處理完成, 總共處理了{count}筆資料, 有{wc.execute("SELECT COUNT(*) FROM tupdata").fetchone()[0]}筆應試號碼')
    conn.close()

def get_data():
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, schName TEXT, depName TEXT, passList TEXT, passCount INTEGER)')
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
                id = int(str(i).zfill(3) + str(j).zfill(3))
                c.execute('INSERT INTO data (id, schName, depName, passList, passCount) VALUES (?, ?, ?, ?, ?)', (id, sch_li[i], name, str(dep_li.tolist()), len(dep_li)))
                conn.commit()
    conn.close()
    print('普通大學資料取得完成')

def deal_data():
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    wc = conn.cursor()
    wc.execute('CREATE TABLE IF NOT EXISTS pdata (id INTEGER PRIMARY KEY, schdepID STRING)')
    count = 0
    for row in c:
        # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        passList = row[3].replace('[', '').replace(']', '').split(', ')
        if passList[0] == '':
            passList = []
        else:
            passList = [int(i) for i in passList]
        for i in passList:
            al_data = wc.execute('SELECT schdepID FROM pdata WHERE id = ?', (int(i),)).fetchone()
            print(i, end=' ')
            if al_data is None:
                pass_li = []
                # TODO here is the problem
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            else:
                pass_li = al_data[0].replace('[', '').replace(']', '').split(', ')
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    if type(pass_li[j]) == str:
                        pass_li[j] = pass_li[j].replace('\'', '')
                    else:
                        pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            count += 1
            wc.execute('DELETE FROM pdata WHERE id = ?', (int(i),))
            wc.execute('INSERT INTO pdata (id, schdepID) VALUES (?, ?)', (int(i), str(pass_li)))
            conn.commit()
    print(f'普通大學資料處理完成, 總共處理了{count}筆資料, 有{wc.execute("SELECT COUNT(*) FROM pdata").fetchone()[0]}筆應試號碼')
    conn.close()

def get_star_data():
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stardata (id INTEGER PRIMARY KEY, schName TEXT, depName TEXT, passList TEXT, passCount INTEGER)')
    conn.commit()
    sch_li = get_star_sch()
    for i in sorted(sch_li.keys()):
        # print('學校代碼: ', i)
        depID = get_star_department(i)
        for j in depID:
            print(str(i).zfill(3), str(j).zfill(2), sch_li[i], end = ' ')
            dep_li, name = get_star_department_namelists(i, j)
            print(name, len(dep_li))
            if dep_li is not None:
                id = int(str(i).zfill(3) + str(j).zfill(2))
                c.execute('INSERT INTO stardata (id, schName, depName, passList, passCount) VALUES (?, ?, ?, ?, ?)', (id, sch_li[i], name, str(dep_li.tolist()), len(dep_li)))
                conn.commit()
    conn.close()
    print('繁星推薦資料取得完成')

def deal_star_data():
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM stardata')
    wc = conn.cursor()
    wc.execute('CREATE TABLE IF NOT EXISTS starpdata (id INTEGER PRIMARY KEY, schdepID STRING)')
    count = 0
    for row in c:
        # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        passList = row[3].replace('[', '').replace(']', '').split(', ')
        if passList[0] == '':
            passList = []
        else:
            passList = [int(i) for i in passList]
        for i in passList:
            al_data = wc.execute('SELECT schdepID FROM starpdata WHERE id = ?', (int(i),)).fetchone()
            print(i, end=' ')
            if al_data is None:
                pass_li = []
                # TODO here is the problem
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            else:
                pass_li = al_data[0].replace('[', '').replace(']', '').split(', ')
                pass_li.append(int(str(row[0]).zfill(3)))
                for j in range(len(pass_li)):
                    if type(pass_li[j]) == str:
                        pass_li[j] = pass_li[j].replace('\'', '')
                    else:
                        pass_li[j] = str(pass_li[j]).zfill(6)
                print(pass_li)
            count += 1
            wc.execute('DELETE FROM starpdata WHERE id = ?', (int(i),))
            wc.execute('INSERT INTO starpdata (id, schdepID) VALUES (?, ?)', (int(i), str(pass_li)))
            conn.commit()
    print(f'繁星推薦資料處理完成, 總共處理了{count}筆資料, 有{wc.execute("SELECT COUNT(*) FROM pdata").fetchone()[0]}筆應試號碼')
    conn.close()

def search(id):
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM pdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('data.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM data WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def tusearch(id):
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM tupdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('data.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM tudata WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def starsearch(id):
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM starpdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('data.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM stardata WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def searchname(id):
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM pnamedata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        return data[1]

def searchAll(id):
    data = search(int(id))
    tudata = tusearch(int(id))
    stardata = starsearch(int(id))
    name = searchname(int(id))
    return data, tudata, stardata, name

def main():
    while True:
        act = int(input('[1]取得並處理資料 [2]查詢應試號碼: '))
        if act == 1:
            print('----------------------------------------')
            os.remove('data.sqlite')
            print('----------------------------------------')
            get_star_data()
            print('----------------------------------------')
            get_data()
            print('----------------------------------------')
            deal_data()
            print('----------------------------------------')
        elif act == 2:
            while True:
                print('========================================')
                num = input('輸入應試號碼(輸入q離開): ')
                if num == 'q':
                    break
                data, tudata, stardata, name = searchAll(num)
                if name is not None:
                    print('----------------------------------------')
                    print(f'姓名: {name}')
                if data is None and tudata is None and stardata is None:
                    print('----------------------------------------')
                    print('查無此號碼')
                else:
                    print('校系代碼 學校名稱 + 校系名稱 (按校系代碼排序)')
                    if stardata is not None:
                        print('----------------------------------------')
                        print(f'繁星推薦通過')# 繁星只有一個校系
                        print('----------------------------------------')
                        for i in stardata.keys():
                            print(str(i).zfill(6), stardata[i])
                    if data is not None:
                        print('----------------------------------------')
                        print(f'普通大學通過{len(data)}個校系')
                        print('----------------------------------------')
                        for i in data.keys():
                            print(str(i).zfill(6), data[i])
                    if tudata is not None:
                        print('----------------------------------------')
                        print(f'科技大學通過{len(tudata)}個校系')
                        print('----------------------------------------')
                        for i in tudata.keys():
                            print(str(i).zfill(6), tudata[i])
                print('========================================')
        else:
            print('----------------------------------------')
            print('輸入錯誤')

if __name__ == '__main__':
    main()