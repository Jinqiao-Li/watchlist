from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    #  http://localhost:5000/test：
    print(url_for('hello'))  # output：/
    print(url_for('user_page', name='greyli'))  # output：/user/greyli
    print(url_for('user_page', name='peter'))  # output：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # output：/test?num=2
    return 'Test page'

