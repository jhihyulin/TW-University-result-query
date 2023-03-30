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
    tags = []
    tags += soup.find_all('span')
    tags += soup.find_all('span')
    li = []
    for tag in tags:
        if len(tag.text) == 8:
            li.append(int(tag.text))
        if tag.text.startswith('通過第一階段篩選人數'):
            count = int(re.findall(r'\d+', tag.text)[0])
        if tag.text.startswith(f'({camCode})'):
            name = tag.text.replace(f'({camCode})', '')
    li = np.unique(li)
    # print('get count: ', count)
    # print('get length: ', len(li))
    print('校系名稱: ', name)
    if len(li) != count:
        print('Error: ', len(li), count, 'length not equal')
        return None
    return li

if __name__ == '__main__':
    schID = int(input('學校名稱: '))
    depID = int(input('科系代碼: '))
    li = get_department_namelists(schID, depID)
    print(li, '\n通過第一階段篩選人數: ', len(li))
