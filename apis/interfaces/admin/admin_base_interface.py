from apis.interfaces.admin.users_interface import UsersInterface


class AdminBaseInterface(object):
    @property
    def users(self) -> UsersInterface:
        return UsersInterface(self)
