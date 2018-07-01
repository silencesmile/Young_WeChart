import itchat
from pyecharts import Bar,Pie,Geo,Map
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image


# 定义两个全局属性：NickName  Sex
NickName = ""
Sex = 0


def get_sex():
    # 获取好友数据
    my_friends = itchat.get_friends(update=True)[0:]
    sex = {"male": 0, "female": 0, "other": 0}
    for item in my_friends[1:]:
        s = item["Sex"]
        if s == 1:
            sex["male"] += 1
        elif s == 2:
            sex["female"] += 1
        else:
            sex["other"] += 1
    total = len(my_friends[1:])

    # 开始画饼图
    attr = list(sex.keys())
    v1 = list(sex.values())
    pie = Pie("好友性别比例")
    pie.add("", attr, v1, v1, is_label_show=True)
    pie.render(path="sex_html/sex.html")

def get_data(type):
    result=[]
    my_friends = itchat.get_friends(update=True)[0:]

    # 获取作者信息
    temp = itchat.get_friends(update=True)[0:1]
    auth = temp[0]

    #
    global NickName
    global Sex
    NickName = auth.get("NickName")
    Sex = auth.get("Sex")

    for item in my_friends:
        result.append(item[type])

    return result

def friends_province():
    # 获取好友省份
    province= get_data("Province")
    # 分类
    province_distribution = {}
    for item in province:
        #删除英文省份，因为中国地图表中没有
        if bool(re.search('[a-z]',item)):
            continue
        elif not province_distribution.__contains__(item):
            province_distribution[item] = 1
        else:
            province_distribution[item] += 1
    #将省份名为空的删除
    province_distribution.pop('')
    #提取地图接口需要的数据格式
    # print(province_distribution)
    province_keys=province_distribution.keys()
    province_values=province_distribution.values()

    return province_keys,province_values


def friends_signature():
    signature = get_data("Signature")
    wash_signature=[]
    for item in signature:
        #去除emoji表情等非文字
        if "emoji" in item:
            continue
        rep = re.compile("1f\d+\w*|[<>/=【】『』♂ω]")
        item=rep.sub("", item)
        wash_signature.append(item)

    words="".join(wash_signature)

    wordlist = jieba.cut(words, cut_all=True)
    word_space_split = " ".join(wordlist)

    global NickName
    global Sex


    # 图片的作用：生成的图片是这个图片的两倍大小
    # 根据性别选择对应的性别模板图
    if Sex == 2:
        coloring = np.array(Image.open("standard/girl.jpg"))
    elif Sex == 1:
        coloring = np.array(Image.open("standard/boy.jpg"))
    else:
        coloring = np.array(Image.open("standard/num.jpg"))


    # simkai.ttf 必填项 识别中文的字体，例：simkai.ttf，
    my_wordcloud = WordCloud(background_color="white", max_words=800,
                             mask=coloring, max_font_size=120, random_state=30, scale=2,font_path="fonts/simkai.ttf").generate(word_space_split)

    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

    # 保存图片
    my_wordcloud.to_file('Signature/signature.png')

if __name__ == '__main__':

    # False 每次登陆需要扫码  True可自动登录
    itchat.auto_login(False)


    # 微信好友省份分布

    attr,value=friends_province()

    map = Map("我的微信好友分布", "@" + NickName ,width=1200, height=600)
    map.add("", attr, value, maptype='china', is_visualmap=True,
            visual_text_color='#000')
    map.render(path="friends_html/friends.html")


    # 词云
    friends_signature()

    # 性别图可以使用
    get_sex()
