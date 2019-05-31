from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Article
from django.core.paginator import Paginator

# Create your views here.
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
    return render(request,'single.html',locals())

