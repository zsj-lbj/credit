import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from app01 import models
# import matplotlib.dates as mdates
import wordcloud
import imageio

def off_zero(string):
    return string.split(' ')[0]

#画舆情分类分布图并打包成数据流返回

def opinion_pie(pos_num,neu_num,neg_num):
    plt.rcParams['font.sans-serif']=["SimHe","KaiTi", "SimHei", "FangSong"]
    labels = ['积极', '中性', '消极']
    size = []
    size.append(pos_num)
    size.append(neu_num)
    size.append(neg_num)

    plt.figure(figsize=(6,6))
    plt.pie(size, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
    # plt.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    pie = "data:image/png;base64," + ims
    buffer.close()
    plt.close()

    return  pie

def sequence_dia(stock_id,startdate,enddate):

    pos_que = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,enterprise_sentiment=1).values_list("date", "enterprise_sentiment")
    neu_que = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,
    enterprise_sentiment=0).values_list("date", "enterprise_sentiment")
    neg_que = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,
    enterprise_sentiment=-1).values_list("date", "enterprise_sentiment")

    if len(pos_que)>0:
        pos_df = pd.DataFrame(list(pos_que), columns=["date", "enterprise_sentiment"])
        pos_df['date'] = pos_df['date'].apply(off_zero)
        pos_df = pos_df.groupby('date')['enterprise_sentiment'].count()#分组统计每天的值
        plt.figure(figsize=(6,6))
        plt.rcParams['font.sans-serif'] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
        plt.title('积极评论时序图', fontsize=20)  # 标题，并设定字号大小
        plt.xlabel(u'日期', fontsize=1)  # 设置x轴，并设定字号大小
        plt.xticks(rotation=315)

        plt.ylabel(u'数量', fontsize=14)  # 设置y轴，并设定字号大小
        plt.bar(list(pos_df.index),list(pos_df.values),alpha=0.6,  facecolor = 'skyblue', edgecolor = 'darkblue')
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        pos_img = "data:image/png;base64," + ims
        buffer.close()
        plt.close()

    else: pos_img = None



    if len(neu_que) > 0:
        neu_df = pd.DataFrame(list(neu_que), columns=["date", "enterprise_sentiment"])
        neu_df['date'] = neu_df['date'].apply(off_zero)
        neu_df = neu_df.groupby('date')['enterprise_sentiment'].count()  # 分组统计每天的值
        plt.figure(figsize=(6,6))
        plt.rcParams['font.sans-serif'] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
        plt.title('中性评论时序图', fontsize=20)  # 标题，并设定字号大小
        plt.xlabel(u'日期', fontsize=1)  # 设置x轴，并设定字号大小
        plt.xticks(rotation=315)
        plt.ylabel(u'数量', fontsize=14)  # 设置y轴，并设定字号大小
        plt.bar(list(neu_df.index), list(neu_df.values), alpha=0.6, width=0.8, facecolor='skyblue',
                edgecolor='darkblue')
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        neu_img = "data:image/png;base64," + ims
        buffer.close()
        plt.close()


    else: neu_img = None

    if len(neg_que) > 0:
        neg_df = pd.DataFrame(list(neg_que), columns=["date", "enterprise_sentiment"])
        neg_df['date'] = neg_df['date'].apply(off_zero)
        neg_df = neg_df.groupby('date')['enterprise_sentiment'].count()  # 分组统计每天的值
        plt.figure(figsize=(6,6))
        plt.rcParams['font.sans-serif'] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
        plt.title('消极评论时序图', fontsize=20)  # 标题，并设定字号大小
        plt.xlabel(u'日期', fontsize=1)  # 设置x轴，并设定字号大小
        plt.xticks(rotation=315)
        plt.ylabel(u'数量', fontsize=14)  # 设置y轴，并设定字号大小
        plt.bar(list(neg_df.index), list(neg_df.values), alpha=0.6, width=0.8, facecolor='skyblue',
                edgecolor='darkblue')
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)  # 对plot_data进行编码
        ims = imb.decode()
        neg_img = "data:image/png;base64," + ims
        buffer.close()
        plt.close()

    else: neg_img = None

    sequence_diag = [pos_img,neu_img,neg_img]

    return sequence_diag

def cloud_pic(stock_id,startdate,enddate):
    opinion = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,).values_list("vocabulary1")
    opinion_df = pd.DataFrame(list(opinion), columns=["opinion"])
    word = opinion_df["opinion"].sum()
    cloudobj = wordcloud.WordCloud(font_path='STXINGKA.TTF',mask=imageio.imread('./mystatic/images/cloud2.png'),background_color='white',scale = 0.8).generate(word)  #mask=imageio.imread('./mystatic/images/cloud2.png'),
    cloudobj.to_file("./mystatic/images/cloud/"+stock_id+startdate+enddate+".png")
    plt.rcParams["font.sans-serif"] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
    plt.axis('off')
    plt.imshow(cloudobj)
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    cloud_img = "data:image/jpg;base64," + ims
    buffer.close()
    plt.close()

    return cloud_img



