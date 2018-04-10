from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
	class Meta:
		#表单对应数据库模型
		model = Comment
		#指明表单需要显示的字段
		fields = ['name', 'email', 'url', 'text']