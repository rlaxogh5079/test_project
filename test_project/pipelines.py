from itemadapter import ItemAdapter
import traceback
import logging
import time
import MySQLdb 


class TestProjectPipeline:
    def __init__(self, host, port, user, password, database): # 생성자
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    @classmethod
    def from_crawler(cls, crawler):
    	# crawler.settings.get("설정이름") = settings.py 파일로부터 "설정 이름" 변수 값을 불러옵니다.
        host = crawler.settings.get("DB_HOST")
        port = crawler.settings.getint("DB_PORT")
        user = crawler.settings.get("DB_USER")
        password = crawler.settings.get("DB_PASSWORD")
        database = crawler.settings.get("DB_NAME")
        return cls(host, port, user, password, database)
    
    def open_spider(self, spider):
        max_attempts = 5
        for attempt in range(1, max_attempts + 1):
            try:
                self.connection = MySQLdb.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.password,
                    db=self.database,
                    charset="utf8mb4",
                )
                self.cursor = self.connection.cursor()
                self._ensure_table()
                return
            except MySQLdb.Error as e:
                logging.error(f"데이터베이스 연결 실패({attempt}/{max_attempts}): {e}")
                time.sleep(5)
        self.connection = None
        self.cursor = None
    
    def _ensure_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS quotes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            quote TEXT NOT NULL,
            name VARCHAR(255) NOT NULL,
            tags JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_sql)
        self.connection.commit()
        
    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def process_item(self, item, spider):
        if not self.connection or not self.cursor:
            logging.error("DB 연결이 설정되지 않아 아이템을 저장하지 못했습니다.")
            return item
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
