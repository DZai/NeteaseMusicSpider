'''
Created on Jan 10, 2018

@author: dec
'''

# save and restore app state

import os

FILE_PROGRESS_CATEGORY = "progress_category.txt"
FILE_PROGRESS_PAGE = "progress_page.txt"
FILE_SONG_TOTAL = "song_total.txt"
FILE_HOT_SONGS = "hot_songs.txt"

def save_state_category(current_category):
    with open(FILE_PROGRESS_CATEGORY,'w',encoding='utf-8') as f:
        f.writelines(str(current_category))

def save_state_page(current_page):
    with open(FILE_PROGRESS_PAGE,'w',encoding='utf-8') as f:
        f.writelines(str(current_page))

def save_state_total_songs(total_songs):
    with open(FILE_SONG_TOTAL,'w',encoding='utf-8') as f:
        f.writelines(str(total_songs))

def save_state_hot_songs(hot_song):
    with open(FILE_HOT_SONGS,'a',encoding='utf-8') as f:
        f.writelines(str(hot_song) + "\n")


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
        
def get_state_hot_songs():
    result = dict()
    if not os.path.exists(FILE_HOT_SONGS):
        return result
    with open(FILE_HOT_SONGS,'r',encoding='utf-8') as f:
        for song_record in f:
            song_record = song_record.replace("\n", "")
            song_record = song_record.replace("歌曲ID：", "")
            song_record = song_record.replace("歌名", "")
            song_record = song_record.replace("评论数", "")
            new_record = song_record.split("：")
            result[new_record[0] + " " + new_record[1]] = new_record[2]
    return result