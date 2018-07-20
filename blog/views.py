import markdown
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from django.views.generic import ListView

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


# def posts(request):
#     post_list = Post.objects.all()
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'blog/full-width.html', context=context)
class PostsViews(ListView):
    model = Post
    template_name = 'blog/full-width.html'
    context_object_name = 'post_list'


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


# 根据从url中捕获的id（pk）获取数据库中文章的id
def detail(request, pk):
    # 传入的pk在数据库中存在就返回对应的post，不存在就返回404
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.increase_views()
    # extensions允许markdown支持额外的扩展，extra更多的扩展，codehilite代码高亮，toc自动生成目录
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
        'form': form,
        'comment_list': comment_list,
    }
    return render(request, 'blog/detail.html', context=context)


# 归档页面
# def archives(request, year, month):
#   # created_time是django的date对象，里面有__year和__month属性，python调用类的属性一般是created_time.year
#   # 但是这里作为参数传入，django规定要用__替代.
#   post_list = Post.objects.filter(created_time__year=year,
#                                   created_time__month=month
#                                   ).order_by('-created_time')
#   # 因为归档下的文章列表显示和主页是一样的，所以直接渲染index.html
#   return render(request, 'blog/index.html', context={'post_list': post_list})
class ArchivesViews(ListView):
    model = Post
    template_name = 'blog/full-width.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesViews, self).get_queryset().filter(created_time__year=year,
                                                                created_time__month=month
                                                                ).order_by('-created_time')

# 分类页面,这里的pk是被访问分类的id
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


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
