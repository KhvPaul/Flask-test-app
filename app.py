from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

    def get_formatted_post_date(self):
        if self.date.day == datetime.now().day:
            return f"{self.date.strftime('%H:%M:%S')}"
        if self.date.day == datetime.now().day - 1:
            return f"tomorrow at {self.date.strftime('%H:%M:%S')}"
        if self.date.day - datetime.now().day - 1 <= 7:
            return f"{self.date.day - datetime.now().day}" \
                   f" days ago at {self.date.strftime('%H:%M:%S')}"[1:]
        else:
            return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')}"


@app.route('/')
@app.route('/home')
def index():  # put application's code here
    return render_template('blog/index.html')


@app.route('/about')
def about():  # put application's code here
    return render_template('blog/about.html')


@app.route('/articles')
def get_articles():  # put application's code here
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('blog/articles.html', articles=articles)


@app.route('/articles/<int:article_id>')
def get_article(article_id):  # put application's code here
    article = Article.query.get(article_id)
    return render_template('blog/article_detail.html', article=article)


@app.route('/create-article', methods=["POST", "GET"])
def create_article():  # put application's code here
    if request.method == "POST":
        title = request.form['article-title']
        intro = request.form['article-intro']
        text = request.form['article-text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('get_article', article_id=article.id))
        except:
            return "Error on article creation"
    else:
        return render_template('blog/article_form.html')


@app.route('/articles/<int:article_id>/update', methods=["POST", "GET"])
def update_article(article_id):  # put application's code here
    article = Article.query.get_or_404(article_id)
    if request.method == "POST":
        article.title = request.form['article-title']
        article.intro = request.form['article-intro']
        article.text = request.form['article-text']

        try:
            db.session.commit()
            return redirect(url_for('get_article', article_id=article_id))
        except:
            return "Error on article creation"
    else:

        return render_template('blog/article_form.html', article=article)


@app.route('/articles/<int:article_id>/delete', methods=["POST", "GET"])
def delete_article(article_id):  # put application's code here
    if request.method == "POST":
        article = Article.query.get_or_404(article_id)
        try:
            db.session.delete(article)
            db.session.commit()
            print('HERE')
            return redirect(url_for('get_articles'))
        except:
            return "Error on article creation"
    else:
        return render_template('blog/article_delete.html', article=Article.query.get_or_404(article_id))


if __name__ == '__main__':
    app.run(debug=True)
