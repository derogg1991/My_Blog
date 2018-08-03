project name = MYblog
Python=3.5.2
部署流程:
1. 调整settings关于数据库的设定
2. source venv
3. pip install -r requirements.txt
4. makemigrations && migrate
5. uwsgi启动
6. nginx启动

### 本博客源自教程:https://www.zmrenwu.com/post/2/
