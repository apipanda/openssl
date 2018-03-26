from app.extensions.json import jsonify

from . import api
from .utils import _search, _search_bucket
from flask import current_app as app
from flask import request
from flask_login import login_required


@api.route('/stats')
@login_required
def stats():
    bio = app.db.bios.count()
    payroll = app.db.payrolls.count()
    work = app.db.work_histories.count()

    context = {
        'counter': {
            'bio': bio,
            'pay_histories': payroll,
            'work_histories': work,
            'mortgages': 0,
            'rents': 0,
            'utilities': 0,
            'loans': 0,
            'education_histories': 0
        },
        'total_records': bio + payroll + work
    }
    return jsonify(context)


@api.route('/search', methods=['GET'])
@login_required
def search():
    bvn = request.args.get('bvn')
    bio = _search(bvn, app)

    return jsonify(bio)


@api.route('/bucket', methods=['GET'])
@login_required
def bucket_search():
    bvn = request.args.get('bvn')
    bucket = request.args.get('bucket')

    data = _search_bucket(bvn, bucket, app)

    return jsonify(data)
