from google.cloud import pubsub
from message_reader import ChimolaProductMessageReader, ChimolaProductMapper
from product_feed import ProductFeed
from chimola_ftp import ChimolaFTP
from concurrent.futures import ThreadPoolExecutor
import time
# from merchants_center import MerchantsCenterClient

# Do not forget to set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Fede\Documents\GCP Keys\Chimola-a45eb1362770.json

SUB_NAME = 'projects/chimola-213915/subscriptions/merchant_center'
# merchantsCenterClient = MerchantsCenterClient('123298316')
feed = ProductFeed()


def callback(message):
    product = ChimolaProductMessageReader.read(message)
    itemfeed = ChimolaProductMapper.map(product)
    # merchantsCenterClient.send(feed)
    feed.add_item(itemfeed)
    message.ack()


def read_message(message):
    print('Message ID: {}'.format(message.message_id))
    product_str = message.data.decode('utf-8')
    print('Message content: {}'.format(product_str))


def upload_feed(ftp):
    size_0 = feed.size()
    print("Feed size={}".format(size_0))
    while True:
        time.sleep(30)
        size_f = feed.size()
        print("Current Feed size={}".format(size_f))
        if size_0 == size_f and size_f > 0:
            print("Calling the upload feed as TXT process...")
            try:
                ftp.upload_asTXT("products_feed.txt", feed)
                print("Feed uploaded!")
                feed.clear()
                size_0 = feed.size()
            except Exception as ex:
                print(ex)
                raise
        else:
            size_0 = size_f


def main():
    subscriber = pubsub.SubscriberClient()
    print("subscriber created!")
    subs_future = subscriber.subscribe(SUB_NAME, callback)
    print("subscriber subcribed to {}!".format(SUB_NAME))
    ftp = ChimolaFTP('ftp.c0310255.ferozo.com', 'c0310255', 'biDIri20fo')
    upload_future = ThreadPoolExecutor(max_workers=1).submit(upload_feed, ftp)
    print("executor created and submited!")
    try:
        print("wating for messages...")
        subs_future.result()
        print("wating for upload feed...")
        upload_future.result()
    except (KeyboardInterrupt, Exception) as ex:
        subs_future.cancel()
        upload_future.cancel()
        print(ex)
        raise


if __name__ == "__main__":
    main()
