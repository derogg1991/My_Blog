# coding=UTF-8
from django.conf.urls import url
from . import views

#视图函数命名空间
app_name = 'blog'
urlpatterns = [
	url(r'^$', views.IndexViews.as_view(), name='index'),
	#(?P<pk>[0-9]+)命名捕获组，从用户访问的URL里把括号内匹配的字符串捕获并作为关键字参数传给其对应的views函数detail
	#例如用户访问past/255/，事实上detail调用时是这样：detail(request, pk=255)
	#这就是在URL中捕获文章的id
	url(r'^posts/$', views.PostsViews.as_view(), name='posts'),
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
	#括号括起来的是命名组参数，django会从用户访问的URL中提取这两个参数的值，然后传递给其对应的视图函数。
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesViews.as_view(), name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryViews.as_view(), name='category'),
	url(r'^author/(?P<pk>[0-9]+)/$', views.author, name='author'),
	url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag')
]