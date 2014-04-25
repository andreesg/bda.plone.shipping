from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter
from zope.component import getAdapter
from zope.component import getAdapters
from zope.i18nmessageid import MessageFactory
from .interfaces import IShipping
from .interfaces import IItemDelivery


_ = MessageFactory('bda.plone.shipping')


class Shippings(object):

    def __init__(self, context):
        self.context = context

    def get(self, name):
        return getAdapter(self.context, IShipping, name=name)

    @property
    def shippings(self):
        adapters = getAdapters((self.context,), IShipping)
        return [_[1] for _ in adapters]

    @property
    def vocab(self):
        adapters = getAdapters((self.context,), IShipping)
        return [(_[0], _[1].label) for _ in adapters if _[1].available]

    @property
    def default(self):
        adapters = getAdapters((self.context,), IShipping)
        for name, shipping in adapters:
            if shipping.default:
                return name
        if adapters:
            return adapters[0][0]


@implementer(IShipping)
@adapter(Interface)
class Shipping(object):
    sid = None
    label = None
    available = False
    default = False

    def __init__(self, context):
        self.context = context

    def calculate(self, items):
        """Calculate shipping costs.

        @param items: list returned by 'bda.plone.cart.extractitems()'
        """
        raise NotImplementedError(u"Abstract ``Shipping`` does not implement "
                                  u"``calculate``")


@implementer(IItemDelivery)
@adapter(Interface)
class NullItemDelivery(object):
    delivery_duration = None

    def __init__(self, context):
        self.context = context
