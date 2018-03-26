from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from . import auth
from ...models import User
from .forms import ChangeEmailForm
from .forms import ChangePasswordForm
from .forms import LoginForm
from .forms import PasswordResetForm
from .forms import PasswordResetRequestForm
from .util import is_safe_url


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_email(email=form.email.data)

        if user is not None and user.verify_password(form.password.data):
            # the optional parameter to the 'login_user' function will store
            # a long-term cookie on the client
            login_user(user, form.remember_me.data)
            flash('Logged in successfully.', 'success')

            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('main.dashboard'))

    flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    # send_email(current_user.email, 'Confirm Your Account',
    #            'auth/email/confirm', user=current_user, token=token)
    flash(
        'A new confirmation email has been sent to you by email. {0} '.format(
            token), 'info')
    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            # db.session.add(current_user)
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.', 'error')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.get_email(email=form.email.data)
        if user:
            # token = user.generate_reset_token()
            pass
        flash('An email with instructions to reset your password has been '
              'sent to you.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.get_email(email=form.email.data)
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            # new_email = form.email.data
            # token = current_user.generate_email_change_token(new_email)
            # send_email(new_email, 'Confirm your email address',
            #            'auth/email/change_email',
            #            user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('Invalid request.', 'error')
    return redirect(url_for('main.index'))
