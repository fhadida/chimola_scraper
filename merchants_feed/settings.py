# -*- coding: utf-8 -*-

# Settings for merchants_feed project

GCLOUD_CREDENTIALS_FILE_PATH = '../keys/Chimola-a45eb1362770.json'
PUB_SUB = {
    'project_id': 'chimola-213915',
    'publish_topic': 'product_feed',
    'sub_name': 'merchant_center'
}

FTP = {
    'hostname': 'ftp.{SECRET_FTP_CHIMOLA_USERNAME}.ferozo.com',
    'username': '{SECRET_FTP_CHIMOLA_USERNAME}',
    'password': '{SECRET_FTP_CHIMOLA_PASSWORD}'
}

FEED_CSV_PATH = './products_feed.txt'
