from apis.interfaces.admin.collections_interface import CollectionsInterface
from apis.interfaces.admin.users_interface import UsersInterface


class AdminBaseInterface(object):
    @property
    def users(self) -> UsersInterface:
        return UsersInterface(self)

    @property
    def collections(self) -> CollectionsInterface:
        return CollectionsInterface(self)