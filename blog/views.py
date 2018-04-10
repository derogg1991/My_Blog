import markdown
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.contrib.auth.models import User

# Create your views here.

def index(request):
	post_list = Post.objects.all()
	context = {
	'post_list': post_list,
	}
	return render(request, 'blog/index.html', context=context)


def posts(request):
	post_list = Post.objects.all()
	context = {
	'post_list': post_list,
	}
	return render(request, 'blog/full-width.html', context=context)

def about(request):
	post_list = Post.objects.all()
	context = {
	'post_list': post_list,
	}
	return render(request, 'blog/about.html', context=context)


def contact(request):
	post_list = Post.objects.all()
	context = {
	'post_list': post_list,
	}
	return render(request, 'blog/contact.html', context=context)

#根据从url中捕获的id（pk）获取数据库中文章的id
def detail(request, pk):
	#传入的pk在数据库中存在就返回对应的post，不存在就返回404
	post = get_object_or_404(Post, pk=pk)
	#extensions允许markdown支持额外的扩展，extra更多的扩展，codehilite代码高亮，toc自动生成目录
	post.body = markdown.markdown(post.body,
		extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {
	'post': post,
	'form':form,
	'comment_list': comment_list,
	}
	return render(request, 'blog/detail.html', context=context)


#归档页面
def archives(request, year, month):
	#created_time是django的date对象，里面有__year和__month属性，python调用类的属性一般是created_time.year
	#但是这里作为参数传入，django规定要用__替代.
	post_list = Post.objects.filter(created_time__year=year,
									created_time__month=month
									).order_by('-created_time')
	#因为归档下的文章列表显示和主页是一样的，所以直接渲染index.html
	return render(request, 'blog/index.html', context={'post_list': post_list})


#分类页面,这里的pk是被访问分类的id
def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})


#作者页面跟分类类似
def author(request, pk):
	post_list = Post.objects.filter(author=pk)
	return render(request, 'blog/index.html', context={'post_list':post_list})


def tag(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	post_list = Post.objects.filter(tag=tag)
	return render(request, 'blog/index.html', context={'post_list':post_list})