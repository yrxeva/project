from django.shortcuts import render,redirect,reverse,get_object_or_404
from .models import Question,Choice,MyUser
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
from .util import checklogin
# 登录授权，登录，登出
from django.contrib.auth import authenticate,login as lgi,logout as lgo
# Create your views here.

# class Login(View):
#     def get(self,request):
#         return render(request,'polls/login.html')
#     def post(self,request):
#         username= request.POST.get('username')
#         if username == 'abc':
#             # 登录成功后，应将用户信息保存到cookie
#             res = redirect(reverse('polls:index'))
#             res.set_cookie('username',username)
#             return res
#         else:
#             return render(request,'polls/login.html',{'error':'用户名错误'})

def login(request):
    # 没有引入数据库
    # if request.method=='GET':
    #     return render(request, 'polls/login.html')
    # else:
    #     username = request.POST.get('username')
    #     if username == 'abc':
    #         # 登录成功后，应将用户信息保存到cookie
    #         res = redirect(reverse('polls:index'))
    #         # cookie缓存
    #         # res.set_cookie('username',username)
    #         # session缓存
    #         request.session['username'] = username
    #         return res
    #     else:
    #         return render(request,'polls/login.html',{'error':'用户名错误'})

    # 使用数据库存取数据
    if request.method == 'GET':
        return render(request, 'polls/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        lgi(request,user)
        return redirect(reverse('polls:index'))

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
        error = None
        if password != password2:
            error = '两次输入密码不一致'
            print('cuowu:', error)
            return render(request,'polls/login.html',{'error':error})
        else:
            MyUser.objects.create_user(username=username,password=password
                                       ,url='http:google.com')
            return redirect(reverse('polls:login'))


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



