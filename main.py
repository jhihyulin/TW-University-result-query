import requests
from bs4 import BeautifulSoup
import numpy as np
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def get_department_namelists(schID, depID):
    camCode = str(schID).zfill(3) + str(depID).zfill(3)
    print('校系代碼: ', camCode)
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
        if re.fullmatch(r'\d{8}', tag.text):
            li.append(int(tag.text))
        if tag.text.startswith('通過第一階段篩選人數'):
            count = int(re.findall(r'\d+', tag.text)[0])
        if tag.text.startswith(f'({camCode})'):
            name = tag.text.replace(f'({camCode})', '')
    li = np.unique(li)
    if len(li) != count:
        print('Error: ', len(li), count, 'length not equal')
        return None
    print('\n通過第一階段篩選人數: ', len(li))
    print('校系名稱: ', name)
    return li

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
    li = []
    for tag in tags:
        if re.fullmatch(r'\(\d{3}\).*', tag.text):
            li.append(tag.text[5:])
    li = np.unique(li)
    return li

if __name__ == '__main__':
    # schID = int(input('學校代碼: '))
    # depID = int(input('科系代碼: '))
    # li = get_department_namelists(schID, depID)
    # li = get_department(schID)
    li = get_sch()
    print(li)
