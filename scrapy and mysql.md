```
import logging
import json
import mysql.connector as Connector


class TutorialPipeline(object):

    config = {
        'user': 'your database user name',
        'database': 'your database name',
        'password': 'your database password',
    }

    def open_spider(self, spider):
        logging.log(logging.INFO, "open_spider")
        self.con = Connector.connect(**self.config)
        self.cursor = self.con.cursor()

    def process_item(self, item, spider):
        logging.log(logging.INFO, "process_item ")
        add_command = u'INSERT INTO movie_table (title, cover, detail, thumbnails, download_links)' \
                      u' VALUES (%s, %s, %s, %s, %s)'
        add_params = (item['title'], item['cover'], item['detail'], json.dumps(item['thumbnails']), json.dumps(item['download_links']))
        self.cursor.execute(add_command, add_params)
        self.con.commit()
        return item
```
