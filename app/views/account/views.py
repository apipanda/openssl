from flask import current_app as app
from flask import render_template
from flask_login import login_required

from . import account


@account.route('/dashboard', methods=['GET'])
# @login_required
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
    return render_template('account/dashboard.html', **context)
