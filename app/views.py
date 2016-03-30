from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, AddCookie
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template("index.html",
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # receiving form data
    if form.validate_on_submit(): # this validates the data (makes sure it's appropriate for the applciation)
        # flash displays data to the user on the next page
        # flash('Login requested for OpenID="%s", remember_me=%s' %
        #      (form.openid.data, str(form.remember_me.data)))
        session['remember_me'] = form.remember_me.data
        session['rfid_tag'] = form.rfid_tag.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

#@app.route('/select', methods=['GET', 'POST'])
#def select(tag):
#    db = connect_db()
#    cur = db.execute("SELECT * FROM db WHERE rfid = tag")
#    return cur

@app.route('/add/<tag>', methods=['GET', 'POST'])
def add(tag):
    user = User.query.filter_by(rfid=tag).first()
    if user is None:
        flash('Sorry, no user has that tag...')
        return redirect(url_for('index'))
    user.cookies = user.cookies + 1
    db.session.commit()
    #db.engine.execute("UPDATE User SET cookies = cookies + 1 WHERE nickname='li.joey96'")
    return redirect(url_for('index'))

@app.route('/verify/<tag>', methods=['GET', 'POST'])
def verify(tag):
    user = User.query.filter_by(rfid=tag).first()
    if user is None:
        return render_template('404.html')
    return jsonify(nickname=user.nickname, cookies=user.cookies)

@app.route('/reset/<tag>', methods=['GET', 'POST'])
def reset(tag):
    user = User.query.filter_by(rfid=tag).first()
    if user is None:
        flash('No user has that tag.')
        return redirect(url_for('index'))
    user.cookies = 0
    db.session.commit()
    #db.engine.execute("UPDATE User SET cookies = 0 WHERE nickname='li.joey96'")
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        if session['rfid_tag'] == "":
            flash('Please enter an RFID tag.')
            return redirect(url_for('login'))
        nickname = resp.nickname
        nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, rfid=session['rfid_tag'])
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

    
