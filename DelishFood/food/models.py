from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30,verbose_name='用户名')
    pwd = models.CharField(max_length=30,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    class Meta():
        verbose_name = '用户'
        verbose_name_plural = verbose_name
class Reserve(models.Model):
    time = models.TimeField(verbose_name='时间')
    date = models.DateField(verbose_name='日期')
    num = models.CharField(max_length=30,verbose_name='人数')
    user= models.ForeignKey(User,models.CASCADE)
    class Meta():
        verbose_name = '预定'
        verbose_name_plural = verbose_name

