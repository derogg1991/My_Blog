import markdown
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.


# def index(request):
#     post_list = Post.objects.all()
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'blog/index.html', context=context)
class IndexViews(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	# 指定 paginate_by 属性后开启分页功能,其值代表每一页包含的文章数
	paginate_by = 5

	def get_context_data(self, **kwargs):
		'''
		在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的,
		例如 render(request, 'blog/index.html', context={'post_list': post_list}),
		这里传递了一个 {'post_list': post_list} 字典给模板.
		在类视图中,这个需要传递的模板变量字典是通过 get_context_data 方法获得的,
		所以我们覆写该方法,以便我们能够自己再插入一些我们自定义的变量进去.
		'''

		# 首先获得父类生成的传递给模板的字典
		context = super().get_context_data(**kwargs)

		'''
		父类生成的字典中已有了 paginator/page_obj/is_paginated 这三个模板变量
		paginator 是 Paginator 的一个实例(分页实例)
		page_obj 是 Page 的一个实例(当前分页实例)
		is_paginated 是一个布尔变量,指示是否分页
		由于 context 是一个字典,所以用 get 方法从中取出某个键对应的值
		'''
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		# 调用自己写的 pagination_data 方法获得显示分页导航条需要得数据
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		# 将分页导航条的模板变量更新到 context 中,注意 pagination_data 方法返回的也是一个字典
		context.update(pagination_data)

		# 将更新后的 context 返回,以便 ListView 使用这个字典中的模板变量去渲染模板.
		# 注意此时 context 字典中已有了显示分页导航条所需的数据
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}
		# 当前页左边连续的页码号,初始值为空
		left = []
		# 当前页右边连续的页码数,初始值为空
		right = []
		# 标示第一页页码后是否需要显示省略号
		left_has_more = False
		# 标示最后一页页码前是否需要显示省略号
		right_has_more = False
		# 标示是否需要显示最后一页页码号
		# 因为如果当前页左边的连续页码中已经含有第一页的页码,此时就无需再显示第一页的页码了
		# 其他情况下第一页页码默认显示
		# 初始值为 False
		first = False
		# 同上,标示变量
		last = False

		# 获得用户当前请求的页码数
		page_number = page.number

		# 获得分页后的总页数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表, 比如分了4页,那就是[1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:
			'''
			如果用户当前请求第一页,那么当前页左边就不需要数据,因此left = [](默认)
			此时只需要获取当前页右边的连续页码数, right = [2, 3, 4, 5]
			后面的数字表示截取的范围
			'''
			right = page_range[page_number:page_number + 2]

			# 如果最右边的页码号比最后一页的页码号减去1还要少,
			# 说明最右边的页码号和最后一页的页码号之间还有其他页码,因此需要省略号,通过 right_has_more 来指示

			if right[-1] < total_pages - 1:
				right_has_more = True

			# 如果最右边的页码比最后一页的页码小,说明当前页右边的连续页码中不包含最后一页页码
			# 所以需要显示最后一页的页码,用 last 来标示

			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			'''
			如果用户请求的是最后一页的数据,那么当前页右边就不需要数据,因此 right = []
			此时只要获取左边的联系页码
			截取左边连续2个页码,如果剩下的页码数不足2个,则从头开始截取
			'''
			left = page_range[(page_number - 3)
							  if (page_number - 3) > 0 else 0:page_number - 1]

			# 如果最左边的页码比第2页的页码大,说明当前页左边需要省略号
			if left[0] > 2:
				left_has_more = True

			# 如果最左边的页码比第一页大,说明需要显示第一页页码
			if left[0] > 1:
				first = True

		else:
			# 用户请求的既不是第一页也不是最后一页,怎需要显示两边的页码
			left = page_range[(page_number - 3)
							  if (page_number - 3) > 0 else 0:page_number - 1]

			right = page_range[page_number:page_number + 2]

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第一页和第一页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}

		return data


# def posts(request):
#     post_list = Post.objects.all()
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'blog/full-width.html', context=context)
class PostsViews(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'


def about(request):
	return render(request, 'blog/about.html')


def contact(request):
	return render(request, 'blog/contact.html')


# 根据从url中捕获的id（pk）获取数据库中文章的id
# def detail(request, pk):
# 	# 传入的pk在数据库中存在就返回对应的post，不存在就返回404
# 	post = get_object_or_404(Post, pk=pk)
# 	# 阅读量+1
# 	post.increase_views()
# 	# extensions允许markdown支持额外的扩展，extra更多的扩展，codehilite代码高亮，toc自动生成目录
# 	post.body = markdown.markdown(post.body,
# 								  extensions=[
# 									  'markdown.extensions.extra',
# 									  'markdown.extensions.codehilite',
# 									  'markdown.extensions.toc',
# 								  ])
# 	form = CommentForm()
# 	comment_list = post.comment_set.all()
# 	context = {
# 		'post': post,
# 		'form': form,
# 		'comment_list': comment_list,
# 	}
# 	return render(request, 'blog/detail.html', context=context)
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	# 可以简单地认为是 detail 视图函数的调用
	def get(self, request, *args, **kwargs):
		'''
		覆写此方法的目的是因为每当文章被访问一次,阅读量就+1
		get 方法返回一个 HttpResponse 实例
		之所以要调用父类的 get 是因为只有当 get 被调用后才有 self.object属性,其值为 Post 模型实例,即被访问的文章 post
		'''
		responese = super(PostDetailView, self).get(request, *args, **kwargs)

		# 将文章阅读量+1 self.object 就是被访问的文章
		self.object.increase_views()

		# 视图必须返回一个 HttpResponse 对象
		return responese

	# 对应 detail 视图函数中根据 pk(id) 获取文章,然后对文章的 post.body 进行 markdown 渲染
	def get_object(self, queryset=None):
		# 覆写 get_object 方法为了对 post.body 进行 markdown 渲染
		post = super(PostDetailView, self).get_object(queryset=None)
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			TocExtension(slugify=slugify)
		])

		post.body = md.convert(post.body)
		post.toc = md.toc

		return post

	def get_context_date(self, **kwargs):
		# 覆写 get_context_date 方法,因为除了要把 post 传给模板( DetailView 已经帮我们完成)之外,还要把评论表单,post 下的传过去
		context = super(PostDetailView, self).get_context_date(**kwargs)
		form = CommentForm()
		comment_list = self.object.comments_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list
		})
		return context


# 归档页面
'''
def archives(request, year, month):
  # created_time是django的date对象，里面有__year和__month属性，python调用类的属性一般是created_time.year
  # 但是这里作为参数传入，django规定要用__替代.
  post_list = Post.objects.filter(created_time__year=year,
								  created_time__month=month
								  ).order_by('-created_time')
  # 因为归档下的文章列表显示和主页是一样的，所以直接渲染index.html
  return render(request, 'blog/index.html', context={'post_list': post_list})
'''


class ArchivesViews(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesViews, self).get_queryset().filter(created_time__icontains="%s-0%s" %(year, month)).order_by('-created_time')


'''
分类页面,这里的pk是被访问分类的id
def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})
'''


class CategoryViews(ListView):
	model = Post
	template_name = 'blog/full-width.html'
	context_object_name = 'post_list'

	# 复写 ListView 的 get_queryset 方法，该方法默认返回制定 model 的全部列表数据
	def get_queryset(self):
		# 首先根据 url 捕获的分类 id（pk）获取分类，在类视图中，捕获的命名组参数值保存在实例的 kwargs 属性中（字典）
		# 非命名组参数保存在 agrs（列表）中,所以使用 self.kwargs.get()获取pk值。
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		# 调用父类的 get_queryset()获取全部列表数据，然后再 filter()
		return super(CategoryViews, self).get_queryset().filter(category=cate)


# 作者页面跟分类类似
def author(request, pk):
	post_list = Post.objects.filter(author=pk)
	return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	post_list = Post.objects.filter(tag=tag)
	return render(request, 'blog/index.html', context={'post_list': post_list})
