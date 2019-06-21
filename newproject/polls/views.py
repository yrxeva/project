from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Question,Choice,MyUser
from .util import checklogin
from django.views.generic import View
from django.contrib.auth import authenticate,login as lgi,logout as lgo
# from .forms import LoginForm,RegisterForm
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from PIL import Image,ImageDraw,ImageFont
import random,io
from django.core.cache import cache
# 引入序列化加密并且有效期信息
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'polls/login.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = get_object_or_404(MyUser,username=username)
        print('active:',user.is_active)
        if not user.is_active:
            return render(request,'polls/login.html',{'error':'用户尚未激活'})
        else:
            check = user.check_password(pwd)
            if check:
                lgi(request,user)
                return redirect(reverse('polls:index'))
            else:
                return render(request,'polls/login.html',{'error':'用户名或密码错误'})


def logout(request):
    # res = redirect(reverse('polls:login'))
    # res.delete_cookie('username')
    # request.session.flush()
    # return res

    # 调用登出方法
    res = redirect(reverse('polls:login'))
    lgo(request)
    return res

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username_reg')
        password = request.POST.get('inputPassword3_reg')
        password2 = request.POST.get('inputPassword3_reg2')
        email = request.POST.get('email')
        error = None
        if password != password2:
            error = '两次输入密码不一致'
            return render(request,'polls/login.html',{'error':error})
        else:
            user = MyUser.objects.create_user(username=username,password=password,url = 'http://laji.com')
            # 设置账号为非激活状态，使用邮箱激活
            user.is_active=0
            user.save()
            # 加密用户id信息，防止非人为激活
            #1得到序列化工具
            # settings.SECRET_KEY为每一个django项目提供的一个密钥
            # Serializer的参数为密钥和过期时间，默认1小时，单位秒，序列化和反序列化密钥时间都要一致
            serutil = Serializer(settings.SECRET_KEY,3600)
            # 2使用工具对字典进行对象序列化
            result = serutil.dumps({'userid':user.id}).decode('utf-8')
            print('result:', result, type(result))

            url = "http:127.0.0.1:8000/polls/active/%s"%(result)
            mail = EmailMultiAlternatives("点击激活","<a href='http:127.0.0.1:8000/polls/active/%s'>点击激活</a><p>手动点击链接%s</p>"%(result,url),
            settings.DEFAULT_FROM_EMAIL, [email])
            mail.content_subtype='html'
            mail.send()
            return render(request,'polls/login.html',{"error":"请在一个小时内激活"})
def active(request,info):
    serutil = Serializer(settings.SECRET_KEY, 3600)
    # 检查过期时间
    try:
        # 反序列化
        obj = serutil.loads(info)
        print('obj:',obj['userid'])
        id = obj['userid']
        user= get_object_or_404(MyUser,pk=id)
        user.is_active = 1
        user.save()
        return redirect(reverse('polls:login'))
    except SignatureExpired as e:   #itsdnagrous自带错误函数
        return HttpResponse('已过期')

# 验证码
def verify(request):
    # 每次请求验证码，都要使用pillow构造出图像，返回
    # 定义变量，用于画面的背景色，宽高
    bgcolor = (random.randrange(20,100),
               random.randrange(20,100),
               random.randrange(20,100),)
    width = 100
    heigth = 35
    # 创建画面对象
    im = Image.new('RGB',(width,heigth),bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 使用画笔的point()函数绘制噪点
    for i in range(0,500):
        # 随机位置
        xy = (random.randrange(0,width),
              random.randrange(0,heigth))
        # 随机颜色
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        # 填充
        draw.point(xy,fill=fill)
    # 验证码内容
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0,4):
        rand_str += str1[random.randrange(0,len(str1))]
    print(rand_str)
    # 构造字体对象
    font = ImageFont.truetype('cambriab.ttf',23)
    fontcolor = (255,random.randrange(0,255),
                 random.randrange(0,255))
    # 绘制字体
    draw.text((5,2),rand_str[0],font=font,fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw

    cache.set('verifycode',rand_str,500)
    f = io.BytesIO()
    im.save(f,'png')
    return HttpResponse(f.getvalue(),'image/png')

# ajax异步刷新
def checkuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        print(username)
        if MyUser.objects.filter(username = username).first():
            return JsonResponse({"state":1})
        else:
            return JsonResponse({"state":0, "error":"用户不存在"})

@checklogin
def index(request):
    username = request.session.get('username')
    questions = Question.objects.all()
    return render(request,'polls/index.html',locals())
@checklogin
def detail(request,id):
    # print(request.path)
    # print(request.method)
    # print(request.GET['name']),出错，会报错
    # print(request.GET.get('name')),出错，不会报错
    question = Question.objects.get(pk=id)
    if request.method == 'POST':
        # 投票成功后，获取投票选项，+1
        # 通过detail.html获得表单，中选项的id
        # 下面的choice为选项名字，由名字获得id
        c_id = request.POST['choice']
        Choice.objects.incresevotes(c_id)
        # 重定向到结果页
        # 简写，解除硬编码
        return redirect(reverse('polls:result',args=(id,)))
        # return HttpResponseRedirect('/polls/result/%s/'%(id,))
    return render(request,'polls/detail.html',locals())
@checklogin
def result(request,id):
    question = Question.objects.get(pk=id)
    return render(request,'polls/result.html',locals())



