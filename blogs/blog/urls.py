from django.conf.urls import url
from . import views
from haystack.views import SearchView
from .feed import BlogFeed
app_name = 'blog'
urlpatterns = [

    url(r'^detail/(\d+)/$',views.detail,name='detail'),
    url(r'^archives/(\d+)/(\d+)/$',views.archives,name='archives'),
    url(r'^search/$',SearchView(),name='search'),
    url(r'^category/(\d+)/$',views.category,name='category'),
    url(r'^tag/(\d+)/$',views.tag,name='tag'),
    url(r'^rss/$',BlogFeed(),name='rss'),
    url(r'^contactus/$',views.Contacts.as_view(),name='contactus'),
    # url(r'^contactus/$',views.contactus,name='contactus'),
    url(r'^addads/$',views.Ads.as_view(),name='addads'),
    # url(r'^$'),
    url(r'^$',views.index,name='index'),
]