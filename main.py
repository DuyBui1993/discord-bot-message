import asyncio
import discord
import os


user_token = os.getenv('USER_TOKEN')
print(f"Token: {user_token}")
channel_id = int(os.getenv('CHANNEL_ID'))
print(f"Channel ID: {channel_id}")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.do_spam()

    async def do_spam(self):
        channel = self.get_channel(channel_id)
        while True:
            await channel.send('/dice amount:5000', delete_after=3)
            print('Message sent!')
            await asyncio.sleep(6)
            await self.close()
            await asyncio.sleep(2)
            await self.start(user_token)


client = MyClient()
client.run(user_token)

