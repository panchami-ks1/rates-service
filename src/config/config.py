import os


class Config:
    def __init__(self):
        self.PG_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:ratestask@localhost:5432/ratestask')
        self.CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
        self.CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'localhost')
        self.CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT', 6379)
        self.CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT', 300)


config = Config()
