from flask import render_template, redirect,url_for
from . import app,db
from .forms import URLForm
from .models import URLModel

import string
import random

def get_short():
    while True:
        short = ''.join(random.choices(string.ascii_letters + string.ascii_letters, k=6))
        if URLModel.query.filter(URLModel.short == short).first():
            continue
        return short


@app.route("/", methods=["GET", "POST"])
def index():
    form = URLForm()

    if form.validate_on_submit():
        url_model = URLModel()

        url_model.url = form.url.data
        url_model.short = get_short()

        db.session.add(url_model)
        db.session.commit()

        return redirect(url_for("urls"))

    return render_template("index.html", form=form)


@app.route("/urls")
def urls():
    urls_list = URLModel.query.all()

    return render_template("urls.html", urls_list=urls_list)


@app.route("/<string:shorts>")
def url_redirect(shorts):
    url = URLModel.query.filter(URLModel.short == shorts).first()

    if url:
        url.visits += 1

        db.session.add(url)
        db.session.commit()

        return redirect(url.url)

    return 'ERROR, DONT VALID URL'