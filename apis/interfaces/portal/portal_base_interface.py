from apis.interfaces.portal.orders_interface import OrdersInterface


class PortalBaseInterface(object):
    @property
    def orders(self) -> OrdersInterface:
        return OrdersInterface(self)
