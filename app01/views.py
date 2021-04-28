from django.shortcuts import render,redirect,reverse
from django.http  import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
import re
from django.http import JsonResponse
from django.db.models import  F
import numpy as np
from app01.external_function import *
import jieba
import jieba.analyse
from snownlp import SnowNLP
import os
from snownlp import sentiment


# Create your views here.

def home(request):
    info={'size':255,
          'name':'hello word',
          'a_tag': "<a href='#'>点我</a>" ,
          'ss':'i love huangshiyue',
          'aa':'the same to hsy' ,
          'zsj':3,
          'hsy':4,
          'list':['zsj','hsy'],
          'dic':{'zsj':'husband','hsy':'wife',},

    }


    return render(request,'home.html',info)#这里必须用绝对路径，不然找不到文件

def date(request,year):

     return HttpResponse(str(year))

# def index(request):
#     print(request.POST)
#     return render(request,'index.html ')

from django.views import View

def outter(f):
    def inner(request):
        print(1)
        ret = f(request)
        print(2)
        return  ret
    return  inner

from django.utils.decorators import method_decorator

# class Login(View):
#     #重写父类View的dispatch方法
#     def dispatch(self, request, *args, **kwargs):
#         print('111')
#         ret = super().dispatch( request, *args, **kwargs)
#         print('222')
#         return ret
#
#
#     @method_decorator(outter)
#     def get(self,request):
#         return  render(request,'login.html')
#
#     def post(self,request):
#         print(request.POST)
#         if request.POST.get('uname')=='zeng' and request.POST.get('psd')=='123':
#             return render(request,'index.html')
#         else:
#             return  HttpResponse('密码错误')

def Login(request):
    tip = 'OR'
    if request.method == 'POST':
        u = request.POST.get('user')
        p = request.POST.get('password')
        if User.objects.filter(username=u):
            user = authenticate(username=u,password=p)
            print(user)
            if user:
                tip = '登陆成功'
                login(request,user)
                request.session['username'] = u
                return render(request,'index.html')
            else:
                tip = '账号密码错误，请重新输入'
        else:
            tip = '用户不存在，请注册'



    return render(request,'login.html',locals())

def mystatic(request):
    data=[11,22,33]
    return render(request,'static.html',{'data':data})



def add(request):
    # obj = models.Book(
    #     title='hsy',
    #     state=True,
    #     pub_date='2020-03-03',
    #     price=15,
    #     publish='hsy 出版社'
    # )
    # obj.save()
    if request.method == 'GET':
        return  render(request,'add.html')
    else:

        title = request.POST.get('title')
        date = request.POST.get('date')
        price = request.POST.get('price')
        publish = request.POST.get('publish')
        print(publish)
        obj = models.Book(
            title = title,
            pub_date = date,
            price = price,
            publish = publish
        )
        obj.save()


    return redirect(reverse('book_show'))


def book_show(request):

    books = models.Book.objects.all()


    return render(request,'book_show.html',{'book':books})

global id,name,stdate,endate#声明全局变量，用来存储index页面输入的股票代码，名称，开始日期，截至日期
id='000002'#规定一个默认值
name='万科A'
stdate='2020-09-01'
endate='2021-04-05'



def index(request):
    user_info = models.user_info.objects.get(user=request.session.get('username'))
    nickname = user_info.nickname#获取当前用户昵称
    img_src = user_info.img_src#获取用户头像图片地址

    #获取所有一级行业
    obj1 = models.first_second.objects.all().values('first').distinct()
    first = []
    for i in range(0, len(obj1)):
        first.append(obj1[i]['first'])
    if request.method =='POST':
        firstname = request.POST.get('firstname')
        secondname = request.POST.get('secondname')
        thirdname = request.POST.get('thirdname')
        fourthname = request.POST.get('fourthname')
        firmname = request.POST.get('firmname')#此处的公司名字是从行业联级查询得来的
        id_or_name = request.POST.get('id_or_name')#处理搜索框提示数据的
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        name_or_id = request.POST.get('name_or_id')#处理搜索框正式提交的数据的

        if firstname  and secondname is None and thirdname is None and fourthname is None:
            obj2 = models.first_second.objects.filter(first=firstname).values('second')
            second = []
            for i in obj2:
                json_dict = {}
                json_dict['second'] = i['second']
                second.append(json_dict)
            data = {'second':second}
            return JsonResponse(data)
        if  secondname and secondname!='...请选择二级行业':
            obj3 = models.second_third.objects.filter(second=secondname).values('third')

            third = []
            for i in obj3:
                json_dict = {}
                json_dict['third'] = i['third']
                third.append(json_dict)
            data = {'third': third}
            return JsonResponse(data)

        if thirdname and thirdname != '...请选择三级行业':
            obj4 = models.third_fourth.objects.filter(third=thirdname).values('fourth')

            fourth = []
            for i in obj4:
                json_dict = {}
                json_dict['fourth'] = i['fourth']
                fourth.append(json_dict)
            data = {'fourth': fourth}
            return JsonResponse(data)

        if fourthname and fourthname != '...请选择四级行业':
            obj5 = models.fourth_firmname.objects.filter(fourth=fourthname).values('firmname')

            firmname = []
            for i in obj5:
                json_dict = {}
                json_dict['firmnae'] = i['firmname']
                firmname.append(json_dict)
            data = {'firmname': firmname}
            return JsonResponse(data)
        if id_or_name:#处理搜索框提示数据的
            if re.match('^\d',id_or_name):#如果是股票代码
                obj6 = models.fourth_firmname.objects.filter(stock_id__startswith=id_or_name).values('stock_id','firmname')
                id_and_name = []
                for i in obj6:
                    id_and_name.append(i)
                data = {'id_and_name': id_and_name}

                return JsonResponse(data)
            else:#如果输入是的公司名称
                obj6 = models.fourth_firmname.objects.filter(firmname__startswith=id_or_name).values('stock_id','firmname')
                id_and_name = []
                for i in obj6:
                    id_and_name.append(i)
                data = {'id_and_name': id_and_name}
                return JsonResponse(data)
        if (firmname is not None) and (startdate is not None) and (enddate is not None):#处理行业联级查询提交的数据
            stock_id = models.fourth_firmname.objects.get(firmname=firmname).stock_id

            opinion = models.enterprise_sentiment.objects.filter(stock_id=stock_id,date__gte=startdate,date__lte=enddate)
            negative = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate,enterprise_sentiment=-1)
            neutral = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate,date__lte=enddate, enterprise_sentiment=0)
            last_month = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte='2021-02-01', date__lte='2021-03-31')
            this_month = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte='2020-12-01', date__lte='2021-01-31')
            credit = models.enterprise_data.objects.filter(stock_id=stock_id).values_list('credit_str')[0][0]
            #把当前提交的公司名称和股票代码存储到session中，便于其他页面调用
            request.session['stock_id'] = stock_id
            request.session['firmname'] = firmname

            opinion_num = len(opinion)#舆情总量
            negative_num = len(negative)#消极舆情总量
            neutral_num = len(neutral)#中性舆情总量
            positive_num = opinion_num-neutral_num-neutral_num#积极舆情总量
            growth_rate = (len(this_month)-len(last_month))/len(last_month)
            pie_img = opinion_pie(positive_num,neutral_num,neutral_num)
            sequence_diag = sequence_dia(stock_id,startdate,enddate)
            cloud_img = cloud_pic(stock_id,startdate,enddate)
            info = [stock_id,startdate,enddate]
            data = {'opinion_num':opinion_num,'negative_num':negative_num,'growth_rate':round(growth_rate*100,2),'credit':credit,'pie_img':pie_img,'sequence_diag':sequence_diag,'cloud_img':cloud_img,'info':info}
            return JsonResponse(data)

        if (name_or_id is not None) and (startdate is not None) and (enddate is not None):#处理搜索框正式提交的数据的
            if not re.match('^\d', name_or_id):  # 如果是股票名称
                stock_id = models.fourth_firmname.objects.get(firmname=name_or_id).stock_id
                request.session['stock_id'] = stock_id
                request.session['firmname'] = name_or_id

            else:
                stock_id = name_or_id
                request.session['stock_id'] = stock_id
                request.session['firmname'] = models.fourth_firmname.objects.get(stock_id=stock_id).firmname
            request.session['startdate'] = startdate
            request.session['enddate'] = enddate

            opinion = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate,date__lte=enddate)
            neutral = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate,date__lte=enddate, enterprise_sentiment=0)
            negative = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate, date__lte=enddate, enterprise_sentiment=-1)
            last_month = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte='2021-02-01',date__lte='2021-03-31')
            this_month = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte='2020-12-01',date__lte='2021-01-31')
            credit = models.enterprise_data.objects.filter(stock_id=stock_id).values_list('credit_str')[0][0]


            opinion_num = len(opinion)  # 舆情总量
            neutral_num = len(neutral)  # 中性舆情总量
            negative_num = len(negative)  # 消极舆情总量
            positive_num = opinion_num-neutral_num-neutral_num#积极舆情总量
            growth_rate = (len(this_month) - len(last_month)) / len(last_month)
            pie_img = opinion_pie(positive_num, neutral_num, neutral_num)
            sequence_diag = sequence_dia(stock_id, startdate, enddate)
            cloud_img = cloud_pic(stock_id, startdate, enddate)
            info = [stock_id,startdate,enddate]
            data = {'opinion_num': opinion_num, 'negative_num': negative_num,
                    'growth_rate': round(growth_rate * 100, 2),'credit':credit,'pie_img':pie_img,'sequence_diag':sequence_diag,'cloud_img':cloud_img,'info':info}
            return JsonResponse(data)


    return render(request,'index.html',{'first':first,'nickname':nickname,'img_src':img_src})



def opinion_details(request):

    stock_id = request.session.get('stock_id')
    firmname = request.session.get('firmname')
    startdate = request.session.get('startdate')
    enddate = request.session.get('enddate')
    obj = models.enterprise_sentiment.objects.filter(stock_id=stock_id, date__gte=startdate,date__lte=enddate)
    data = {'stock_id':stock_id,'stock_name':firmname,'opinion_details':obj}
    if request.method =='POST':
        click_num = request.POST.get('click_num')
        review_num = request.POST.get('review_num')
        opinion = request.POST.get('opinion')
        date = request.POST.get('date')

        models.enterprise_sentiment.objects.filter(click_num=click_num,review_num=review_num,opinion=opinion,date=date).update(click_num=F('click_num')+1)




    return render(request,'opinion_details.html',{'data':data})

def index2(request):
    return render(request,'index2.html')

def index3(request):
    return render(request,'index3.html')



def register(request):
    if request.method =='GET':
        render(request,'register.html')

    if request.method == 'POST':

        u = request.POST.get('user','')

        email = request.POST.get('email','')
        psd1 = request.POST.get('psd1','')
        psd2 = request.POST.get('psd2','')

        if User.objects.filter(username=u):
            tip = '用户已存在，请重新输入用户名'
        else:
            if psd1 != psd2:
                tip ='两次密码输入不一致，请重新输入'
            else:

                d = dict(username=u,password=psd1,email=email,is_staff=1)
                obj = User.objects.create_user(**d)
                obj.save()
                tip = "注册成功 请登陆"

    return render(request,'register.html',locals())

def forgot_password(request):
    import random
    button = '发送验证码'
    VCodeInfo = False
    password = False
    if request.method == 'POST':
        u = request.POST.get('user')
        VCode = request.POST.get('VCode')
        p = request.POST.get('password')
        user = User.objects.filter(username=u)
        #用户不存在
        if not user:
            print(1)
            tip = '用户不存在'
        else:
            #判断验证码并将其写入session
            if not request.session.get('VCode'):
                button = '重置密码'
                tip = '验证码已发送'
                password = True
                VCodeInfo = True
                VCode = str(random.randint(1000,9999))
                request.session['VCode'] = VCode
                user[0].email_user('找回密码',VCode)
            elif VCode == request.POST.get('VCode'):
                #密码加密处理并保存到数据库
                s_p= make_password(p,None,'pbkdf2_sha256')
                user[0].password=s_p
                user[0].save()
                del request.session['VCode']
                tip = '密码已经重置'
            #输入验证码错误
            else:
                tip = '验证码错误，请重新获取'
                VCodeInfo = False
                password = False
                del request.session['VCode']
    return  render(request,'forgot-password.html',locals())


def ajax(request):
    if request.method == 'POST':
        inp1 = request.POST.get('input1')
        inp2 = request.POST.get('input2')
        res = inp1+inp2
        d = {'sum':res}
        return  JsonResponse(d)#把字典转成json数据
    return render(request,'ajax.html')

def picture(request):
    plt.plot(np.random.randn(50).cumsum(), 'k--')
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    context = {
        'img': imd,
    }
    return render(request, 'picture.html', context)


def credit(request):
    if request.session.get('stock_id') is None:
        stock_id = '000002'
        firmname = '万科A'
    else:
        stock_id = request.session.get('stock_id')
        firmname = request.session.get('firmname')


    if request.method == 'POST':

        data = element_diag(stock_id)
        return JsonResponse(data)

    return render(request,'credit.html',{'firmname':firmname})



def pre_pos(opinion):
    s=SnowNLP(opinion)
    if s.sentiments>=0.65:
        return 1
    elif s.sentiments<=0.65 and s.sentiments>=0.35:
        return 0
    else:
        return -1

def opinion_input(request):
    if request.method == 'POST':

        jieba.load_userdict('./mystatic/sentiment/股票基金词库.txt')
        jieba.analyse.set_stop_words('./mystatic/sentiment/停用词.txt')
        stopword = pd.read_csv('./mystatic/sentiment/停用词.txt', names=['stopword'], encoding='utf-8',error_bad_lines=False)
        stopwordlist = stopword['stopword'].tolist()
        stock_id = request.POST.get('stock_id')
        date = request.POST.get('date')
        opinion = request.POST.get('opinion')
        click_num = 0
        review_num = 0
        vocabulary1 =' '.join([item for item in jieba.cut(opinion) if item not in stopwordlist])
        vocabulary2 =''.join([item for item in jieba.cut(opinion) if item not in stopwordlist])
        sentiment = pre_pos(vocabulary2)
        obj = models.enterprise_sentiment(
            click_num = click_num,
            review_num = review_num,
            opinion = opinion,
            date = date,
            stock_id = stock_id,
            vocabulary1 = vocabulary1,
            vocabulary2 = vocabulary2,
            enterprise_sentiment = sentiment
        )
        obj.save()
        print(models.enterprise_sentiment.objects.filter(date=date))


    return render(request,'opinion_input.html')

def profile(request):

    if request.method == 'POST':

        username = request.session.get('username')
        nickname = request.POST.get('nickname')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        institute = request.POST.get('institute')
        img = request.FILES.get('img')
        img_src = '/static/images/profiles/'+username+'.jpg'
        current_path =os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/')#获取E:/上财文件1/大四上/二专毕业设计/project/app01
        print(current_path)

        with open(current_path+'/mystatic/images/profiles/'+username+'.jpg','wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
            f.close()


        if models.user_info.objects.filter(user = username):#如果数据库里存在该用户信息
            models.user_info.objects.filter(user = username).update(nickname=nickname,age=age,phone=phone,institute=institute,img_src=img_src)
        else:
            d = dict(user = username,nickname=nickname,age=age,phone=phone,institute=institute,img_src=img_src)
            obj = models.user_info.objects.create(**d)
        img_src = models.user_info.objects.get(user = username).img_src
        return render(request,'profile.html',locals())


    return render(request,'profile.html')