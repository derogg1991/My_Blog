# coding:UTF-8

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Post(models.Model):
	#标题
	title = models.CharField(max_length=100)
	#文章
	body = models.TextField()
	#创建时间
	created_time = models.DateTimeField()
	#修改时间
	modified_time = models.DateTimeField()
	#文章摘要
	excerpt = models.CharField(max_length=200, blank=True)
	#分类，一对多
	category = models.ForeignKey(Category)
	#标签，多对多
	tag = models.ManyToManyField(Tag)
	#作者，一对多
	author = models.ForeignKey(User)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		#blog应用下的name=detail（urls.py）,pk在这里就是id
		#找到对应视图函数，传入参数pk替换urls中的正则表达式，再返回，生成POST自己的URL
		return reverse('blog:detail', kwargs={'pk': self.pk})
	#django允许我们在models.Model的子类里定义一个Meta内部类
	class Meta:
		'''
		这个内部类通过指定一些属性来规定这个类该有的一些特性
		ordering属性用来指定文章的排序方式，先按照created_time的反序排列，created_time相同再按照标题排序
		'''
		ordering = ['-created_time', 'title']