# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from google.cloud import pubsub


class ChimolaScraperPipeline(object):
    def __init__(self, publish_project, publish_topic, credentials_file_path):
        self.publish_project = publish_project
        self.publish_topic = publish_topic
        self.credentials_file_path = credentials_file_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            publish_project=crawler.settings.get('PUBLISH_PROJECT'),
            publish_topic=crawler.settings.get('PUBLISH_TOPIC', 'items'),
            credentials_file_path=crawler.settings.get(
                'GCLOUD_CREDENTIALS_FILE_PATH')
        )

    def open_spider(self, spider):
        self.publish_client = pubsub.PublisherClient \
            .from_service_account_json(self.credentials_file_path)
        self.publish_resource = self.publish_client.topic_path(
            self.publish_project, self.publish_topic
        )

    def process_item(self, item, spider):
        def callback(future):
            message_id = future.result()
            print("Message published: {}".format(message_id))

        future = self.publish_client.publish(
            self.publish_resource,
            str(dict(item)).encode('utf-8')
        )
        future.add_done_callback(callback)
        return item
