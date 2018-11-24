class ProductFeed:

    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items.copy()

    def add_item(self, item):
        if not isinstance(item, ProductFeed.Item):
            raise TypeError("Not a ProductFeed.Item")
        self._items.append(item)

    def size(self):
        return len(self._items)

    def clear(self):
        self._items.clear()

    @staticmethod
    def header():
        return [
            'id', 'title', 'description', 'link', 'price', 'availability',
            'image link', 'brand', 'gtin', 'identifier exists', 'produc type'
        ]

    class Item:

        def __init__(self):
            self._id = ''
            self._title = ''
            self._description = ''
            self._link = ''
            self._price = ProductFeed.Item.Price()
            self._availability = ''
            self._imageLink = ''
            self._brand = ''
            self._gtin = ''
            self._identifierExists = ''
            self._productType = ''

        @property
        def id(self):
            return self._id

        @id.setter
        def id(self, id):
            self._id = id

        @property
        def title(self):
            return self._title

        @title.setter
        def title(self, title):
            self._title = title

        @property
        def description(self):
            return self._description

        @description.setter
        def description(self, description):
            self._description = description

        @property
        def link(self):
            return self._link

        @link.setter
        def link(self, link):
            self._link = link

        @property
        def price(self):
            return self._price

        @price.setter
        def price(self, price):
            self._price = price

        @property
        def availability(self):
            return self._availability

        @availability.setter
        def availability(self, availability):
            self._availability = availability

        @property
        def imageLink(self):
            return self._imageLink

        @imageLink.setter
        def imageLink(self, imageLink):
            self._imageLink = imageLink

        @property
        def brand(self):
            return self._brand

        @brand.setter
        def brand(self, brand):
            self._brand = brand

        @property
        def gtin(self):
            return self._gtin

        @gtin.setter
        def gtin(self, gtin):
            self._gtin = gtin

        @property
        def identifierExists(self):
            return self._identifierExists

        @identifierExists.setter
        def identifierExists(self, identifierExists):
            self._identifierExists = identifierExists

        @property
        def productType(self):
            return self._productType

        @productType.setter
        def productType(self, productType):
            self._productType = productType

        def __iter__(self):
            for key in dir(self):
                if not key.startswith('_'):
                    value = getattr(self, key)
                    if not callable(value):
                        if isinstance(value, ProductFeed.Item.Price):
                            value = dict(value)
                        yield key, value

        def to_row(self):
            return [
                self.id, self.title, self.description, self.link,
                self.price.value + ' ' + self.price.currency, self.availability,
                self.imageLink, self.brand, self.gtin, self.identifierExists,
                self.productType
            ]

        class Price:

            def __init__(self, currency='ARS', value='0.00'):
                self._currency = currency
                self._value = value

            @property
            def currency(self):
                return self._currency

            @property
            def value(self):
                return self._value

            def __iter__(self):
                for key in dir(self):
                    if not key.startswith('_'):
                        value = getattr(self, key)
                        if not callable(value):
                            yield key, value
