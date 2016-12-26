# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xlsxwriter
from movie_crawler import Movie_crawl

movie_crawl = Movie_crawl()
codes = movie_crawl.code_crawler()
basic_infos = movie_crawl.movie_basic_info(codes)
win_infos = movie_crawl.find_win(codes)
stat_infos = movie_crawl.movie_stat(codes)
rescreen_infos = movie_crawl.Rescreen(codes)
country_info = movie_crawl.movie_country_info(codes)
level_info = movie_crawl.movie_level_info(codes)


workbook = xlsxwriter.Workbook('crawl_movies_2015.xlsx')
worksheet = workbook.add_worksheet()

row = 1
col = 0

for i in range(len(codes)):
    Name = basic_infos[i][0]
    Code_ = basic_infos[i][1]
    Type = basic_infos[i][2]
    Genre = basic_infos[i][3]
    Level = level_info[i]
    RunningTime = basic_infos[i][4]
    Country = country_info[i]
    Released = basic_infos[i][5]
    PublishedYear = basic_infos[i][6]
    Win = win_infos[i]
    Whole_Aud = stat_infos[i][0]
    Seoul_Aud = stat_infos[i][1]
    PoSA = stat_infos[i][2]
    Screen = stat_infos[i][3]
    Noshow = stat_infos[i][4]
    Rescreen = rescreen_infos[i]

    worksheet.write(row, col, Name)
    worksheet.write(row, col+1, Code_)
    worksheet.write(row, col+2, Type)
    worksheet.write(row, col+3, Genre)
    worksheet.write(row, col+4, Level)
    worksheet.write(row, col+5, RunningTime)
    worksheet.write(row, col+6, Country)
    worksheet.write(row, col+7, Released)
    worksheet.write(row, col+8, PublishedYear)
    worksheet.write(row, col+9, Win)
    worksheet.write(row, col+10, Whole_Aud)
    worksheet.write(row, col+11, Seoul_Aud)
    worksheet.write(row, col+12, PoSA)
    worksheet.write(row, col+13, Screen)
    worksheet.write(row, col+14, Noshow)
    worksheet.write(row, col+15, Rescreen)

    row += 1

workbook.close()
