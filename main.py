from flask import Flask, render_template, redirect, abort, request
from data import db_session
from data.users import User
from data.ads import Ads
from forms.user import RegisterForm, LoginForm
from forms.ad import AdsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/ads.db")
    app.run()


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    ads = db_sess.query(Ads)
    return render_template("index.html", ads=ads)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = AdsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ads = Ads()
        ads.title = form.title.data
        ads.author = form.author.data
        ads.genre = form.genre.data
        ads.about = form.about.data
        ads.publisher = form.publisher.data
        ads.year = form.year.data
        current_user.news.append(ads)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ads.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = AdsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ads = db_sess.query(Ads).filter(Ads.id == id, Ads.user == current_user).first()
        if ads:
            form.title.data = ads.title
            form.author.data = ads.author
            form.genre.data = ads.genre
            form.about.data = ads.about
            form.publisher.data = ads.publisher
            form.year.data = ads.year
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ads = db_sess.query(Ads).filter(Ads.id == id, Ads.user == current_user).first()
        if ads:
            ads.title = form.title.data
            ads.author = form.author.data
            ads.genre = form.genre.data
            ads.about = form.about.data
            ads.publisher = form.publisher.data
            ads.year = form.year.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('ads.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ads_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Ads).filter(Ads.id == id, Ads.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
