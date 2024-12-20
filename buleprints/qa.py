from flask import Blueprint, request, render_template, redirect, url_for,g

from buleprints.forms import QuestionForm, AnswerForm
from exts import db
from models import QuestionModel, AnswerModel
from 代码.zhiliaooa.decorators import login_required

bp = Blueprint("qa", __name__,url_prefix="/")
# 首页
# http://127.0.0.1:5000
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


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

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)

# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id) )
    else:
        print(form.errors)
        return redirect(url_for("qa.qa.detail",qa_id=request.form.get("question_id")) )


@bp.route("/search")
def search():
    """
    处理搜索请求的视图函数。

    该函数从查询参数中获取搜索关键词，然后从数据库中查询包含该关键词的问题，
    最后将查询结果渲染到模板中并返回。
    """
    # /search?q=flask
    # /search/<q>
    # post, request.from

    # 从查询参数中获取搜索关键词
    q = request.args.get("q")

    # 使用SQLAlchemy查询包含搜索关键词的问题
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()

    # 渲染模板并将查询结果传递给模板
    return render_template("index.html", questions=questions)