from django.shortcuts import render,redirect,reverse,get_object_or_404
# 装饰器
# def  checklogin(fun):
#     def check(request,*args):
#         # un = request.COOKIES.get('username')
#         print(request.user, '-----')
#         un = request.session.get('username')
#         # print(un)
#         if un:
#             return fun(request,*args)
#         else:
#             return redirect(reverse('polls:login'))
#     return check

def  checklogin(fun):
    def check(request,*args):
        print(request.user, '-----')
        # 判断是否授权
        print(request.user.is_authenticated)
        if request.user and request.user.is_authenticated:
            return fun(request,*args)
        else:
            return redirect(reverse('polls:login'))
    return check