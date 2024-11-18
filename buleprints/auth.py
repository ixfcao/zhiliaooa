import string
import random
from flask import Blueprint, render_template, request, jsonify, url_for
from mako.runtime import capture
from werkzeug.security import generate_password_hash

from buleprints.forms import RegisterForm
from exts import mail, db
from flask_mail import Message
from flask import redirect
from models import EmailCaptchaModel, UserModel

bp = Blueprint("auth", __name__,url_prefix="/auth")

@bp.route("/login")
def login():
    return "login"

# 2717176337@qq.com
@bp.route("/register",methods=["GET","POST"])
def register():
    # 验证用户提交的邮箱和验证码是否对应正确
    # 表单验证：flask-wtf：wtforms
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password,method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 验证码
@bp.route("/captcha/email", methods=['GET'])
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # 4/6:数组、字母、数组和字母的组合
    source = string.digits * 4
    # 采样
    captcha =  random.sample(source, 4)
    captcha = "".join(captcha)
    # I/O :Input/Output 可以用任务队列做
    message = Message(subject="知了传课注册验证码", recipients=[email], body=f"测试！您的验证码是：{captcha}")
    mail.send(message)
    #  验证码可以存放在缓存中 memcached/redis
    #  用数据库存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({
        "code": 200,
        "message": "",
        "data": None
    })



@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2717176337@qq.com"], body="这是一个测试邮件")
    mail.send(message)
    return "邮件发送测试成功"