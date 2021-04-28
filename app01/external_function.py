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
    neu_que = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,enterprise_sentiment=0).values_list("date", "enterprise_sentiment")
    neg_que = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,enterprise_sentiment=-1).values_list("date", "enterprise_sentiment")

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

chinese_col = ['股票代码','总股本','应收账款周转天数','总资产报酬率','历史授信额度','年化波动率%','企业规模','主体最新信用评级变动方向','最新授信额度','现金流量/流动负债','区间诉讼次数','情感指数','股本回报率','市净率PB（LF）','净利润/营业总收入','综合评级（数值）','存货周转天数','现金流量/营业收入','每股营业总收入','基本每股收益（增长率）','BETA值','股东户数','流动比率','流动资产/总资产','资产负债率','总市值（ 元）','平均收益率%','员工总数','注册资本（元）','应付账款周转天数','市销率PS（TTM）','主体最新信用评级','信用评级']
english_col = ['stock_id','tot_stock','day_accpay','roa','his_creidt','volatility','scale','credit_change','new_credit','cash_liability','laysuit_num','sentiment','roe','pb','inc_rev','com_grade','day_inventory','cash_rev','income','eps_incre','beta','shareholder_num','liquidity_ratio','liquidity_asset','debt_asset','value','yield_field','staff_num','reg_cap','day_accrec','ps','credit_num','credit_str']
eng_chi = {}

for i in range(len(chinese_col)):
    dic = {english_col[i]:chinese_col[i]}
    eng_chi.update(dic)#用字典来存储英文字段和中文字段的对照关系

def change_str_to_num(x):
    if x ==-1:
        return '降低'
    if x==0:
        return '维持'
    if x==1:
        return  '调高'

def element_diag(stock_id):
    obj = models.element_contrib.objects.filter(stock_id=stock_id).values()
    obj1 = models.enterprise_data.objects.filter(stock_id=stock_id).values()
    credit_str =obj1 [0]['credit_str']
    credit_change = change_str_to_num(obj1[0]['credit_change'])
    print(credit_str,credit_change)
    obj = obj[0]#queryset转字典
    field_name = []
    field_value = []
    chi_field_name =[]
    for item in obj.items():
        if item[0] == 'stock_id' or  item[0]=='credit_str':
            continue
        field_name.append(item[0])
    for key in field_name:
        field_value.append(obj[key])

    for i in field_name:
        chi_field_name.append(eng_chi[i])#把英文字段转换成中文字段

    df = pd.DataFrame({'字段名':chi_field_name,'值':field_value})
    df = df.sort_values(by=['值'],ascending=False)

    top_10 = plt_bar(df.iloc[0:10,0],df.iloc[0:10,1],'成分贡献图','属性','贡献度')
    mid_10 = plt_bar(df.iloc[10:20,0],df.iloc[10:20,1],'成分贡献图','属性','贡献度')
    last_10 = plt_bar(df.iloc[20:,0],df.iloc[20:,1],'成分贡献图','属性','贡献度')
    element_par_info = [top_10,mid_10,last_10]

    top_10_pie = plt_pie(df.iloc[0:10,1]/df.iloc[0:10,1].sum(),df.iloc[0:10,0])
    mid_10_pie = plt_pie(df.iloc[10:20,1]/df.iloc[10:20,1].sum(),df.iloc[10:20,0])
    last_10_pie = plt_pie(df.iloc[20:,1]/df.iloc[20:,1].sum(),df.iloc[20:,0])
    element_pie_info =[top_10_pie,mid_10_pie,last_10_pie]

    data = {'element_par_info':element_par_info,'element_pie_info':element_pie_info,'credit_str':credit_str,'credit_change':credit_change}

    return data

def plt_bar(x,y,title,xlabel,ylabel):
    plt.figure(figsize=(6, 3.8))
    plt.rcParams['font.sans-serif'] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
    plt.title(title, fontsize=20)  # 标题，并设定字号大小
    plt.xlabel(xlabel, fontsize=1)  # 设置x轴，并设定字号大小
    plt.xticks(rotation=315)
    plt.ylabel(ylabel, fontsize=14)  # 设置y轴，并设定字号大小
    plt.bar(x, y, alpha=0.6, width=0.8, facecolor='skyblue',
            edgecolor='darkblue')
    buffer = BytesIO()
    plt.savefig(buffer,bbox_inches='tight',pad_inches=0.0)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    img_info = "data:image/png;base64," + ims
    buffer.close()
    plt.close()
    return img_info

def plt_pie(size,labels):
    plt.rcParams['font.sans-serif'] = ["SimHe", "KaiTi", "SimHei", "FangSong"]
    plt.figure(figsize=(6,9))
    # colors = ['dodgerblue', 'orangered', 'limegreen', 'cyan', 'gold']
    plt.pie(size, labels=labels,autopct='%1.1f%%', shadow=False, startangle=150,pctdistance = 0.8)

    # plt.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer,bbox_inches='tight',pad_inches=0.0)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    pie = "data:image/png;base64," + ims
    buffer.close()
    plt.close()
    return pie