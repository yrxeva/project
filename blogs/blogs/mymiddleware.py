'''
自定义中间件
'''
class Mymiddleware():
    def __init__(self,_get_response):
        self.get_response = _get_response
    def __call__(self, request):
        print('截取到请求：', request)
        response = self.get_response(request)
        print('截取响应', response)
        # return response
        from django.http import HttpResponse
        return HttpResponse('123')