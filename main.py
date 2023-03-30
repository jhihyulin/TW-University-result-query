import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def get_department_namelists(depID):
    url = 'https://www.cac.edu.tw/CacLink/apply112/112Apply_SieveW8n_H86sTvu/html_sieve_112_P5gW9x/ColPost/common/apply/' + str(depID) + '.htm'
    r = requests.get(url, headers = headers)
    # print(r.text)
    # return html file
    # need to be catch class name htmldw43CC5 and htmldw43CC7
    # then have int
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = []
    tags += soup.find_all('span', class_ = 'htmldw70412')
    tags += soup.find_all('span', class_ = 'htmldw70414')
    li = []
    for tag in tags:
        li.append(int(tag.text))
    # print(li)
    return li

if __name__ == '__main__':
    li = get_department_namelists(153082)
    print(li)
    print('數量: ', len(li))
