from flask import Blueprint, request, render_template, redirect, url_for,g

from buleprints.forms import QuestionForm
from exts import db
from models import QuestionModel
from 代码.zhiliaooa.decorators import login_required

bp = Blueprint("qa", __name__,url_prefix="/")
# 首页
# http://127.0.0.1:5000
@bp.route("/")
def index():
   return "这是首页 "


@bp.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))