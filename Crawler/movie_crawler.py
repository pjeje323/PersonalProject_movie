# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
import re

class Movie_crawl(object):

    def __init__(self):
        pass

    # code crawling
    def code_crawler(self):
        Code = []
        #pages = [80,81,82,83,84]
        pages = range(1,100)
        for page in pages:
            res = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do',
            params = {'curPage':page, 'useYn':'Y','sMovLang':'ko','sOpenYearS':'2015-01-01',
            'sOpenYearE':'2015-12-31','sPrdtStatStr':'개봉','sMovTypeStr':'옴니버스,장편'
            ,'sGradeStr':'12세이상관람가,전체관람가,15세이상관람가,청소년관람불가'
            ,'searchOpen':'Y','sPrdtStatCd':'220210','sMovTypeCd':'220103'
            ,'sMovTypeCd':'220101'})
            content = res.content
            soup = BeautifulSoup(content,'html.parser')
            try:
                a_none = soup.find('tbody').find_all('a', attrs = {'href':'#none'})
                find_code = re.findall(u"'movie','2\d\d\d\d\d\d\d'", str(a_none))
                for i in range(len(find_code)):
                    codes = find_code[i].split(',')[1].strip("''")
                    Code.append(codes)
                    for codes in Code:
                        if Code.count(codes) != 1:
                            Code.remove(codes)
                        else:
                            pass
            except AttributeError:
                pass
        return Code



    # 기본 정보들
    def movie_basic_info(self, Code):
        Basic_info = []
        for code in Code:
            stat = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'titleYN':'Y', 'isOuterReq':'false'})
            stats = stat.content
            BasicInfo = BeautifulSoup(stats, 'html.parser')
            name = BasicInfo.find('div', attrs = {'class':'mtitle'}).get_text().split('(')
            Name = str(name[0]).encode('utf-8')
            # NameEng = str(name[1])
            Code_ = code
            Type = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[0].get_text().strip()
            Genre = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[2]\
            .get_text().split(',')[0].strip().split('/')[0]
            RunningTime = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[3].get_text().split('분')[0]
            Released = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[6].get_text().strip()
            Published = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[7].get_text(' ').split()[1].split()[0]
            PublishedYear = '\n'.join(re.findall(u'\d+', Published))

            Basic_info.append((Name, str(Code_), str(Type), str(Genre),str(RunningTime),
            str(Released), str(PublishedYear)))
        return Basic_info


    # 국가 정보
    def movie_country_info(self, Code):
        Country_infos = []
        for code in Code:
            stat = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'titleYN':'Y', 'isOuterReq':'false'})
            stats = stat.content
            BasicInfo = BeautifulSoup(stats, 'html.parser')
            country = BasicInfo.find('article', attrs = {'class':'basicInfo'})('li')[5].get_text().strip()
            if country.find(',') == True:
                country = country.strip(',')[0]
                Country_infos.append(country)
            else:
                Country_infos.append(country)
        return Country_infos


    def movie_level_info(self, Code):
        Level_info = []
        for code in Code:
            stat = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'titleYN':'Y', 'isOuterReq':'false'})
            stats = stat.content
            BasicInfo = BeautifulSoup(stats, 'html.parser')
            try:
                Level = BasicInfo.find_all('li',attrs = {'class':'nobar'})[2].get_text().strip()
                Level_info.append(Level)
            except TypeError as e:
                Level_info.append('?')
            except IndexError as I:
                Level_info.append('?')
        return Level_info


    # 수상 경력
    def find_win(self, Code):
        win_list = []
        for code in Code:
            stat = requests.post('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'titleYN':'Y', 'isOuterReq':'false'})
            stats = stat.content
            BasicInfo = BeautifulSoup(stats, 'html.parser')
            Win = BasicInfo.find_all('td',attrs = {'class':'ellipsis leftP08 alignL'})
            win_lst = []
            try:
                for i in range(len(Win)+1):
                    if i % 3 == 2:
                        if Win[i].get_text() != '':
                            win_lst.append(Win[i].get_text())
                        else:
                            pass
                    else:
                        pass
                if win_lst != []:
                    win_list.append('1')
                else:
                    win_list.append('0')
            except:
                win_list.append('0')
        return win_list


    # 통계 정보들
    def movie_stat(self, Code):
        stat_info = []
        for code in Code:
            res_stat = requests.post(
            'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'sType':'stat'})
            stats = res_stat.content
            stat = BeautifulSoup(stats, 'html.parser')

            try:
                WholeAud = stat.find('tfoot')('td')[3].get_text().split('(')[0].strip()
            except TypeError:
                Wholeaud = '?'

            try:
                SeoulAud = stat.find('table', attrs = {'class':'board02 bma b02s'})('td')[3].get_text().split('(')[0]
            except TypeError:
                SeoulAud = '?'

            try:
                PoSA = stat.find('table', attrs = {'class':'board02 bma b02s'})('td')[3].get_text().split('(')[1].split('%')[0]
            except TypeError:
                PoSA = '?'

            try:
                Screen = stat.find('table', attrs = {'class':'board02 b02s'})('tfoot')[0]('td')[1].get_text()
            except TypeError:
                Screen = '?'

            try:
                Noshow = stat.find('table', attrs = {'class':'board02 b02s'})('tfoot')[0]('td')[2].get_text()
            except TypeError:
                Noshow = '?'

            stat_info.append((WholeAud, SeoulAud, PoSA, Screen, Noshow))
        return stat_info


    # 재개봉/재상영 여부
    def Rescreen(self, Code):
        rescreen_list = []
        for code in Code:
            NowRld = requests.post(
            'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do',
            params = {'code': code, 'sType':'thea'})
            NOW = NowRld.content
            Now = BeautifulSoup(NOW, 'html.parser').get_text(' ').strip()[:5]
            if re.search(Now, u'상영영화관'):
                rescreen_list.append('0')
            else:
                rescreen_list.append('1')
        return rescreen_list
