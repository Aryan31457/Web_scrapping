# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        return item
    

import mysql.connector
class SavetoMySQLPipeline:
    def __init__(self):
        self.conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='books'
        )

        self.cur=self.conn.cursor() 

    def process_item():
        pass


    def close_spider(self,commit):

        self.cur.close()
        self.conn.close()

