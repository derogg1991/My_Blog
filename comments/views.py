#redirect将http请求重定向，可以接受一个URL作为参数也可以接受一个实例，如果接受实例，实例必须实现了get_absolute_url方法。
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
	#先获取文章，存在则返回，不存在就404
	post = get_object_or_404(Post, pk=post_pk)

	if request.method == 'POST':
		#用户提交的数据存在request.POST中，这是一个类字典对象，利用这些数据构造CommentForm实例，这样django表单就生成了
		form = CommentForm(request.POST)
		#检测表单的数据是否复合要求
		if form.is_valid():
			#表单数据合法，就save(),commit=False意思是仅利用数据生成模型，不保存到数据库中
			comment = form.save(commit=False)
			#将评论和文章关联起来
			comment.post = post
			#最终将数据保存进数据库
			comment.save()
			#重定向到post页，实际上redirect接受一个模型实例的时候，他会调用这个模型实例的get_absolute_url方法
			#然后重定向到get_absolute_url得到的url
			return redirect(post)
		else:
			#检测到数据不合法，重新渲染详情页，并且渲染表单的错误，因此我们传了三个模版变量给detail.html，一个是文章，一个评论列表，
			#一个是表单form.post.comment_set.all()方法有点类似于Post.objects.all(),作用是获取这post下的全部评论，因为post和
			#comment是ForeignKey关联的，所以使用post.comment_set.all()反向查找所有评论。
#--post.comment_set.all()--
#	回顾下获取某个分类cate下的所有文章：Post.objects.filter(category=cate),这里的post.comment_set.all()等价于
#	Comment.objects.filter(post=post),即根据post过滤该post下所有评论。
#	既然我们已经有了Post模型的实例post（它对应的是Post在数据库中的一条记录），那么获取和post关联的评论列表的一个简单方法，即调用它
#	的xxx_set属性来获取一个类似objects的模型管理器，然后调用all()方法返回这个post关联的全部评论。其中xxx_set中的xxx为关联模型的类名
#	（小写）。例如Post.objects.filter(category=cate)也可以等价写为cate.post_set.all()
			comment_list = post.comment_set.all()
			#comment_list = Comment.objects.filter(post=post)
			context = {
			'post': post,
			'form': form,
			'comment_list': comment_list,
			}
			return render(request, 'blog/detail.html', context=context)
		#不是post请求，说明用户没有提交数据，直接重定向到post
	return redirect(post)
