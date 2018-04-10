from ..models import Post, Category, Tag
from django import template

#实例化
register = template.Library()

#最新文章标签
#实例化后调用方法再作为装饰器使用
@register.simple_tag
def get_recent_posts(num=5):
	#在models的Post类中默认返回title，这里根据时间排序，提取它的前5个标题
	return Post.objects.all().order_by('-created_time')[:num]


#归档模版标签
@register.simple_tag
def archives():
	#dates方法会返回一个列表，里面的元素是每一篇文章的创建时间。而且是python的date对象，精确到月，降序排列。
	return Post.objects.dates('created_time', 'month', order='DESC')


#分类模版标签
@register.simple_tag
def get_categorys():
	return Category.objects.all()


@register.simple_tag
def get_post_count(pk):
	cate = Category.objects.filter(pk=pk)
	post_count = Post.objects.filter(category=cate).count()
	return post_count


@register.simple_tag
def get_tag_list():
	tag_list = Tag.objects.all()
	return tag_list