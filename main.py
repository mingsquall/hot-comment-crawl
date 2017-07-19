import requests
import json
from lxml import html

class MusicHotCommentCrawl:

    # 获取json解析出专辑内所有歌曲对象，返回歌曲的list
    # 传入专辑id
    def getSongs(self, list_id):
        # 获取专辑url
        url = 'http://music.163.com/album?id='+str(list_id)
        # 专辑列表请求方式为GET, 读取Response内容
        r = requests.get(url)
        tree = html.fromstring(r.text)
        # Xpath定位到包含json信息的那个标签，获取到这个json并解析
        data_json = tree.xpath('//textarea[@style="display:none;"]')[0].text
        data_songs = json.loads(data_json)

        return data_songs

    # 获取每首歌的热门评论list
    # 传入歌曲id
    def getHotComments(self, song_id):
        # 获取歌曲url
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+str(song_id)+'?csrf_token='
        # 表单中两个加密参数，仅限于爬取第一页，其他页码就不适用了
        param = {'params':'tLuQppglQ32L+v9rNqsQQbeE20b0gnB09HHxy8AR2fs951bIlBbdhyE3nX3CfQp8P9rGIFViH8y/SSfBH2DCTxarKjgMCVJpzMOptuwRawzEhVPtEJkvc/C8nzpAZb7Myifyy9iQ898dc/zx+N7VlUjZGJn6smFFqupIVHrMj+WgTaOrbW8ERp/vBokYfG7Sjhhl49dAxMse5pJ83HkmI5f5iGSAPulG5vz/L8wtIss=',\
'encSecKey':'8bb0624301b2ebdcbdb921ce514ddc7f35a7f398f5ee62f1ab37f7b3ac47489dad75f4c2ff67b400badba7e73a52b2ef4dbd0a619b472951c4e56e714951813327dd0af9c2cb5697e3bf6236cc0dd8642bcc5f108799f8324562e76e82e1182ea7bc45a530cbaf3d301443651edf4facbb32462b435cc7a92af449af2f1298db'}
        # 歌曲请求方式为POST
        r = requests.post(url, param)
        # data得到的就是歌曲的json数据
        data = r.text
        # 加载获取的json数据，获得json对象
        json_loaded = json.loads(data)
        hotComments = json_loaded['hotComments']

        return hotComments


crawl_for_rainbowmountain = MusicHotCommentCrawl()
# 2646287是某专辑id，可在网页版歌单的url末尾获取
songs = crawl_for_rainbowmountain.getSongs(2646287)

for song in songs:
    # 此处按照专辑列表内的_歌曲id, 获取到相应歌曲内的热门评论list
    hotComments = crawl_for_rainbowmountain.getHotComments(song['id'])
    # 此处输出每首歌的-歌名-歌手-热评数
    print("\n")
    print("歌曲标题: %s - 歌手: %s - 热评数: %s " % (song['name'], song['artists'][0]['alia'][0], str(len(hotComments))))
    print("\n")
    # 循环输出每一首歌内的所有热门评论
    for i in range(len(hotComments)):
        user_nickname = hotComments[i]['user']['nickname']
        likedCount = hotComments[i]['likedCount']
        user_comment = hotComments[i]['content']
        print("第 %s 条热门评论: " % (i+1))
        print(user_comment)
        print("评论者: %s  收到赞: %s" % (user_nickname, likedCount))
        print("----------------------------------------------------------------")
