import os

BOT_NAME = "test_project"

SPIDER_MODULES = ["test_project.spiders"]
NEWSPIDER_MODULE = "test_project.spiders"

ADDONS = {}

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "quote")
DB_PASSWORD = os.getenv("DB_PASSWORD", "quote_password")
DB_NAME = os.getenv("DB_NAME", "quotes")

ITEM_PIPELINES = {
    "test_project.pipelines.TestProjectPipeline": 100, # 숫자가 낮을 수록, 우선순위가 높음
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
