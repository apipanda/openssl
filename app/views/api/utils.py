import arrow

from datetime import date


def clean(collection):
    del collection['_id']

    return collection


def _search(bvn, app):
    bio = app.db.bios.find_one(
        {'_id': bvn}, projection=['bvn', 'first_name', 'last_name',
                                  'gender', 'dob', 'created_at'])

    if not bio:
        bio = {'status': 'error', 'data': None,
               'message': 'Unknown Bank Verification Number'}

    bio['dob'] = get_age(bio.get('dob'))
    bio['created_at'] = humanize_date(bio.get('created_at'))

    payrolls = app.db.payrolls.find({'_id': bvn})
    work = app.db.work_histories.find({'_id': bvn})
    data = {}
    data['payrolls'] = payrolls.distinct('rows')
    data['work_histories'] = work.distinct('rows')
    data['mortgages'] = []
    data['rents'] = []
    data['utilities'] = []
    data['loans'] = []
    data['education_histories'] = []

    bio.update(buckets=data)

    return bio


def _search_bucket(bvn, bucket, app):
    bucket_collection = app.db.get_collection(bucket)

    if not bucket:
        data = {'status': 'error', 'data': [],
                'message': 'Unknown Bucket Name.'}
        return data

    record = bucket_collection.find({'_id': bvn})

    if not record:
        data = {
            'status': 'error', 'data': [],
            'message': 'No {0} Record exist for this user yet.'.format(bucket)}

    else:
        data = record.distinct('rows')
    return map((lambda d: d.pop('bvn') and d), data)


def get_age(born=None):

    if not born:
        return 'No Age Record'
    born = arrow.get(born).datetime
    today = date.today()
    age = today.year - born.year - (
        (today.month, today.day) < (born.month, born.day))

    return '{0} years'.format(age)


def humanize_date(value):
    return arrow.get(value).humanize()
