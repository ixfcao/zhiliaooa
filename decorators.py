from functools import wraps
from flask import g, redirect, url_for
# g：一个全局对象，可以在请求生命周期内存储任意数据。
# redirect：用于重定向到另一个URL。
# url_for：用于生成指定视图函数的URL。
def login_required(func):
    @wraps(func)  # 使用functools.wraps保留原函数的元信息，如名称、文档字符串等
    def inner(*args, **kwargs):
        if g.user:  # 检查g对象中是否存在user属性，即用户是否已登录
            return func(*args, **kwargs)  # 如果用户已登录，调用原函数并传递参数
        else:
            return redirect(url_for('auth.login'))  # 如果用户未登录，重定向到登录页面

    return inner  # 返回装饰后的函数

# @login_required
# def public_question(question_id):
#     pass
#
# login_required(public_question)(question_id)