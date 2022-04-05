import requests
import re


class Category:
    def __init__(self, category, name):
        self.category = category
        self.name = name

    def __str__(self):
        return self.category + ' ' + self.name

    def __repr__(self):
        return self.category + ' ' + self.name


class Word:
    def __init__(self, origin_no, mean):
        self.origin_no = origin_no
        self.mean = mean

    def __repr__(self):
        return self.origin_no + ' ' + self.mean


"""
    https://sldict.korean.go.kr/front/sign/signList.do
    https://sldict.korean.go.kr/front/sign/signList.do?category=CTE001&pageIndex=1
    https://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=12482
"""

categories = []
words = []


def loadCategory():
    global categories
    body = requests.get(
        'https://sldict.korean.go.kr/front/sign/signList.do', verify=False)
    category_text = body.text.split('<ul id="cteView2" class="">')[
        1].split('</ul>')[0].replace(' ', '')
    categories = [Category(items.split("'")[0], items.split("<span>")[1].split("</span>")[0])
                  for items in category_text.split("javascript:fnSearchCategory('")[1:]]
    return categories


def getWord(category_code, page):
    global words
    search_body = requests.get(
        "https://sldict.korean.go.kr/front/sign/signList.do?category=" +
        str(category_code) + "&pageIndex=" + str(page),
        verify=False).text

    words = [Word(items.split("fnSearchContentsView('")[1].split("'")[0],
                  items.split("fnSearchContentsView('")[1].split('>')[1].split('<')[0].strip())
             for items in search_body.split('<div class="list_right">')[1:]]
    return words


def getMovieUrl(origin_no):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    data = {
        "origin_no": origin_no,
        "size": "high",
        "viewSelect": "high"
    }

    movie = requests.post("https://sldict.korean.go.kr/front/sign/include/controlVideoSpeed.do", verify=False,
                          params=data, headers=headers)

    return movie.text.split('" type="video/mp4"')[0].split('<source src="')[1]


def getPictureUrl(origin_no):
    word_body = requests.get(
        "https://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=" +
        str(origin_no),
        verify=False).text
    temp = word_body.split("content_view_dis")[1].split("dd>")[1]

    picture_list = []  # 이미지 링크
    picture_pos = []  # src 위치

    # src 위치 찾기
    pos = temp.find("src")
    picture_pos.append(pos)
    while temp[pos+1:].find("src") != -1:
        pos = temp[pos+1:].find("src") + pos + 1
        picture_pos.append(pos)

    # 이미지 링크 찾기
    for i in range(len(picture_pos)):
        end_position = temp[picture_pos[i]+5:].find('"') + picture_pos[i] + 5
        picture_list.append(temp[picture_pos[i]+5:end_position])
    return picture_list


def getExplain(origin_no):
    word_body = requests.get(
        "https://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=" +
        str(origin_no),
        verify=False).text

    return word_body.split("content_view_dis")[
        1].split("수형 설명")[1].split("dd>")[1][:-2]


def numOfPages(category_code):
    num = 0
    search_body = requests.get(
        "https://sldict.korean.go.kr/front/sign/signList.do?category=" +
        str(category_code) + "&pageIndex=1",
        verify=False).text

    num = int(
        re.sub(r'[^0-9]', '', search_body.split('t_orange">')[1].split('<')[0]))
    if num % 10 == 0:
        return num//10
    else:
        return num//10 + 1


# loadCategory()

mode = 0
origin_no = None

# while True:
#     if mode == 0:  # 카테고리
#         print('\n'.join([str(str(idx + 1) + ' ' + items.name)
#               for idx, items in enumerate(categories)]))
#         command = int(input("명령여를 입력해주세요.\n"
#                             "1 : 단어 목록\n"
#                             "2 : 카테고리 접속\n"))
#         if command == 1:
#             print('\n'.join([str(str(idx + 1) + ' ' + items.name)
#                   for idx, items in enumerate(categories)]))
#         elif command == 2:
#             num, page = input('번호와 페이지를 입력해주세요').split(' ')
#             getWord(categories[int(num) - 1].category, page)
#             mode = 1
#     elif mode == 1:  # 카테고리 접속
#         print('\n'.join([str(idx + 1) + ' ' +
#               items.mean for idx, items in enumerate(words)]))
#         command = int(input("명령여를 입력해주세요.\n"
#                             "0 : 이전 단계로\n"
#                             "1 : 단어 목록\n"
#                             "2 : 단어 접속\n"))

#         if command == 0:
#             mode = 0
#         elif command == 1:
#             print('\n'.join([str(items.origin_no + ' ' + items.mean)
#                   for items in words]))
#         elif command == 2:
#             num = input('번호를 입력해주세요.')
#             mode = 2
#             origin_no = words[int(num) - 1].origin_no
#     elif mode == 2:  # 단어 접속
#         command = int(input("명령어를 입력해주세요.\n"
#                             "0 : 이전 단계로\n"
#                             "1 : 동영상 보기\n"
#                             "2 : 수형 사진 보기\n"
#                             "3 : 설명 보기\n"))
#         if command == 0:
#             mode = 1
#         elif command == 1:
#             print(getMovieUrl(origin_no))
#         elif command == 2:
#             print(getPictureUrl(origin_no))
#         elif command == 3:
#             print(getExplain(origin_no))
