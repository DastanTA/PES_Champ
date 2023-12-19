import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_user(self, user_id, first_name, group_chat_id):
        query = f"INSERT INTO users (first_name, user_id, group_chat_id) VALUES ('{first_name}', {user_id}, {group_chat_id}) ON CONFLICT (user_id) DO UPDATE SET first_name='{first_name}'"
        await self.connector.execute(query)

    async def check_user(self, user_id):
        query = f"SELECT * FROM users WHERE user_id={user_id}"
        found_user = await self.connector.fetch(query)
        if found_user:
            return True
        return False

    async def all_users(self, group_chat_id):
        query = f"SELECT * FROM users WHERE group_chat_id={group_chat_id}"
        return await self.connector.fetch(query)

    async def add_group(self, group_chat_id, group_name):
        query = f"INSERT INTO groups (group_chat_id, date_created, group_name) VALUES ({group_chat_id}, CURRENT_DATE, '{group_name}') ON CONFLICT (group_chat_id) DO UPDATE SET group_name='{group_name}'"
        await self.connector.execute(query)

    async def check_group(self, group_chat_id):
        query = f"SELECT * FROM groups WHERE group_chat_id = '{group_chat_id}'"
        found_group = await self.connector.fetch(query)
        if found_group:
            return True
        return False
