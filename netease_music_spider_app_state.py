'''
Created on Jan 10, 2018

@author: dec
'''

# save and restore app state

import os

DIR_OUT = os.path.curdir + os.path.sep + "out" + os.path.sep

FILE_PROGRESS_CATEGORY = DIR_OUT + "progress_category.txt"
FILE_PROGRESS_PAGE = DIR_OUT + "progress_page.txt"
FILE_SONG_TOTAL = DIR_OUT + "song_total.txt"

FILE_HOT_SONGS_100000 = DIR_OUT + "hot_songs_100000.txt" # 100000+
FILE_HOT_SONGS_80000 = DIR_OUT + "hot_songs_80000.txt" # 80000 ~ 100000
FILE_HOT_SONGS_60000 = DIR_OUT + "hot_songs_60000.txt" # 60000 ~ 80000
FILE_HOT_SONGS_40000 = DIR_OUT + "hot_songs_40000.txt" # 40000 ~ 60000
FILE_HOT_SONGS_20000 = DIR_OUT + "hot_songs_20000.txt" # 20000 ~ 40000

def save_state_category(current_category):
    if not os.path.exists(DIR_OUT):
        os.mkdir(DIR_OUT)
    with open(FILE_PROGRESS_CATEGORY,'w',encoding='utf-8') as f:
        f.writelines(str(current_category))

def save_state_page(current_page):
    if not os.path.exists(DIR_OUT):
        os.mkdir(DIR_OUT)
    with open(FILE_PROGRESS_PAGE,'w',encoding='utf-8') as f:
        f.writelines(str(current_page))

def save_state_total_songs(total_songs):
    if not os.path.exists(DIR_OUT):
        os.mkdir(DIR_OUT)
    with open(FILE_SONG_TOTAL,'w',encoding='utf-8') as f:
        f.writelines(str(total_songs))

def save_state_hot_songs(hot_song_file, hot_song_record):
    if not os.path.exists(DIR_OUT):
        os.mkdir(DIR_OUT)
    with open(hot_song_file,'a',encoding='utf-8') as f:
        f.writelines(str(hot_song_record) + "\n")


def get_state_category():
    if not os.path.exists(FILE_PROGRESS_CATEGORY):
        return 0
    with open(FILE_PROGRESS_CATEGORY,'r',encoding='utf-8') as f:
        return int(f.readline())

def get_state_page():
    if not os.path.exists(FILE_PROGRESS_PAGE):
        return 0
    with open(FILE_PROGRESS_PAGE,'r',encoding='utf-8') as f:
        return int(f.readline())

def get_state_total_songs():
    if not os.path.exists(FILE_SONG_TOTAL):
        return 0
    with open(FILE_SONG_TOTAL,'r',encoding='utf-8') as f:
        return int(f.readline())

def write_to_file(file_name, txt_content):
    with open(file_name,'w',encoding='utf-8') as f:
        f.writelines(str(txt_content))
        
def get_state_hot_songs(hot_song_file):
    result = dict()
    if not os.path.exists(hot_song_file):
        return result
    with open(hot_song_file,'r',encoding='utf-8') as f:
        for song_record in f:
            song_record = song_record.replace("\n", "")
            song_record = song_record.replace("歌曲ID：", "")
            song_record = song_record.replace("歌名", "")
            song_record = song_record.replace("评论数", "")
            new_record = song_record.split("：")
            result[new_record[0] + " " + new_record[1]] = new_record[2]
    return result