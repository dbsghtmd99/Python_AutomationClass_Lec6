import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs


def getRankList():
    url = 'https://www.naver.com/'
    html = requests.get(url)
    # pprint(html.text)
    soup = bs(html.text, 'html.parser')
    # soup.select('태그명')
    # soup.select('.클래스명')
    # soup.select('상위태그명 > 하위태그명 > 하위태그명')
    # soup.select('상위태그명.클래스명 > 하위태그명.클래스명')  # 바로 아래의(자식) 태그를 선택시에는 > 기호를 사용
    data = soup.select('div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li')
    # pprint(data)
    b = []
    for sill in data:
        b.append(sill.text)
    # print(b)

    k = 1
    list = []
    for i in b:
        if k > 9:
            list.append(i[5:-2])
        else:
            list.append(i[4:-2])
        k += 1
    # print(list)

    print("=" * 30 + '\n' + ' ' * 7 + 'NAVER RANK LIST\n' + '=' * 30)
    for s, list in enumerate(list):
        print("{}위 - {}".format(s + 1, list))


# getRankList() # for test

def getWebtoonTitle():
    # 웹 페이지를 열고 소스코드를 읽어옵니다.
    url = "http://comic.naver.com/webtoon/weekday.nhn"
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    html.close()

    # 요일별 웹툰영역 추출하기
    data1_list = soup.findAll('div', {'class': 'col_inner'})

    # 전체 웹툰 리스트
    week_title_list = []

    for data1 in data1_list:
        # 제목 포함영역 추출하기
        data2 = data1.findAll('a', {'class': 'title'})

        # 텍스트만 추출
        title_list = [t.text for t in data2]

        # extend는 요소로 바꿔서 추가 []가 사라짐
        # week_title_list.extend(title_list)

        # append는 그대로 추가
        week_title_list.append(title_list)

    pprint(week_title_list)


# getWebtoonTitle() # for test

import re, os
from urllib.request import urlretrieve


def getThumbnail():
    try:
        if not (os.path.isdir('image')):
            os.makedirs(os.path.join('image'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("폴더 생성 실패")
            exit()

    # 웹 페이지를 열고 소스코드를 읽어옵니다.
    url = "http://comic.naver.com/webtoon/weekday.nhn"
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    html.close()

    # 요일별 웹툰영역 추출하기
    data1_list = soup.findAll('div', {'class': 'col_inner'})

    # 전체 웹툰 리스트
    li_list = []
    for data1 in data1_list:
        # 제목 + 썸네일 영역추출
        li_list.extend(data1.findAll('li'))

    # 각각의 썸네일과 제목 추출
    for li in li_list:
        img = li.find('img')
        title = img['title']
        img_src = img['src']
        # print(title, img_src)
        title = re.sub('[0-9a-zA-Zㄱ-힗]', '', title)
        urlretrieve(img_src, './image/' + title + '.jpg')


# getThumbnail() # for test

def ex1():
    # 웹 페이지를 열고 소스코드를 읽어옵니다.
    url = "https://www.youtube.com/feed/trending/"
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    html.close()

    data1 = soup.findAll('a', {'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
    for link in data1:
        YTurl = 'https://www.youtube.com' + link.get('href')
        print(YTurl)

ex1() # for test
