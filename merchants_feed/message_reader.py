import ast
from product_feed import ProductFeed


class ChimolaProductMessageReader:
    @staticmethod
    def read(message):
        print('Reading Message with ID: {}...'.format(message.message_id))
        product_str = message.data.decode('utf-8')
        print('Message content: {}'.format(product_str))
        product = ast.literal_eval(product_str)
        if ChimolaProductMessageReader.is_valid(product):
            print('Product Id: {}'.format(product['id']))
            print('Porduct title: {}'.format(product['title']))
            return product
        else:
            return None

    @staticmethod
    def is_valid(product):
        if 'id' not in product:
            return False
        if 'title' not in product:
            return False
        # if 'description' not in product:
        #    return False
        if 'url' not in product:
            return False
        if 'price' not in product:
            return False
        if 'availability' not in product:
            return False
        if 'image_urls' not in product:
            return False
        if 'category_path' not in product:
            return False

        return True


class ChimolaProductMapper:
    @staticmethod
    def map(product):
        item_feed = ProductFeed.Item()
        item_feed.id = product.get('id')
        item_feed.title = product.get('title')
        item_feed.description = product.get('description')
        item_feed.link = product.get('url')
        item_feed.price = ProductFeed.Item.Price(value=product.get('price'))
        item_feed.availability = product.get('availability')
        imageUrls = product.get('image_urls', [])
        if len(imageUrls) > 0:
            item_feed.imageLink = 'https:' + imageUrls[0]
        item_feed.brand = 'Chimola'
        item_feed.identifierExists = 'no'
        item_feed.productType = ' > '.join(product.get('category_path', []))
        return item_feed
