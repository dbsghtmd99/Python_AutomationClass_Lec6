# Python_AutomationClass_Lec6

여섯 번째 수업에서는 html 정보로부터 크롤링을 하는 방법에 대해 학습했다.

소스코드 파일은 [https://github.com/dbsghtmd99/Python_AutomationClass_Lec6](https://github.com/dbsghtmd99/Python_AutomationClass_Lec6) 에서 확인 가능하다.

## 1. 라이브러리 설명

beautifulSoup : html 로부터 사용자가 원하는 값들을 크롤링 해오는 기능 제공

## 2. 수업 때 다루었던 내용

1. 네이버 실시간 검색어 순위 불러오기
   
```python
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
```

2. 요일별 네이버 웹툰 제목 가져오기
   
```python
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
```

3. 요일별로 웹툰 썸네일 가져오기
   
```python
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
```

## 3. 연습문제

프로젝트가 유튜브와 관련되어 있어서 미리 연습 해보고자 수업을 한 당일 구현해보았다. 아래의 코드는 유튜브의 '인기' 탭에 있는 동영상들의 Url을 모두 가져오는 기능을 수행한다.

```python
def ex1():
    # 웹 페이지를 열고 소스코드를 읽어옵니다.
    url = "https://www.youtube.com/feed/trending/"
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    html.close()

    # 아래의 클래스명은 f12 개발자 도구를 이용하여 찾으려 하였으나, 검색해도 나오지 않아 'a' 태그를 모두 출력한 후, 출력된 값들 중 찾고 있는 값을 검색하여 구해냈다.
    data1 = soup.findAll('a', {'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
    for link in data1:
        YTurl = 'https://www.youtube.com' + link.get('href')
        print(YTurl)

# ex1() # for test
```

실행 결과

![1](test.png)