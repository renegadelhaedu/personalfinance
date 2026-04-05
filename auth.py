from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import  ph
from dao.userdao import UserDAO
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_dao = UserDAO()


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user_dao.create_user(username=username, email=email, password=password)
        flash('Conta criada!', 'success')
        return redirect(url_for('auth.login'))  # Note o prefixo 'auth.'

    return render_template('register.html')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        user = user_dao.get_by_email(email)


        #if user and bcrypt.check_password_hash(user.password, password):
        if user:
            try:
                ph.verify(user.password, password)
                login_user(user, remember=True)

                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            except Exception:
                flash('Login inválido. Verifique seu email e senha', 'danger')

        else:
            flash('Login inválido. Verifique seu email e senha', 'danger')

    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash('Você saiu da sua conta', 'info')
    return redirect(url_for('auth.login'))