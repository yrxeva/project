from django import template
from ..models import Article,Category,Tag,Ads

# 注册模板
register = template.Library()
'''
过滤器最多两个参数
标签可以有任意多个参数
'''
@register.filter(name='mylower')
def mylower(value):
    return value.lower()

@register.filter(name='myslice')
def myslice(value,length):
    return value[:length]

@register.simple_tag(name='getcategorys')
def getcategorys():
    return Category.objects.all()

# 最新文章
@register.simple_tag
def getlatestarticles(num=3):
    return Article.objects.all().order_by('-create_time')[:num]
# order_by排序，-按时间倒序排序

# 归档，按年月日排序
@register.simple_tag
def getarchives(num=3):
    #dates方法可以根据日期自动分类，并去重
    return Article.objects.dates('create_time','month',order='DESC')[:num]

# 分类
@register.simple_tag
def getcategorys():
    return Category.objects.all()

#获取标签
@register.simple_tag
def gettags():
    return Tag.objects.all()

# 显示所有图片
@register.simple_tag
def getads():
    return Ads.objects.all()

