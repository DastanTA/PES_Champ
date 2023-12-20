import asyncpg
from asyncpg import Record


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def _stats_from_db(self, query) -> dict:
        all_records = await self.connector.fetch(query)
        all_stats = {}
        for record in all_records:
            if record["winner_id"] not in all_stats:
                all_stats[record["winner_id"]] = 1
            else:
                all_stats[record["winner_id"]] += 1

        sorted_stats_list = sorted(all_stats.items(), key=lambda x: x[1], reverse=True)
        sorted_stats = dict(sorted_stats_list)

        return sorted_stats

    async def add_user(self, user_id, first_name, group_chat_id):
        query = f"INSERT INTO users (first_name, user_id, group_chat_id) VALUES ('{first_name}', {user_id}, {group_chat_id}) ON CONFLICT (user_id) DO UPDATE SET first_name='{first_name}'"
        await self.connector.execute(query)

    async def get_user(self, user_id):
        query = f"SELECT * FROM users WHERE user_id={user_id}"
        return await self.connector.fetch(query)

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

    async def add_champion(self, group_chat_id, winner_id):
        query = f"INSERT INTO champ_results (group_chat_id, winner_id, date_created) VALUES ({group_chat_id}, {winner_id}, CURRENT_DATE)"
        await self.connector.execute(query)

    async def get_all_stats(self, group_chat_id) -> dict:
        query = f"SELECT * FROM champ_results WHERE group_chat_id = '{group_chat_id}'"
        all_stats = await self._stats_from_db(query)
        return all_stats

    async def get_stats_current_year(self, group_chat_id) -> dict:
        query = f"SELECT * FROM champ_results WHERE EXTRACT(YEAR FROM date_created) = EXTRACT(YEAR FROM CURRENT_DATE) AND group_chat_id = '{group_chat_id}'"
        this_year_stats = await self._stats_from_db(query)
        return this_year_stats
