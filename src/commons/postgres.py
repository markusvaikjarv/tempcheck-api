import asyncpg
import os

class Postgres:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        print('Connecting to database...')
        self.pool = await asyncpg.create_pool(self.database_url)
        print('Connected to database')

    async def disconnect(self):
        self.pool.terminate()


database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError('DATABASE_URL is not set')

database = Postgres(database_url)
