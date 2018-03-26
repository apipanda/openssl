from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from . import main
from .forms import SearchForm

from ..api.utils import _search


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    bio = app.db.bios.count()
    payroll = app.db.payrolls.count()
    work = app.db.work_histories.count()

    context = {
        'counter': {
            'Bio': bio,
            'Payrolls': payroll,
            'Work Histories': work,
            'Mortgages': 0,
            'Rents': 0,
            'Utilities': 0,
            'Loans': 0,
            'Education Histories': 0
        },
        'total_records': bio + payroll + work
    }
    context.update(labels=list(context['counter'].keys()),
                   values=list(context['counter'].values()))
    return render_template('main/dashboard.html', **context)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    context = {}
    form = SearchForm()

    if form.validate_on_submit():
        bvn = form.bvn.data

        context.update(bvn=form.bvn.data)
        result = _search(bvn, app)

        if result.get('status') == 'error':
            flash(result.get('message'), 'error')
        context.update(enrollee=result)
    else:
        for error in form.errors.values():
            if isinstance(error, list):
                for e in error:
                    flash(e, 'error')
            else:
                flash(error, 'error')
    return render_template('search/results.html', **context)
