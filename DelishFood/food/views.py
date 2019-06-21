from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Reserve
from django.http import HttpResponse
from .models import User,Reserve
# Create your views here.

def index(request):
    name = request.session.get('username')
    if name:
        return render(request,'food/index.html',{'state':name+'已登录'})
    else:
        print('mn')
        return render(request,'food/index.html',{'state':'未登录'})
def single(request):
    if request.session.get('username'):
        return render(request,'food/single.html',{'state':'退出'})
    return render(request, 'food/single.html', {'state': '未登录'})
def show(request):
    if request.session.get('username'):
        return render(request,'food/gallery.html',{'state':'退出'})
    return render(request, 'food/gallery.html', {'state': '未登录'})
def about(request):
    if request.session.get('username'):
        return render(request,'food/about.html',{'state':'退出'})
    return render(request, 'food/about.html', {'state': '未登录'})
def login(request):
    # 判断是否已登录
    if request.session.get('username'):
        return render(request,'food/login.html',{'info':'已有账户登录'})
    if request.method == 'POST':
        email = request.POST.get('email2')
        pwd = request.POST.get('pwd2')
        print(email, pwd)
        # if User.objects.all().get(name=request.POST.get(name)):
        if not User.objects.filter(pwd=pwd):
            return render(request, 'food/login.html', {'info': '密码错误'})
        if not User.objects.filter(email=email):
            return render(request,'food/login.html',{'info':'邮箱错误'})
        name = User.objects.all().get(email=email).name
        print('name1:', name)
        request.session['username']=name
        return render(request,'food/login.html',{'info':'登录成功'})
    else:
        return render(request, 'food/login.html', {'info': ''})
    # return render(request,'food/index.html')
def register(request):
    if request.method == 'POST':
        name=request.POST.get('name1')
        email = request.POST.get('email1')
        pwd = request.POST.get('pwd1')
        print(name,pwd,email)
        # if User.objects.all().get(name=request.POST.get(name)):
        if User.objects.filter(name=name):
            return render(request, 'food/login.html', {'info': '用户名已占用'})
        if User.objects.filter(email=email):
            return render(request,'food/login.html',{'info':'邮箱已占用'})
        temp = User()
        temp.name=name
        temp.pwd=pwd
        temp.email = email
        temp.save()
        return render(request,'food/login.html',{'info':'注册成功'})
    else:
        return render(request, 'food/login.html', {'info': ''})
def logout(request):
    request.session.flush()
    return render(request,'food/index.html')
def reserve(request):
    name = request.session.get('username')
    if name:
        u = User.objects.all().get(name=name)
        # 获得该用户的所有订单
        print(type(u))
        # orders = u.reserve_set.list
        if request.method == 'POST':
            order = Reserve()
            order.time = request.POST.get('time1').replace('/',':')
            order.date = request.POST.get('date1').replace('/','-')
            order.num = request.POST.get('select1')
            order.user = User.objects.all().get(name=name)
            order.save()
            # return render(request, 'food/reserve.html',{'info':'订购成功'})
            return render(request, 'food/index.html')
        else:
            return render(request, 'food/reserve.html',{'orders':u})

    else:
        return render(request,'food/reserve.html',{'info':'请先登录'})









