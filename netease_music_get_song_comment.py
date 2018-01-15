from Crypto.Cipher import AES
import base64
import requests
import json
from json.decoder import JSONDecodeError

# 头部信息 #需根据自己浏览器的信息进行替换
headers={'Host':'music.163.com',
         'Accept':'*/*',
         'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
         'Accept-Encoding':'gzip, deflate',
         'Content-Type':'application/x-www-form-urlencoded',
         'Referer':'http://music.163.com/song?id=347597',
         'Content-Length':'484',
         'Cookie':'__s_=1; _ntes_nnid=f17890f7160fd145486752ebbf2066df,1505221478108; _ntes_nuid=f17890f7160fd145486752ebbf2066df; JSESSIONID-WYYY=Z99pE%2BatJVOAGco1d%2FJpojOK94Xe9GHqe0epcCOj23nqP2SlHt1XwzWQ2FXTwaM2xgIN628qJGj8%2BikzfYkv%2FXAUo%2FSzwMxjdyO9oeQlGKBvH6nYoFpJpVlA%2F8eP57fkZAVEsuB9wqkVgdQc2cjIStE1vyfE6SxKAlA8r0sAgOnEun%2BV%3A1512200032388; _iuqxldmzr_=32; __utma=94650624.1642739310.1512184312.1512184312.1512184312.1; __utmc=94650624; __utmz=94650624.1512184312.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); playerid=10841206',	
         'Connection':'keep-alive',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
# first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
second_param = "010001" # 第二个参数
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"

# 获取参数
def get_params(page): # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8") #注意一定要加上这一句，没有这一句则出现错误
    return encrypt_text

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

# decemberpei added function
# song R_SO_4_147030
def get_comment_number(song):
    url = "http://music.163.com/weapi/v1/resource/comments/" + song + "?csrf_token="
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    try:
        json_dict = json.loads(json_text.decode("utf-8"))
        comments_num = int(json_dict['total'])
        return comments_num
    except JSONDecodeError:
        print("json decode error: ")
        print(json_text)
        return 0
    except KeyError:
        print("json decode error: ")
        print(json_text)
        return 0
