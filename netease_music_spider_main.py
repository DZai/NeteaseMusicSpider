#!/usr/bin/python
# -*- coding: UTF-8 -*- 

from bs4 import BeautifulSoup
import requests
import warnings
from netease_music_get_song_comment import get_comment_number
from netease_music_spider_app_state import get_state_category, get_state_page,\
    get_state_hot_songs, get_state_total_songs, save_state_total_songs,\
    save_state_hot_songs, save_state_category, save_state_page

def len_zh(check_str):
    count = 0
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            count = count +1
    return count

warnings.filterwarnings("ignore")

# base url for netease music
BASE_URL = 'http://music.163.com/'

# global session object for use
SESSION = requests.session()

# filter songs with comments count greater than 100000
COMMENT_COUNT_LMT = 100000

FETCHED_SONGS = "fetched_songs.txt"

# pages to fetch for each category
MAX_PAGES_PER_CATE = 2

CATEGORY_BASE_URL = "http://music.163.com/discover/playlist/?order=hot&cat="
CATEGORY_SUFFIX = "&limit=35&offset="

headers = { 'Referer':'http://music.163.com/', 'Host':'music.163.com', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }

url_categories_language = [ CATEGORY_BASE_URL + "华语" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "欧美" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "日语" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "韩语" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "粤语" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "小语种" + CATEGORY_SUFFIX ]

url_categories_style = [CATEGORY_BASE_URL + "流行" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "摇滚" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "民谣" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "电子" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "舞曲" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "说唱" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "轻音乐" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "爵士" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "乡村" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "R%26B%2FSoul" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "古典" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "民族" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "英伦" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "金属" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "朋克" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "蓝调" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "雷鬼" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "世界音乐" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "拉丁" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "%E5%8F%A6%E7%B1%BB%2F%E7%8B%AC%E7%AB%8B" + CATEGORY_SUFFIX, \
              CATEGORY_BASE_URL + "New%20Age" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "古风" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "后摇" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "Bossa%20Nova" + CATEGORY_SUFFIX]

url_categories_feel = [CATEGORY_BASE_URL + "怀旧" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "清新" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "浪漫" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "性感" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "伤感" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "治愈" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "放松" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "孤独" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "感动" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "兴奋" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "快乐" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "安静" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "思念" + CATEGORY_SUFFIX]

url_categories_background = [CATEGORY_BASE_URL + "影视原声" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "ACG" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "校园" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "游戏" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "70后" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "80后" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "90后" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "网络歌曲" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "KTV" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "经典" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "翻唱" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "吉他" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "器乐" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "儿童" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "榜单" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "00后" + CATEGORY_SUFFIX,\
              CATEGORY_BASE_URL + "钢琴" + CATEGORY_SUFFIX ]

def get_song_list_for_page(url):
    songIdList = dict()
    soup = BeautifulSoup(SESSION.get(url).content)
    aList = soup.findAll('a', attrs={'class': 'tit f-thide s-fc0'})
    for a in aList:
        uri = a['href']
        playListUrl = BASE_URL + uri[1:]
        #print("processing play list " + playListUrl)
        soup = BeautifulSoup(SESSION.get(playListUrl,headers = headers).content) 
        ul = soup.find('ul',{'class':'f-hide'}) 
        if(ul != None):
            for li in ul.findAll('li'):
                song_id = (li.find('a'))['href'].split('=')[1]
                song_name = li.get_text()
                songIdList[song_id] = song_name
    print("totally " + str(len(aList)) + " play lists in " + url)
    print("totally " + str(len(songIdList.keys())) + " songs in page " + url)
    return songIdList

if __name__ == '__main__':
    
    start_category = get_state_category() 
    start_page = get_state_page() 
    hot_songs = get_state_hot_songs()
    all_songs = get_state_total_songs()
    url_all_categories = url_categories_background + url_categories_feel + url_categories_language + url_categories_style
    for cate_index in range(start_category, len(url_all_categories)):
        save_state_category(cate_index)
        for page_index in range(start_page, MAX_PAGES_PER_CATE):
            save_state_page(page_index)
            print("*** category index: " + str(cate_index) + " page index: " + str(page_index))
            page_song_list = get_song_list_for_page(url_all_categories[cate_index] + str(page_index * 35))
            for song_id in page_song_list.keys():
                comment_num = get_comment_number("R_SO_4_" + song_id)
                all_songs = all_songs + 1
                print("new song id " + song_id + ", totally " + str(all_songs) + " songs...")
                save_state_total_songs(all_songs)
                if(comment_num > COMMENT_COUNT_LMT):
                    song_key = song_id + " " + page_song_list[song_id]
                    if(song_key in hot_songs):
                        print(song_key +" already exists, pass")
                    else:
                        hot_songs[song_key] = comment_num
                        song_record = "歌曲ID：" + song_id.ljust(10) + "歌名：" + page_song_list[song_id].ljust(40 - int(len_zh(page_song_list[song_id])/2)) + "评论数：" + str(hot_songs[song_key]).ljust(8)
                        print(song_record)
                        save_state_hot_songs(song_record)
        start_page = 0
    print("All Done, totally songs parsed: " + str(all_songs))
    
    
    