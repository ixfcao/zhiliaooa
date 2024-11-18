import string
import random
from flask import Blueprint, render_template, request
from mako.runtime import capture


from exts import mail
from flask_mail import Message
from flask import redirect
bp = Blueprint("auth", __name__,url_prefix="/auth")

@bp.route("/login")
def login():
    return "login"


@bp.route("/register")
def register():
    return render_template("register.html")

# 验证码
@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # 4/6:数组、字母、数组和字母的组合
    source = string.digits * 4
    # 采样
    captcha =  random.sample(source, 4)
    captcha = " ".join(captcha)
    message = Message(subject="知了传课注册验证码", recipients=["2717176337@qq.com"], body=f"测试！您的验证码是：{captcha}")
    mail.send(message)

    #  验证码可以存放在缓存中 memcached/redis
    #  用数据库存储


    return "success"







@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2717176337@qq.com"], body="这是一个测试邮件")
    mail.send(message)
    return "邮件发送测试成功"