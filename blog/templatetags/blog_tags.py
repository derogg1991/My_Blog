from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

# 实例化
register = template.Library()

# 最新文章标签
# 实例化后调用方法再作为装饰器使用


@register.simple_tag
def get_recent_posts(num=5):
	# 在models的Post类中默认返回title，这里根据时间排序，提取它的前5个标题
	return Post.objects.all().order_by('-created_time')[:num]


# 归档模版标签
@register.simple_tag
def archives():
	# dates方法会返回一个列表，里面的元素是每一篇文章的创建时间。而且是python的date对象，精确到月，降序排列。
	return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模版标签
@register.simple_tag
def get_categorys():
	# Category.objects.annotate 方法会返回数据库中所有 Category 记录,同时统计返回的 Category 记录集合中每条记录的文章数(Count)
	# Count 接受一个和 Category 相关联的模型参数名(这里是 Post 通过 ForeignKey 关联),然后它会统计 Category 记录集合中每条记录下
	# 与之相关联的 Post 记录的行数,把值保存在 num_posts 中
	# 此外还做一个过滤 num_posts 小于1的说明有分类没文章,就不显示
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tag_list():
	tag_list = Tag.objects.all()
	return tag_list
