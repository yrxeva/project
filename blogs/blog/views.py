from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse
from .models import Article,Category,Tag,Ads as AdsModel
from django.core.paginator import Paginator
import markdown
from comments.forms import CommentForm
from django.views.generic import View
from .forms import ContactForm
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings

# 导入缓存
from django.views.decorators.cache import cache_page
# Create your views here.
# @cache_page(30)  #n分钟后删除缓存
def index(request):
    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum==None else pagenum

    articles = Article.objects.all().order_by('-views')
    # 返回分页器，每页显示一个
    paginator = Paginator(articles,1)
    # 根据传入页码获取页面
    page = paginator.get_page(pagenum)
    return render(request,'index.html',{'page':page})
def detail(request,id):
    article = get_object_or_404(Article,pk=id)
    article.views+=1
    # 确保body字段没被更改
    article.save()
    # 方法一：针对需要处理的article.body将markdown转换为html
    # article.body = markdown.markdown(article.body,extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',#给代码块高亮
    #     'markdown.extensions.toc',#生成自动目录
    # ])
    # 方法二：使用构造函数的写法，以便能够在外部使用目录
    mk = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.body = mk.convert(article.body)
    article.toc = mk.toc    #在外部生成自动目录
    # 生成表单
    cf = CommentForm()
    return render(request,'single.html',locals())

# 归档,根据年月归档
def archives(request,year,month):
    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum == None else pagenum
    #属性名__比较类型=
    articles = Article.objects.filter(create_time__year=year,
    create_time__month=month)
    paginator = Paginator(articles,1)
    #传入页码得到页面，page包含所有信息
    page = paginator.get_page(pagenum)
    page.parms = "/archives/%s/%s/"%(year,month)
    return render(request,'index.html',{'page':page})

# 分类
def category(request,id):
    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum==None else pagenum
    articles = get_object_or_404(Category,pk=id).article_set.all()
    paginator = Paginator(articles,1)
    page = paginator.get_page(pagenum)
    page.parms = '/category/%s'%(id,)
    return render(request,'index.html',{'page':page})

# 标签云
def tag(request,id):
    pagenum = request.GET.get("page")
    pagenum = 1 if pagenum == None else pagenum
    articles = get_object_or_404(Tag, pk=id).article_set.all()
    paginator = Paginator(articles, 1)
    # 传入页码得到一个页面   page包含所有信息
    page = paginator.get_page(pagenum)
    page.parms = "/tag/%s/"%(id,)
    return render(request, 'index.html', {"page": page})

# class Contacts(View):
#     def get(self,request):
#         cf = ContactForm()
#         return render(request,'contact.html',locals())
#     def post(self,request):
#         #向hr发送邮件
#         try:
#             send_mail("测试邮件", "请点击  <a href='http://127.0.0.1:8000/'>首页</a>", settings.DEFAULT_FROM_EMAIL,
#                       ["2356163184@qq.com","eva@liveme.uu.me"])
#             print('here')
#             # send_mass_mail((("测试邮件1", "邮件1", settings.DEFAULT_FROM_EMAIL, ["zhangzhaoyu@qikux.com", "496575233@qq.com"]),
#             #                ("测试邮件2", "邮件2", settings.DEFAULT_FROM_EMAIL, [ "496575233@qq.com"]),
#             #                ("测试邮件3", "邮件3", settings.DEFAULT_FROM_EMAIL, ["zhangzhaoyu@qikux.com"])))
#         except Exception as e:
#             print(e)
#
#         cf = ContactForm(request.POST)
#         cf.save()
#         cf = ContactForm()
#         return render(request,'contact.html',{'info':'成功','cf':cf})
# def contactus(request):
#     return render(request,'contact.html')
class Contacts(View):
    def get(self,request):
        cf = ContactForm()
        return render(request, 'contact.html',locals())
    def post(self,request):
        # 向HR发送邮件
        try:
            send_mail("测试邮件", "请点击  <a href='http://127.0.0.1:8000/'>首页</a>", settings.DEFAULT_FROM_EMAIL,
                      ["2356163184@qq.com", "eva@liveme.uu.me"])
            # send_mass_mail((("测试邮件1", "邮件1", settings.DEFAULT_FROM_EMAIL, ["zhangzhaoyu@qikux.com", "496575233@qq.com"]),
            #                ("测试邮件2", "邮件2", settings.DEFAULT_FROM_EMAIL, [ "496575233@qq.com"]),
            #                ("测试邮件3", "邮件3", settings.DEFAULT_FROM_EMAIL, ["zhangzhaoyu@qikux.com"])))
        except Exception as e:
            print(e)

        cf = ContactForm(request.POST)
        cf.save()
        cf = ContactForm()
        return render(request, 'contact.html', {"info":'成功1',"cf":cf})

class Ads(View):
    def get(self,request):
        return render(request,'addads.html')
    def post(self,request):
        img = request.FILES['img']
        desc = request.POST.get('desc')
        ad = AdsModel(img=img,desc=desc)
        ad.save()
        return redirect(reverse('blog:index'))