from .allows import Allows
from .requirements import Requirement
from flask import current_app as app
from flask import g


allows = Allows(identity_loader=lambda: g.user)


def is_staff(identity, request):
    pass


class CanAccessBucket(Requirement):
    """docstring for CanAccessBucket"""

    def __init__(self, arg):
        super(CanAccessBucket, self).__init__()
        self.arg = arg

    def fulfill(self, identity, request):
        forum_id = self.determine_forum_id(request)
        user_group_ids = self.get_user_group_ids(user)

        q = Forum.query.with_entities(Forum.id).filter(
            Forum.id == forum_id, Forum.groups.any(
                Group.id.in_(user_group_ids))
        ).first()

        return q is not None

    def determine_forum(self, request):
        # do something complicated to determine the forum_id
        return request.view_args['forum_id']

    def user_group_ids(self, user):
        if user.is_anonymous():
            return [Group.get_guest_group().id]
        else:
            return [gr.id for gr in user.groups]
