from haystack import indexes
from .models import Post

'''
这是 haystack 的规定,要在某个 app 下进行全文搜索,就要在该 app 下创建一个search_indexes.py 的文件
然后创建一个 XXIndex 的类,(XX为含有被检索数据的模型),并且继承 SearchIndex 和 indexes.Indexable 类
'''
class PostIndex(indexes.SearchIndex, indexes.Indexable):
	# 每个索引里面必须有且只有一个字段为 document=True,这代表 haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)
	# text 是一般约定名,是 SearchIndex 类里面的一贯命名,不建议改
	# use_template=True 允许我们使用数据模板去建立搜索引擎索引的文件,通俗地讲就是索引里面需要存放一些什么东西,例如 Post 的 Title字段
	# 这样我们可以通过 title 的内容来检索 Post数据.
	# 举个例子，假如你搜索 Python ，那么就可以检索出 title 中含有 Python 的Post了，怎么样是不是很简单？
	text = indexes.CharField(document=True, use_template=True)
	'''
	数据模板的路径为 templates/search/indexes/youapp/\<model_name>_text.txt（例如 templates/search/indexes/blog/post_text.txt），
	其内容为：

	templates/search/indexes/blog/post_text.txt

	{{ object.title }}
	{{ object.body }}

	这个数据模板的作用是对 Post.title、Post.body 这两个字段建立索引，当检索的时候会对这两个字段做全文检索匹配，
	然后将匹配的结果排序后作为搜索结果返回。
	'''

	def get_model(self):
		return Post


	def index_queryset(self, using=None):
		return self.get_model().objects.all()