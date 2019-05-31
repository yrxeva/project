from django.conf.urls import url
from . import views
app_name = 'food'
urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^single/$',views.single,name='single'),
    url(r'^gallery/$',views.show,name='show'),
    url(r'^about/$',views.about,name='about'),
    url(r'^login/$',views.login,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^reserve/$',views.reserve,name='reserve'),


]