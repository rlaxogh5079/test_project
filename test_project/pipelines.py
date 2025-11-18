from itemadapter import ItemAdapter
import traceback
import logging
import MySQLdb 


class TestProjectPipeline:
    def __init__(self, host, user, password, database): # 생성자
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    @classmethod
    def from_crawler(cls, crawler):
    	# crawler.settings.get("설정이름") = settings.py 파일로부터 "설정 이름" 변수 값을 불러옵니다.
        host = crawler.settings.get("DB_HOST")
        user = crawler.settings.get("DB_USER")
        password = crawler.settings.get("DB_PASSWORD")
        database = crawler.settings.get("DB_NAME")
        return cls(host, user, password, database)
    
    def open_spider(self, spider):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.database)
        self.cursor = self.connection.cursor()
        
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
    
    def process_item(self, item, spider):
        try:
            placeholders = ', '.join(['%s'] * len(item['tags']))
            sql = (
                f"INSERT INTO quotes (quote, name, tags) "
                f"VALUES (%s, %s, JSON_ARRAY({placeholders}))"
            )
            params = [item['quote'], item['name'], *item['tags']]
            self.cursor.execute(sql, params)
            
        except MySQLdb.Error as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            
        finally:
            self.connection.commit()
            
        return item