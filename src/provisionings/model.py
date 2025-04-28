from typing import List
from src.provisionings.schemas import Provisioning
from src.commons.postgres import database

async def get_user_provisionings(user_id) -> List[Provisioning]:
    query = "SELECT id, updated_at, created_at, display_name FROM provisionings WHERE user_id = $1"
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, user_id)
        provisionings = [Provisioning(id=record["id"], updated_at=record["updated_at"], created_at=record['created_at'], display_name=record['display_name']) for record in rows]
        return provisionings


async def create_provisioning(user_id: str, display_name: str) -> Provisioning:
    query = "INSERT INTO provisionings (user_id, display_name) VALUES ($1, $2) RETURNING id, updated_at, created_at, display_name"
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, user_id, display_name)
        return Provisioning(id=row["id"], updated_at=row["updated_at"], created_at=row['created_at'], display_name=row['display_name'])